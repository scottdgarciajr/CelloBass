"""CelloBass r0.2: ORIGINAL, isolated, non-load-rated fit-test coupons.
Run from project root with .venv/Scripts/python.exe output/source/build_coupons.py.
Dimensions in mm. Printed anchors/swivel are mock fixtures, never suspension hardware.
"""
from pathlib import Path
import csv, json, math
import cadquery as cq
import trimesh

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'output'
PARAMS = {
    'pivot_diameter_mm':6.3, 'pivot_hardware_mm':6,
    'lock_diameter_mm':4.3, 'lock_hardware_mm':4,
    'tongue_bottom_mm':4.3, 'tongue_top_mm':13.7,
    'clevis_gap_mm':10, 'index_radius_mm':24,
    'rod_nominal_mm':12, 'rod_coupon_bore_mm':12.4,
    'endpin_nominal_mm':10, 'endpin_coupon_bore_mm':10.5,
    'printer_mm':[200,200,200],
}

def box(x,y,z,center):
    return cq.Workplane('XY').box(x,y,z).translate(center)

def bore_z(shape, x,y,d,z0=-1,h=40):
    return shape.cut(cq.Workplane('XY').center(x,y).circle(d/2).extrude(h).translate((0,0,z0)))

def hinge_base():
    # 4-mm plates, 10-mm internal gap; M6 pin and two M4 positive lock positions.
    lower = cq.Workplane('XY').circle(34).extrude(4)
    upper = lower.translate((0,0,14))
    p=lower.union(upper).union(box(14,28,10,(-23,0,9)))
    # Hard-stop faces are y=-9 (0 deg) and x=-9 (90 deg).
    p=p.union(box(18,5,10,(21,-11.5,9))).union(box(5,18,10,(-11.5,21,9)))
    p=bore_z(p,0,0,PARAMS['pivot_diameter_mm'])
    for x,y in [(24,0),(0,24),(-23,-8),(-23,8)]:
        p=bore_z(p,x,y,4.3 if x>=0 else 5.5)
    return p

def hinge_tongue():
    p=cq.Workplane('XY').circle(10).extrude(9.4)
    p=p.union(box(60,18,9.4,(30,0,4.7)))
    for x,d in [(0,6.3),(24,4.3),(46,5.5)]: p=bore_z(p,x,0,d)
    return p

def anchor_drill_template():
    # Metal backplate layout template, no printed suspension path.
    p=box(64,34,6,(0,0,3))
    for x,y,d in [(-24,-10,5.5),(-24,10,5.5),(24,-10,5.5),(24,10,5.5),(0,0,8.5)]:
        p=bore_z(p,x,y,d)
    return p

def rod_saddle_half():
    # Fits a separate dummy 12-mm rod; clamping friction is NOT a live anchor design.
    p=box(42,32,14,(0,0,7))
    tool=cq.Workplane('YZ').circle(6.2).extrude(50,both=True).translate((0,0,14))
    p=p.cut(tool)
    for x in [-14,14]:
        for y in [-11,11]: p=bore_z(p,x,y,5.5)
    return p

def swivel_mock():
    p=cq.Workplane('XY').circle(30).extrude(8)
    p=bore_z(p,0,0,8.5)
    for angle in [0,45,90]:
        a=math.radians(angle); p=bore_z(p,22*math.cos(a),22*math.sin(a),4.3)
    # Strap webbing mock slot: 26 x 4 mm, through.
    return p.cut(box(26,4,12,(0,-18,4)))

def travel_latch():
    p=box(44,24,5,(0,0,2.5))
    p=p.union(box(8,24,16,(-18,0,13))).union(box(8,24,16,(18,0,13)))
    # Cross pin axis x, 12-mm open gap under pin. Two cheeks capture a wing tang.
    hole=cq.Workplane('YZ').center(0,14).circle(2.15).extrude(60,both=True)
    p=p.cut(hole)
    for x in [-10,10]: p=bore_z(p,x,0,5.5)
    return p

def travel_tang():
    p=box(22,18,18,(0,0,9))
    return p.cut(cq.Workplane('YZ').center(0,11).circle(2.15).extrude(40,both=True))

