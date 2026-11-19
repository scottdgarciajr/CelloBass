from pathlib import Path
import csv,hashlib,json,math
import numpy as np
import trimesh
import cadquery as cq
import sys

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
sys.path.insert(0,str(OUT/'source'))
from build_coupons import hinge_base,hinge_tongue

checks=[]
def record(name,passed,detail):
    checks.append({'check':name,'pass':bool(passed),'detail':detail})
    print(name, 'PASS' if passed else 'FAIL',flush=True)
    assert passed,detail

for item in csv.DictReader((ROOT/'tools/source_hashes.lock.csv').open()):
    path=ROOT/item['path'];actual=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
    record('immutable '+item['path'],actual==item['sha256'],actual)
for path in sorted((OUT/'step/coupons').glob('*.step')):
    shape=cq.importers.importStep(str(path));box=shape.val().BoundingBox()
    record('STEP '+path.stem,shape.val().isValid() and len(shape.solids().vals())==1,[box.xlen,box.ylen,box.zlen])
    mesh=trimesh.load_mesh(OUT/f'stl/coupons/{path.stem}.stl')
    record('STL '+path.stem,mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and max(mesh.extents)<=200,mesh.extents.tolist())
    record('STEP/STL extent agreement '+path.stem,np.max(np.abs(np.array([box.xlen,box.ylen,box.zlen])-mesh.extents))<.1,'Within tessellation tolerance 0.1 mm')

base=hinge_base().val();tongue=hinge_tongue().val().translate((0,0,4.3))
for deg in [-1,91]:
    overlap=base.intersect(tongue.rotate((0,0,0),(0,0,1),deg)).Volume()
    record(f'hard stop blocks overtravel {deg} deg',overlap>.01,overlap)
for deg,xy in [(0,(24,0)),(90,(0,24))]:
    pin=cq.Workplane('XY').center(*xy).circle(2).extrude(18).val()
    moved=tongue.rotate((0,0,0),(0,0,1),deg)
    interference=base.intersect(pin).Volume()+moved.intersect(pin).Volume()
    record(f'M4 lock bore aligned {deg} deg',interference<.001,interference)

audit=json.loads((OUT/'reports/blender_audit.json').read_text())
for obj in audit['objects']:
    if obj['type']!='MESH':continue
    source=json.loads((ROOT/obj['mesh_file']).read_text())
    expected=np.array(source['vertices'])*1000
    name=Path(obj['mesh_file']).stem
    mesh=trimesh.load_mesh(OUT/f'source_meshes/mm/{name}.stl')
    # Compare all source vertices to the nearest exported STL vertex.
    from scipy.spatial import cKDTree
    error=cKDTree(mesh.vertices).query(expected)[0].max()
    record('original surface '+obj['name'],error<.0001,float(error))
state=json.loads((OUT/'context/states.json').read_text())
for name,objects in state.items():
    for ob in objects:
        mesh=trimesh.Trimesh(vertices=ob['vertices'],faces=ob['faces'])
        record(f'closed positive solid {name}/{ob["name"]}',mesh.is_watertight and mesh.volume>0,round(float(mesh.volume),3))
record('same live geometry',json.loads((OUT/'reports/live_geometry_regression.json').read_text())['pass'],'Inverse rigid transform vertex regression')
record('wing continuous padded sweep',not json.loads((OUT/'reports/wing_sweep.json').read_text())['possible_intersections'],'Limited to modeled core/wing envelopes')
(OUT/'reports/regression_checks.json').write_text(json.dumps({'passed':len(checks),'failed':0,'checks':checks},indent=2))
print(len(checks),'checks passed')
