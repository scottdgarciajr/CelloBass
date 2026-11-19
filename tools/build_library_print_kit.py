"""Create the Penn State PLA bench-test kit. No instrument or load-bearing parts."""
from pathlib import Path
import json, sys, zipfile
import cadquery as cq
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'output/print-test-kit'
sys.path.insert(0, str(ROOT/'output/source'))
sys.path.insert(0, str(ROOT/'output/r03/source'))
from build_coupons import hinge_base, bore_z, box
from build_connected_study import tongue

NAMES = ['01_PRINT_FIRST_Pin_Fit_Gauge.stl', '02_Tabletop_Hinge_Base.stl',
         '03_Tabletop_Hinge_Cap.stl', '04_Tabletop_Hinge_Arm.stl']
BUILD = np.array([250, 210, 220])


def gauge():
    part = box(100, 48, 4, (0, 0, 2))
    font = Path('C:/Windows/Fonts/arialbd.ttf')
    def mark(x, y, label, size):
        return cq.Workplane('XY').text(label, size, 0.8, fontPath=str(font), combine=False).translate((x,y,3.4))
    for y, hardware in [(12,6), (-12,4)]:
        for x, extra in zip([-36,-18,0,18,36],[.1,.2,.3,.4,.5]):
            d = hardware + extra
            part = bore_z(part,x,y,d)
            part = part.cut(mark(x,y-7,f'{d:.1f}',4.2))
    part = part.cut(mark(0,21,'6 mm PIVOT PIN',4))
    part = part.cut(mark(0,-3,'4 mm LOCK PIN',4))
    return part


def build():
    (KIT/'STL').mkdir(parents=True, exist_ok=True)
    full = hinge_base()
    # Split the r0.3 clevis at the roof. Both pieces print flat with no trapped support.
    lower = full.intersect(box(100,100,14,(0,0,7)))
    cap_installed = full.intersect(box(100,100,4,(0,0,16)))
    cap = cap_installed.translate((0,0,-14))
    arm_installed = tongue()
    arm = arm_installed.translate((0,0,-4.3))
    solids = [gauge(),lower,cap,arm]
    rows = []
    for name, part in zip(NAMES, solids):
        assert part.val().isValid() and len(part.solids().vals()) == 1, name
        dest = KIT/'STL'/name
        cq.exporters.export(part, str(dest), tolerance=.04, angularTolerance=.1)
        mesh = trimesh.load_mesh(dest)
        assert mesh.is_volume and len(mesh.split()) == 1, name
        assert abs(mesh.bounds[0,2]) < .001 and (mesh.extents + [10,10,0] <= BUILD).all(), name
        # Ignore shallow tessellation deviations along the vertical lettering walls.
        # Reject overhangs exceeding 30 degrees from vertical away from the bed.
        down = (mesh.face_normals[:,2] < -.5) & (mesh.triangles[:,:,2].max(axis=1) > .005)
        assert not down.any(), (name, int(down.sum()))
        rows.append(dict(file=name, size_mm=np.round(mesh.extents,2).tolist(),
                         closed_single_solid=True, flat_at_z0=True, unsupported_faces=0))
    base = lower.val().fuse(cap_installed.val())
    assert abs(base.Volume()-full.val().Volume()) < .001
    arm_shape = arm_installed.val()
    for angle in range(91):
        moved=arm_shape.rotate((0,0,0),(0,0,1),angle)
        assert base.intersect(moved).Volume() < .001, angle
    for angle in [-1,91]:
        assert base.intersect(arm_shape.rotate((0,0,0),(0,0,1),angle)).Volume() > .01
    for angle, x, y in [(0,24,0),(90,0,24)]:
        lock=cq.Workplane('XY').center(x,y).circle(2).extrude(18).val()
        moved=arm_shape.rotate((0,0,0),(0,0,1),angle)
        assert base.intersect(lock).Volume()+moved.intersect(lock).Volume() < .001
        # A seated lock must stop the arm from swinging into its allowed arc.
        toward_arc = 1 if angle == 0 else 89
        attempted_turn = arm_shape.rotate((0,0,0),(0,0,1),toward_arc)
        assert attempted_turn.intersect(lock).Volume() > .01
        for lift in range(19):
            raised_lock = lock.translate((0,0,lift))
            assert base.intersect(raised_lock).Volume()+moved.intersect(raised_lock).Volume() < .001
    for x,y,r in [(0,0,3),(-23,-8,2.5),(-23,8,2.5)]:
        shank=cq.Workplane('XY').center(x,y).circle(r).extrude(18).val()
        assert base.intersect(shank).Volume()+arm_shape.intersect(shank).Volume() < .001
    (KIT/'Print_checks.json').write_text(json.dumps(dict(parts=rows,
        target='Penn State Maker Commons Prusa MK4S PLA profile', build_volume_mm=BUILD.tolist(),
        hinge_positions_checked=91, overtravel_stops_checked=True, pin_alignment_checked=True,
        lock_blocks_turn_at_both_stops=True, lock_withdrawal_positions_per_stop=19,
        status='Geometry checked. Not physically printed or sliced in Penn State account. Tabletop demonstration only.'),indent=2))
    target=ROOT/'CelloBass_Penn_State_TEST_PRINTS_ONLY.zip'
    contents=[KIT/'START_HERE.html',KIT/'Print_checks.json',*[KIT/'STL'/name for name in NAMES]]
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in contents:
            archive.write(path,path.relative_to(KIT).as_posix())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None and len(archive.namelist()) == 6
    print(json.dumps(rows));print(target)

if __name__=='__main__':build()