def endpin_clip():
    # TPU C-clip; temporary retention only, not the floor-load clamp.
    p=cq.Workplane('XY').circle(10).circle(5.25).extrude(16)
    p=p.cut(box(8,14,20,(0,10,8)))
    p=p.union(box(32,8,5,(0,-10,2.5)))
    for x in [-12,12]: p=bore_z(p,x,-10,3.5)
    return p

def clearance_gauge():
    p=box(100,30,6,(0,0,3))
    for x,d in zip([-40,-20,0,20,40],[6.1,6.2,6.3,6.4,6.5]): p=bore_z(p,x,0,d)
    return p

def rod_ring_gauge():
    p=box(100,30,6,(0,0,3))
    for x,d in zip([-36,-12,12,36],[12.0,12.2,12.4,12.6]): p=bore_z(p,x,0,d)
    return p

PARTS = {
 'C01_anchor_drill_template':(anchor_drill_template,'PETG','Flat; steel plate drilling/fit template only'),
 'C02_rod_saddle_half':(rod_saddle_half,'PETG','Flat base; print two for dummy-rod fit only'),
 'C03_swivel_mock':(swivel_mock,'PETG','Disk flat; print two; anti-roll pin mock, no live suspension'),
 'C04_wing_hinge_base':(hinge_base,'PETG','Lower disk flat; supports under upper disk; clear bores after print'),
 'C05_wing_hinge_tongue':(hinge_tongue,'PETG','Flat; 0.3 mm axial gap each side'),
 'C06_travel_latch':(travel_latch,'PETG','Base flat; support transverse pin bores'),
 'C07_travel_tang':(travel_tang,'PETG','Base flat; fit pin to C06 at tang bottom z=3 mm'),
 'C08_endpin_stow_clip':(endpin_clip,'TPU','Flat flange; no support; retention only'),
 'C09_M6_clearance_gauge':(clearance_gauge,'PETG','Flat; diameters left to right 6.1/6.2/6.3/6.4/6.5'),
 'C10_rod_clearance_gauge':(rod_ring_gauge,'PETG','Flat; diameters left to right 12.0/12.2/12.4/12.6'),
}

def build():
    for folder in ['stl/coupons','step/coupons','reports']:(OUT/folder).mkdir(parents=True,exist_ok=True)
    checks=[]; shapes={}
    for name,(fn,material,orientation) in PARTS.items():
        obj=fn(); shape=obj.val(); shapes[name]=shape
        assert shape.isValid(),name
        assert len(obj.solids().vals())==1,name
        cq.exporters.export(obj,str(OUT/f'stl/coupons/{name}.stl'),tolerance=0.08,angularTolerance=0.1)
        cq.exporters.export(obj,str(OUT/f'step/coupons/{name}.step'))
        mesh=trimesh.load_mesh(OUT/f'stl/coupons/{name}.stl')
        extent=mesh.extents
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
        assert all(extent[i]<=PARAMS['printer_mm'][i] for i in range(3)),name
        checks.append(dict(part=name,material=material,x_mm=round(extent[0],3),y_mm=round(extent[1],3),z_mm=round(extent[2],3),
                           volume_mm3=round(mesh.volume,2),watertight=mesh.is_watertight,one_solid=True,printer_fit=True,print_orientation=orientation))
        print(name,'OK',extent,flush=True)
    with (OUT/'reports/coupon_checks.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,checks[0].keys());w.writeheader();w.writerows(checks)
    # Check actual solids throughout the hinge's allowed quadrant, not only endpoints.
    base=shapes['C04_wing_hinge_base']; tongue=shapes['C05_wing_hinge_tongue'].translate((0,0,4.3))
    swept=[]
    for deg in range(0,91):
        moved=tongue.rotate((0,0,0),(0,0,1),deg)
        overlap=base.intersect(moved).Volume()
        swept.append({'angle_deg':deg,'overlap_mm3':overlap})
        assert overlap<0.001, f'Hinge collision {deg}: {overlap}'
    (OUT/'reports/hinge_sweep.json').write_text(json.dumps(swept,indent=2))
    (OUT/'source/coupon_parameters.json').write_text(json.dumps(PARAMS,indent=2))
    assy=cq.Assembly(name='Bench_only_hinge')
    assy.add(base,name='base');assy.add(tongue,name='tongue')
    assy.export(str(OUT/'step/hinge_bench_assembly.step'))
    print('91 hinge positions: no solid interference. Printed clearances NOT TESTED.')

if __name__=='__main__': build()
