"""Measured source + parametric envelope study, NOT a tension-ready instrument.
Musical meshes are copied unchanged in millimetres. New wings are original designs.
An entire assembly rotates for live changes; only wings rotate for travel.
"""
from pathlib import Path
import json, math
import numpy as np
import trimesh
import cadquery as cq

ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'output'
P={'hinge_x_mm':55,'hinge_y_mm':-70,'hinge_z_mm':150,
   'wing_reach_mm':155,'wing_depth_mm':12,'wing_height_mm':57,
   'rotation_center_mm':[0,-40,280],
   'metal_rail_envelope_mm':[25,10,680],
   'metal_rail_center_mm':[-40,-50,150],
   'anchor_proposals_mm':[[-40,-50,180],[-40,-50,460]],
   'mass_assumption_kg':3.5,'com_offset_assumption_mm':150,
   'status':'r0.2 ENVELOPE STUDY; live support unresolved; NOT FOR INSTRUMENT PRINT'}

def original(name):
    path=OUT/'source_meshes/mm'/(''.join(c if c.isalnum() or c in '-_' else '_' for c in name)+'.stl')
    return trimesh.load_mesh(path)

def wing():
    # Local XY interpreted as radial distance / longitudinal offset, later mapped to X/Z.
    outer=[(0,-12),(155,-12),(155,35),(125,45),(0,16)]
    inner=[(14,0),(143,0),(143,26),(123,33),(14,8)]
    part=cq.Workplane('XY').polyline(outer).close().extrude(12)
    part=part.cut(cq.Workplane('XY').polyline(inner).close().extrude(12))
    # No hinge integration asserted. Interfaces held for bench-test result.
    return part

def around_y(deg,center):
    return trimesh.transformations.rotation_matrix(math.radians(deg),[0,1,0],center)

def world_wing(local,side,fold):
    m=local.copy();v=m.vertices.copy()
    # local radial X, vertical Y -> world X/Z; extrusion behind Y.
    m.vertices=np.column_stack([side*(P['hinge_x_mm']+v[:,0]),P['hinge_y_mm']-v[:,2],P['hinge_z_mm']+v[:,1]])
    if side==-1:m.faces=m.faces[:,::-1]
    m.apply_transform(around_y(-side*fold,[side*P['hinge_x_mm'],P['hinge_y_mm'],P['hinge_z_mm']]))
    return m

def separate_bounds(a,b,pad=0):
    return bool(np.any((a[1]+pad<b[0]) | (b[1]+pad<a[0])))

def build():
    for folder in ['context','views','reports','step','source']:(OUT/folder).mkdir(exist_ok=True)
    cq.exporters.export(wing(),str(OUT/'context/wing_envelope_local.stl'))
    cq.exporters.export(wing(),str(OUT/'step/wing_envelope_ONLY.step'))
    local=trimesh.load_mesh(OUT/'context/wing_envelope_local.stl')
    core_names=[f'Part {i}' for i in range(1,7)]+['Bridge','Center bar','Nameplate','Chest rest']
    core={name:original(name) for name in core_names}
    all_states={};bounds={}
    for state,angle,fold in [('cello',0,0),('bass',-90,0),('transition',-45,0),('travel',0,90)]:
        objects=[]
        for name,mesh in core.items():objects.append((name,mesh.copy(),'original'))
        for side in [-1,1]:objects.append((f'wing_{side}',world_wing(local,side,fold),'wing'))
        # Reference proposed metal beam, no claimed connection design or hardware rating.
        rail=trimesh.creation.box(extents=P['metal_rail_envelope_mm']);rail.apply_translation(P['metal_rail_center_mm'])
        objects.append(('METAL_RAIL_ENVELOPE_unresolved',rail,'metal'))
        # Stowed 10-mm x 450-mm tube from official BOM; absent from supplied Blender model.
        tube=trimesh.creation.annulus(r_min=4,r_max=5,height=450)
        tube.apply_translation([27,-55,65]);objects.append(('ENDPIN_STOW_ASSUMED',tube,'assumed'))
        matrix=around_y(angle,P['rotation_center_mm'])
        scene=trimesh.Scene()
        data=[]
        palette={'original':[195,207,216,255],'wing':[21,164,159,255],'metal':[74,91,110,255],'assumed':[236,171,67,255]}
        for name,m,role in objects:
            m.apply_transform(matrix);m.visual.face_colors=palette[role];scene.add_geometry(m,node_name=name)
            data.append({'name':name,'role':role,'vertices':np.round(m.vertices,4).tolist(),'faces':m.faces.tolist()})
        scene.export(OUT/f'context/{state}_study.glb')
        all_states[state]=data
        bounds[state]={'min_mm':scene.bounds[0].tolist(),'max_mm':scene.bounds[1].tolist(),
                       'xyz_mm':scene.extents.tolist(),'complete_hardware':False}
    # Conservative separation check: expand each sampled wing AABB by > maximum displacement
    # to the nearest one-degree sample (radius*0.5deg), bounding continuous intermediate angles.
    max_radius=float(np.linalg.norm(local.vertices[:,:2],axis=1).max())
    pad=max_radius*math.radians(.5)+.02
    collisions=[]
    for angle in range(91):
        pair=[world_wing(local,side,angle) for side in [-1,1]]
        for side,m in zip([-1,1],pair):
            for name,c in core.items():
                if not separate_bounds(m.bounds,c.bounds,pad):
                    collisions.append({'angle':angle,'pair':[f'wing_{side}',name],'result':'BROAD_PHASE_POSSIBLE'})
        if not separate_bounds(pair[0].bounds,pair[1].bounds,2*pad):
            collisions.append({'angle':angle,'pair':['wing_-1','wing_1'],'result':'BROAD_PHASE_POSSIBLE'})
    result={'method':'AABB separation with continuous angular displacement padding',
            'angle_step_deg':1,'padding_mm':pad,'possible_intersections':collisions,
            'exclusions':'Hinges, locks, real tuners, strings, human, harness, wires and padding not fully modeled; no whole-instrument clearance certification'}
    (OUT/'reports/wing_sweep.json').write_text(json.dumps(result,indent=2))
    (OUT/'reports/state_bounds.json').write_text(json.dumps(bounds,indent=2))
    (OUT/'source/kinematic_parameters.json').write_text(json.dumps(P,indent=2))
    (OUT/'context/states.json').write_text(json.dumps(all_states,separators=(',',':')))
    # Quantify fixed live body: identical local wing vertices before global rotation.
    # Stronger regression: recover bass vertices into cello frame, compare every component.
    inverse=np.linalg.inv(around_y(-90,P['rotation_center_mm']))
    drift=[]
    for cello,bass in zip(all_states['cello'],all_states['bass']):
        recovered=trimesh.transform_points(np.array(bass['vertices']),inverse)
        drift.append(float(np.abs(recovered-np.array(cello['vertices'])).max()))
    assert max(drift)<.001
    (OUT/'reports/live_geometry_regression.json').write_text(json.dumps({'max_vertex_error_mm':max(drift),'pass':True,'wing_fold_angle_both_live_deg':0},indent=2))
    print('Bounds',json.dumps(bounds,indent=2));print('Sweep possible intersections',len(collisions))

if __name__=='__main__':build()
