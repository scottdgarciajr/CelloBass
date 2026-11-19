"""Run with portable Blender -b source.blend --python tools/inspect_blender.py.
Never saves or edits the source file. Exports evaluated meshes in native scene units.
"""
import bpy, json, sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/reports'
MESH = ROOT / 'output/source_meshes/native_units'
MESH.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
deps = bpy.context.evaluated_depsgraph_get()
objects = []
for ob in bpy.data.objects:
    entry = {'name': ob.name, 'type': ob.type, 'location': list(ob.location),
             'rotation': list(ob.rotation_euler), 'scale': list(ob.scale),
             'hidden': ob.hide_render, 'matrix_world': [list(row) for row in ob.matrix_world]}
    if ob.type == 'MESH':
        evaluated = ob.evaluated_get(deps)
        mesh = evaluated.to_mesh()
        vertices = [list(ob.matrix_world @ v.co) for v in mesh.vertices]
        mesh.calc_loop_triangles()
        faces = [list(t.vertices) for t in mesh.loop_triangles]
        mins = [min(v[i] for v in vertices) for i in range(3)]
        maxs = [max(v[i] for v in vertices) for i in range(3)]
        entry.update(bounds=[mins,maxs], dimensions=[b-a for a,b in zip(mins,maxs)],
                     vertices=len(vertices), triangles=len(faces), modifiers=[m.type for m in ob.modifiers])
        safe = ''.join(c if c.isalnum() or c in '-_' else '_' for c in ob.name)
        entry['mesh_file'] = str((MESH / (safe + '.json')).relative_to(ROOT)).replace('\\','/')
        (MESH / (safe + '.json')).write_text(json.dumps({'vertices': vertices, 'faces': faces}))
        evaluated.to_mesh_clear()
    objects.append(entry)
scene = bpy.context.scene
result = {'blender_version': bpy.app.version_string, 'source': Path(bpy.data.filepath).relative_to(ROOT).as_posix(),
          'units': {'system':scene.unit_settings.system, 'scale_length':scene.unit_settings.scale_length,
                    'length_unit':scene.unit_settings.length_unit}, 'objects':objects}
(OUT / 'blender_audit.json').write_text(json.dumps(result, indent=2))
print('CELLOBASS_AUDIT', json.dumps(result, indent=2))
