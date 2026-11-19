import bpy,json,math
from pathlib import Path
from mathutils import Vector,Matrix

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/r03'
data=json.loads((OUT/'study/connected_model.json').read_text());p=data['parameters']
bpy.ops.wm.read_factory_settings(use_empty=True)
palette={'core':(.66,.72,.79,1),'frame':(.025,.50,.45,1),'pad':(.09,.12,.15,1),
         'metal':(.30,.39,.50,1),'joint':(.06,.31,.36,1),'pin':(.74,.61,.31,1),'lock':(1,.38,.06,1),'strings':(.36,.34,.30,1)}
meshes={}
for ob in data['parts']:
    mesh=bpy.data.meshes.new(ob['name']);mesh.from_pydata(ob['vertices'],[],ob['faces']);mesh.update();meshes[ob['name']]=mesh
def ry(deg,point):return Matrix.Translation(Vector(point))@Matrix.Rotation(math.radians(deg),4,'Y')@Matrix.Translation(-Vector(point))
scenes=[]
specs=[('cello',0,0),('bass',-70,0),('transition',-35,0),('travel',0,90),('hinge_detail',0,0)]
for name,angle,fold in specs:
    scene=bpy.data.scenes.new('CelloBass_r03_'+name);scenes.append(scene)
    scene['status']='CONNECTED DESIGN STUDY; structural retention, load and ergonomics NOT TESTED'
    root=bpy.data.objects.new('rigid_assembly_'+name,None);scene.collection.objects.link(root);root.matrix_world=ry(angle,p['rotation_center_mm'])
    for part in data['parts']:
        ob=bpy.data.objects.new(part['name'],meshes[part['name']]);scene.collection.objects.link(ob);ob.parent=root;ob.color=palette[part['role']]
        ob['motion']=part['motion'];ob['side']=part['side']
        ob['status']='Original source surface' if part['role']=='core' else 'PROPOSED geometry; not a production part'
        if part['motion']=='wing':ob.matrix_basis=ry(-part['side']*fold,p['hinges'][str(part['side'])])
        if part['motion']=='lock' and fold:ob.location=(-part['side']*24,0,24)
    center=Vector((0,-30,280));scale=1250
    if name=='hinge_detail':center=Vector((100,-75,155));scale=240
    camdata=bpy.data.cameras.new('Camera_'+name);cam=bpy.data.objects.new('Camera_'+name,camdata);scene.collection.objects.link(cam)
    offset=Vector((650,1800,600)) if name!='hinge_detail' else Vector((650,-1800,600))
    cam.location=center+offset;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO';camdata.ortho_scale=scale;camdata.clip_end=10000;scene.camera=cam
    scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT'
    scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.show_object_outline=True
    scene.display.shading.background_type='WORLD';scene.world=bpy.data.worlds.new(name);scene.world.color=(.94,.96,.98)
    scene.render.resolution_x=1400;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
    scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'
    scene.render.filepath=str(OUT/f'views/{name}.png');scene.render.image_settings.file_format='PNG'
    bpy.context.window.scene=scene;bpy.ops.render.render(write_still=True,scene=scene.name)
for s in list(bpy.data.scenes):
    if s not in scenes:bpy.data.scenes.remove(s)
bpy.context.window.scene=scenes[1]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CelloBass_r03_connected_study.blend'))
print('Saved linked connected-study assembly, five scenes')
