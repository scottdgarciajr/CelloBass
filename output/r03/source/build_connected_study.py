"""r0.3 connected mechanism and ergonomic DESIGN STUDY, not production hardware.
Preserves original musical meshes. Removes the original projecting chest rest.
Shows explicit brackets, hinge bases, pins, bolted tongues and padded asymmetric frames.
All new solid STEP parts remain under study/, never the printable coupon directory.
"""
from pathlib import Path
import sys,json,math
import numpy as np
import trimesh
import cadquery as cq

ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'output/r03'
sys.path.insert(0,str(ROOT/'output/source'))
from build_coupons import hinge_base,bore_z,box
P={'revision':'r0.3','bass_neck_up_deg':20,'live_rotation_deg':-70,
   'bass_use_preference':'SEATED: padded lower frame is a thigh cradle; no seated fit validated',
   'rotation_center_mm':[0,-40,280],
   'hinges':{'1':[65,-60,150],'-1':[-65,-110,150]},
   'source_chest_rest':'REMOVED: projecting rigid rest interferes with dual-pose concept',
   'status':'CONNECTED CAD STUDY; metal spine attachment, ergonomics and loads NOT TESTED'}

def shape_mesh(shape):
    v,f=shape.tessellate(.35,.12)
    return trimesh.Trimesh(vertices=[x.toTuple() for x in v],faces=f,process=True)

def closed_shape(points,height,z=0):
    return cq.Workplane('XY').moveTo(*points[0]).spline(points[1:],includeCurrent=True).close().extrude(height).translate((0,0,z))

def frame(side):
    if side==1:
        outer=[(40,-18),(80,-78),(145,-72),(176,-25),(172,54),(132,116),(85,104),(40,20)]
        inner=[(85,-30),(112,-47),(142,-25),(144,34),(121,73),(96,62),(85,30)]
    else:
        outer=[(40,-18),(78,-75),(137,-65),(155,-20),(125,17),(110,45),(144,83),(130,115),(80,116),(40,20)]
        inner=[(85,-26),(117,-37),(124,-15),(95,20),(91,50),(112,81),(97,87),(78,57)]
    part=closed_shape(outer,8,13.7).cut(closed_shape(inner,12,12))
    for r in [48,68]:part=bore_z(part,r,0,5.5,z0=0,h=30)
    return part

def tongue():
    part=cq.Workplane('XY').circle(10).extrude(9.4).union(box(80,18,9.4,(40,0,4.7)))
    for r,d in [(0,6.3),(24,4.3),(48,5.5),(68,5.5)]:part=bore_z(part,r,0,d)
    return part.translate((0,0,4.3))

def cushion(side):
    if side==1:points=[(155,-55),(169,-25),(171,20),(157,65)]
    else:points=[(127,14),(111,39),(133,71)]
    # Rounded foam cushion envelope, wider in front/back than the frame.
    part=None
    for a,b in zip(points[:-1],points[1:]):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        # Keep the forearm pad 3 mm clear of the rear rail in the travel sweep.
        depth,z0=(35,-2) if side==1 else (50,-12)
        s=cq.Workplane('XY').slot2D(length+20,20,math.degrees(math.atan2(dy,dx))).extrude(depth).translate(((a[0]+b[0])/2,(a[1]+b[1])/2,z0))
        part=s if part is None else part.union(s)
    return part

def local_to_world(mesh,side):
    m=mesh.copy();v=m.vertices.copy();h=P['hinges'][str(side)]
    m.vertices=np.column_stack([h[0]+side*v[:,0],h[1]-v[:,2],h[2]+v[:,1]])
    if side==-1:m.faces=m.faces[:,::-1]
    return m

def rot(deg,point):return trimesh.transformations.rotation_matrix(math.radians(deg),[0,1,0],point)

def cylinder(radius,height,center):
    m=trimesh.creation.cylinder(radius=radius,height=height,sections=24);m.apply_translation(center);return m

