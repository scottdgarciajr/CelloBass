"""Convert evaluated Blender geometry to mm; no repair, smoothing or scaling guesses."""
from pathlib import Path
import csv,json
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
audit=json.loads((OUT/'reports/blender_audit.json').read_text())
assert audit['units']['system']=='METRIC'
FACTOR=audit['units']['scale_length']*1000
meshes={};rows=[]
for ob in audit['objects']:
    if ob['type']!='MESH':continue
    raw=json.loads((ROOT/ob['mesh_file']).read_text())
    mesh=trimesh.Trimesh(vertices=np.array(raw['vertices'])*FACTOR,faces=raw['faces'],process=False)
    meshes[ob['name']]=mesh
    dest=OUT/'source_meshes/mm'/f"{Path(ob['mesh_file']).stem}.stl"
    dest.parent.mkdir(parents=True,exist_ok=True);mesh.export(dest)
    rows.append(dict(object=ob['name'],unit='mm',x_mm=mesh.extents[0],y_mm=mesh.extents[1],z_mm=mesh.extents[2],
                     xmin=mesh.bounds[0,0],ymin=mesh.bounds[0,1],zmin=mesh.bounds[0,2],
                     xmax=mesh.bounds[1,0],ymax=mesh.bounds[1,1],zmax=mesh.bounds[1,2],
                     watertight_as_supplied=mesh.is_watertight,triangles=len(mesh.faces)))
with (OUT/'reports/object_dimensions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
names=[f'Part {i}' for i in range(1,7)]+['Bridge','Center bar','Nameplate','Chest rest','Knee bar','Knee rest left','Knee rest right']
fig,axes=plt.subplots(1,2,figsize=(10,12),layout='constrained')
colors=plt.get_cmap('Set2')
for ax,dims,title in zip(axes,[(0,2),(1,2)],['Front: X / Z','Side: Y / Z']):
    for i,name in enumerate(names):
        m=meshes[name];poly=m.vertices[m.faces][:,:,dims]
        ax.add_collection(PolyCollection(poly,facecolor=colors(i%8),edgecolor='#26394c',linewidth=0.15,alpha=0.85))
        if name.startswith('Part') or name=='Bridge':
            center=m.bounds.mean(axis=0);ax.annotate(name,(center[dims[0]],center[dims[1]]),xytext=(50,0),textcoords='offset points',fontsize=8,arrowprops={'arrowstyle':'-','lw':0.5})
    ax.autoscale_view();ax.set_aspect('equal');ax.set_xlabel('mm');ax.set_ylabel('mm');ax.set_title(title);ax.grid(alpha=.15)
fig.suptitle("O'Cello supplied assembly | evaluated original meshes | millimetres\nLoose stand fittings and alternate left chest rest excluded",fontsize=13)
(OUT/'views').mkdir(exist_ok=True)
fig.savefig(OUT/'views/original_ocello_orthographic.png',dpi=160)
plt.close(fig)
print('Converted',len(meshes),'source objects using factor',FACTOR)
for name in ['Center bar','Bridge','Part 1']:
    m=meshes[name]
    print(name,'connected components',[(len(c.vertices),c.bounds.tolist()) for c in m.split(only_watertight=False)])
