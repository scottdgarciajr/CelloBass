from pathlib import Path
import sys,json,math
import numpy as np
import trimesh
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/r03'
sys.path.insert(0,str(OUT/'source'))
from build_connected_study import frame,tongue,cushion,P,local_to_world,shape_mesh,rot
sys.path.insert(0,str(ROOT/'output/source'))
from build_coupons import hinge_base
checks=[]
def check(name,result,detail):
    checks.append(dict(check=name,pass_=bool(result),detail=detail));assert result,(name,detail)
for path in (OUT/'study').glob('*.step'):
    shape=cq.importers.importStep(str(path)).val();check('STEP '+path.stem,shape.isValid() and shape.Volume()>0,'Solid re-import')
base=hinge_base().val()
sweep=[]
for side in [-1,1]:
    fixed=[('tongue',tongue().val()),('frame',frame(side).val()),('pad',cushion(side).val())]
    for angle in range(91):
        for name,shape in fixed:
            moving=shape.rotate((0,0,0),(0,0,1),angle)
            overlap=base.intersect(moving).Volume()
            sweep.append(dict(side=side,angle_deg=angle,part=name,base_overlap_mm3=overlap))
            assert overlap<.001,(side,angle,name,overlap)
check('moving tongue/frame/pad against hinge base',True,'546 exact solid comparisons at 1 degree intervals; no volume overlap')
for angle in [-1,91]:check('hinge overtravel '+str(angle),base.intersect(tongue().val().rotate((0,0,0),(0,0,1),angle)).Volume()>.01,'Hard stops block extended r03 tongue')
model=json.loads((OUT/'study/connected_model.json').read_text())
inv=np.linalg.inv(rot(-70,P['rotation_center_mm']));drift=0
for a,b in zip(model['states']['cello'],model['states']['bass']):
    assert a['name']==b['name'];v=trimesh.transform_points(b['vertices'],inv);drift=max(drift,float(np.abs(v-np.array(a['vertices'])).max()))
check('unchanged live assembly',drift<.001,{'max_error_mm':drift,'live_wing_fold_deg':0})
for part in model['parts']:
    m=trimesh.Trimesh(vertices=part['vertices'],faces=part['faces'])
    check('closed positive mesh '+part['name'],m.is_watertight and m.volume>0,'Source or study geometry, not a print/strength release')
    if part['role']=='core':
        source=trimesh.load_mesh(ROOT/f'output/source_meshes/mm/{part["name"]}.stl')
        from scipy.spatial import cKDTree
        error=cKDTree(source.vertices).query(part['vertices'])[0].max();check('original mesh preserved '+part['name'],error<.0001,float(error))
(OUT/'reports/hinge_sweep.json').write_text(json.dumps(sweep,indent=2))
(OUT/'reports/revision_checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'limitations':'No whole-instrument or human sweep certification. No structural or comfort result.'},indent=2))
print(len(checks),'r03 checks passed; 546 local moving-solid sweep comparisons')