def segment(a,b,radius):
    a=np.array(a);b=np.array(b);m=trimesh.creation.cylinder(radius=radius,height=np.linalg.norm(b-a),sections=10)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],b-a));m.apply_translation((a+b)/2);return m

def build():
    for folder in ['source','study','views','reports']:(OUT/folder).mkdir(parents=True,exist_ok=True)
    objects=[];solid_checks=[]
    def add(name,mesh,role='metal',motion='fixed',side=0,label=None):
        objects.append(dict(name=name,mesh=mesh,role=role,motion=motion,side=side,label=label or name))
    def cad(name,shape,role='metal',motion='fixed',side=0,local=False):
        assert shape.val().isValid(),name
        cq.exporters.export(shape,str(OUT/f'study/{name}.step'))
        m=shape_mesh(shape.val());assert m.is_watertight and m.volume>0,name
        if local:m=local_to_world(m,side)
        add(name,m,role,motion,side)
        solid_checks.append({'part':name,'valid':True,'watertight':True,'volume_mm3':float(m.volume)})
    for name in [f'Part_{i}' for i in range(1,7)]+['Bridge','Center_bar','Nameplate']:
        add(name,trimesh.load_mesh(ROOT/f'output/source_meshes/mm/{name}.stl'),'core')
    # Proposed rail, lower metal-to-rod adapter and upper secondary brace.
    cad('rear_metal_backbone',box(20,10,650,(0,-50,125)))
    lower=box(34,76,24,(0,-22,-180))
    tool=cq.Workplane('XY').center(0,4).circle(6.4).extrude(40).translate((0,0,-200))
    cad('lower_metal_adapter_PROPOSED',lower.cut(tool))
    cad('upper_secondary_saddle_PROPOSED',box(30,39,20,(0,-30.5,440)))
    crossmember=box(108,16,24,(0,-50,150))
    crossmember=crossmember.cut(cq.Workplane('XY').center(25,-49).circle(5.3).extrude(40).translate((0,0,130)))
    cad('wing_crossmember',crossmember)
    # Labels are deliberately explicit: positive rod retention is still unresolved.
    for side in [-1,1]:
        h=P['hinges'][str(side)];length=abs(h[1]-(-50))+8
        cad(f'mount_standoff_{side}',box(14,28,length,(-23,0,-length/2)),side=side,local=True)
        cad(f'clevis_base_{side}',hinge_base(),side=side,local=True)
        cad(f'hinged_tongue_{side}',tongue(),'joint','wing',side,True)
        cad(f'contoured_frame_{side}',frame(side),'frame','wing',side,True)
        cad(f'padded_contact_{side}',cushion(side),'pad','wing',side,True)
        # Steel pivot spans the actual 18-mm clevis and tongue. Head + retaining collar shown.
        for suffix,r,z,height in [('shaft',3,10,24),('head',5,-3,4),('retainer',4.5,23,3)]:
            add(f'pivot_{suffix}_{side}',local_to_world(cylinder(r,height,[0,0,z]),side),'pin',side=side)
        for rpos in [48,68]:
            bolt=trimesh.util.concatenate([cylinder(2.5,26,[rpos,0,13]),cylinder(4.5,3,[rpos,0,25])])
            add(f'frame_bolt_{side}_{rpos}',local_to_world(bolt,side),'pin','wing',side)
        for zpos in [-8,8]:
            bolt=trimesh.util.concatenate([cylinder(2.5,length+25,[-23,zpos,8-length/2]),cylinder(4.5,3,[-23,zpos,21])])
            add(f'base_bolt_{side}_{zpos}',local_to_world(bolt,side),'pin',side=side)
        # Removable captive/tethered locking pin is relocated at each endpoint.
        lock=trimesh.util.concatenate([cylinder(2,23,[24,0,9.5]),cylinder(5,5,[24,0,23])])
        add(f'wing_lock_{side}',local_to_world(lock,side),'lock','lock',side)
    # Two metal harness eyes attached to the proposed rail, not to the folding frames.
    for z in [210,420]:
        eye=trimesh.creation.annulus(r_min=4.5,r_max=8,height=5,sections=24)
        eye.apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[1,0,0]));eye.apply_translation([0,-58,z])
        add(f'harness_eye_{z}',eye,'pin')
        cad(f'harness_eye_boss_{z}',box(16,12,18,(0,-55,z)))
    # Four illustrative source-aligned string paths: explicitly not calibrated contact dimensions.
    bridge=[[-23.8,25.5,55.5],[-8,31,55.5],[8.1,32.1,55.5],[23.4,27.7,55.5]]
    for i,(x,b) in enumerate(zip([-11.85,-4.1,4.1,11.85],bridge)):
        n=[x,24,748];tail=[(-34 if i<2 else 34),-7,(-30 if i%2==0 else -85)]
        add(f'string_illustration_{i}',trimesh.util.concatenate([segment(n,b,.35),segment(b,tail,.35)]),'strings')
    # Endpin stays pre-stowed for both live views, visibly clipped to the fixed frame.
    tube=trimesh.creation.annulus(r_min=4,r_max=5,height=450);tube.apply_translation([25,-49,40]);add('stowed_endpin_tube',tube,'metal')
    for z in [-100,200]:
        clip=box(32,15,12,(15,-50,z))
        clip=clip.cut(cq.Workplane('XY').center(25,-49).circle(5.3).extrude(20).translate((0,0,z-10)))
        cad(f'endpin_bracket_{z}',clip)
    # Encode per-part motion, rather than independent drawings of different instruments.
    baseline=[]
    for ob in objects:
        data={k:v for k,v in ob.items() if k!='mesh'}
        data.update(vertices=np.round(ob['mesh'].vertices,4).tolist(),faces=ob['mesh'].faces.tolist())
        baseline.append(data)
    palette={'core':[190,201,213,255],'frame':[30,151,143,255],'pad':[69,80,89,255],
             'metal':[95,113,136,255],'joint':[40,123,133,255],'pin':[208,184,108,255],'lock':[235,145,43,255],'strings':[100,98,91,255]}
    states={};bounds={}
    for state,angle,fold in [('cello',0,0),('bass',-70,0),('transition',-35,0),('travel',0,90)]:
        scene=trimesh.Scene();data=[]
        for ob in objects:
            m=ob['mesh'].copy();side=ob['side']
            if ob['motion']=='wing':m.apply_transform(rot(-side*fold,P['hinges'][str(side)]))
            if ob['motion']=='lock' and fold:
                # Local (24,0) -> (0,24); don't rotate axis since it remains along Y.
                m.apply_translation([-side*24,0,24])
            m.apply_transform(rot(angle,P['rotation_center_mm']));m.visual.face_colors=palette[ob['role']]
            scene.add_geometry(m,node_name=ob['name'])
            data.append(dict(name=ob['name'],role=ob['role'],vertices=np.round(m.vertices,4).tolist(),faces=m.faces.tolist()))
        scene.export(OUT/f'study/{state}.glb');states[state]=data
        bounds[state]=dict(xyz_mm=scene.extents.tolist(),min_mm=scene.bounds[0].tolist(),max_mm=scene.bounds[1].tolist(),status='provisional connected study incl pad envelopes; no human/harness/cable protection bounds')
    payload={'parameters':P,'parts':baseline,'states':states}
    (OUT/'study/connected_model.json').write_text(json.dumps(payload,separators=(',',':')))
    (OUT/'reports/solid_checks.json').write_text(json.dumps(solid_checks,indent=2))
    (OUT/'reports/bounds.json').write_text(json.dumps(bounds,indent=2))
    (OUT/'source/parameters.json').write_text(json.dumps(P,indent=2))
    print('Created',len(objects),'assembled study parts;',len(solid_checks),'valid new CAD solids')
    print('Travel XYZ',bounds['travel']['xyz_mm'])

if __name__=='__main__':build()
