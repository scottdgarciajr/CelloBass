import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
scenes={s.name:s for s in bpy.data.scenes}
assert set(scenes)=={'CelloBass_cello','CelloBass_bass','CelloBass_transition','CelloBass_travel'}
objects={name:{o.data.name:o for o in s.objects if o.type=='MESH'} for name,s in scenes.items()}
base=objects['CelloBass_cello']
for state,items in objects.items():
    assert set(items)==set(base)
    for name,ob in items.items():assert ob.data==base[name].data
assert all(s.unit_settings.scale_length>.000999 and s.unit_settings.scale_length<.001001 for s in scenes.values())
(ROOT/'output/reports/native_assembly_check.json').write_text(json.dumps({'scenes':list(scenes),'linked_meshes_per_scene':len(base),'all_mesh_datablocks_shared':True,'unit_mm':True},indent=2))
print('Four native scenes share',len(base),'unchanged mesh datablocks; millimetres confirmed')
