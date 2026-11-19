"""Create editable linked four-scene Blender kinematic assembly from measured source.
The STL/STEP coupon CAD remains the parametric source for new test mechanisms.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
states=json.loads((OUT/'context/states.json').read_text())
p=json.loads((OUT/'source/kinematic_parameters.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
meshes={}
colors={'original':(.69,.74,.80,1),'wing':(.035,.52,.48,1),'metal':(.17,.22,.29,1),'assumed':(.95,.55,.13,1)}
for item in states['cello']:
    mesh=bpy.data.meshes.new(item['name']);mesh.from_pydata(item['vertices'],[],item['faces']);mesh.update()
    meshes[item['name']]=(mesh,item['role'])

def rotate_y(angle,point):
    return Matrix.Translation(Vector(point)) @ Matrix.Rotation(math.radians(angle),4,'Y') @ Matrix.Translation(-Vector(point))

def line(scene,name,coords,color,radius=2):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=2
    spline=cu.splines.new('POLY');spline.points.add(len(coords)-1)
    for point,co in zip(spline.points,coords):point.co=(*co,1)
    ob=bpy.data.objects.new(name,cu);scene.collection.objects.link(ob);ob.color=color
    return ob

scenes=[]
for name,angle,fold in [('cello',0,0),('bass',-90,0),('transition',-45,0),('travel',0,90)]:
    scene=bpy.data.scenes.new('CelloBass_'+name)
    scenes.append(scene)
    scene['prototype_status']='ENVELOPE ONLY; unresolved live harness/metal attachment; NOT load-rated'
    scene['wing_fold_deg']=fold
    root=bpy.data.objects.new('SAME_ASSEMBLY_'+name,None);scene.collection.objects.link(root)
    root.matrix_world=rotate_y(angle,p['rotation_center_mm'])
    for obname,(mesh,role) in meshes.items():
        ob=bpy.data.objects.new(obname,mesh);scene.collection.objects.link(ob);ob.parent=root;ob.color=colors[role]
        ob['provenance']='O-Cello exact evaluated source mm' if role=='original' else 'PROVISIONAL original envelope, not production component'
        if obname.startswith('wing_') and fold:
            side=int(obname.split('_')[1]);ob.matrix_basis=rotate_y(-side*fold,[side*p['hinge_x_mm'],p['hinge_y_mm'],p['hinge_z_mm']])
    # Representative routing outside bow-side surface; not a solved human harness.
    if name!='travel':
        for i,anchor in enumerate(p['anchor_proposals_mm']):
            coords=[anchor,[-110,-190,300 if i==0 else 510],[-150,-230,430]]
            route=line(scene,f'HARNESS_ROUTING_PROPOSAL_{i}',coords,(.92,.56,.14,1),3)
            route.parent=root
        route=line(scene,'AUDIO_ROUTING_PROPOSAL',[[0,15,55],[-38,-30,45],[-55,-95,100],[-65,-110,180],[-120,-180,160]],(.35,.28,.62,1),1.7)
        route.parent=root
    # Orthographic 3/4 view with same scale for upright and folded views.
    center=Vector((0,-10,285))
    if name=='bass':center=Vector((-5,-10,280))
    camdata=bpy.data.cameras.new('Camera_'+name);cam=bpy.data.objects.new('Camera_'+name,camdata)
    scene.collection.objects.link(cam);cam.location=center+Vector((650,1800,600))
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO';camdata.ortho_scale=1240;camdata.clip_end=10000;scene.camera=cam
    scene.render.engine='BLENDER_WORKBENCH'
    scene.display.shading.light='STUDIO';scene.display.shading.studiolight_rotate_z=.5
    scene.display.shading.color_type='OBJECT';scene.display.shading.show_shadows=True
    scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
    scene.display.shading.show_object_outline=True
    scene.display.shading.background_type='WORLD';scene.world=bpy.data.worlds.new('White_'+name)
    scene.world.color=(.94,.96,.98)
    scene.render.resolution_x=1300;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001;scene.unit_settings.length_unit='MILLIMETERS'
    scene.render.filepath=str(OUT/f'views/{name}_study.png')
    bpy.context.window.scene=scene
    bpy.ops.render.render(write_still=True,scene=scene.name)
for scene in list(bpy.data.scenes):
    if scene not in scenes:bpy.data.scenes.remove(scene)
bpy.context.window.scene=scenes[0]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CelloBass_r02_kinematic_study.blend'))
print('SAVED editable four-scene linked assembly')
