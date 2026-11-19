from pathlib import Path
import csv,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
fontpath='C:/Windows/Fonts/segoeui.ttf'
font=ImageFont.truetype(fontpath,28);small=ImageFont.truetype(fontpath,20)
canvas=Image.new('RGB',(1600,1540),'#f3f6f8');d=ImageDraw.Draw(canvas)
d.text((36,20),'CelloBass V2 | source-measured prototype study',font=font,fill='#163249')
d.text((36,60),'Gray: original core  |  Teal: wing envelopes  |  Gold: assumed stow/support routing',font=small,fill='#3c596c')
labels=[('cello','CELLO: deployed wings'),('bass','BASS: same deployed wings'),('transition','TRANSITION: whole assembly rotates'),('travel','TRAVEL: wings fold; full length retained')]
for i,(state,label) in enumerate(labels):
    x=20+(i%2)*800;y=110+(i//2)*680
    im=Image.open(OUT/f'views/{state}_study.png').convert('RGB');im.thumbnail((760,620))
    canvas.paste(im,(x+(760-im.width)//2,y))
    d.text((x+15,y+625),label,font=small,fill='#163249')
d.text((36,1480),'ENVELOPE STUDY: harness/load path unresolved; NOT a production or tension-ready instrument.',font=small,fill='#8c431c')
canvas.save(OUT/'views/CelloBass_four_states.png')

# Coupon thumbnails in an axonometric, dimension-labelled sheet.
fig,axes=plt.subplots(2,5,figsize=(16,6.5),layout='constrained')
rows=list(csv.DictReader((OUT/'reports/coupon_checks.csv').open()))
for ax,row in zip(axes.flat,rows):
    mesh=trimesh.load_mesh(OUT/f'stl/coupons/{row["part"]}.stl');v=mesh.vertices
    u=.87*v[:,0]-.50*v[:,1];w=.25*v[:,0]+.43*v[:,1]+.87*v[:,2]
    projection=np.column_stack([u,w]);face=projection[mesh.faces]
    depth=-.43*v[:,0]-.75*v[:,1]+.5*v[:,2]
    order=np.argsort(depth[mesh.faces].mean(axis=1))
    ax.add_collection(PolyCollection(face[order],facecolor='#44a5a1',edgecolor='#205956',linewidth=.25))
    ax.autoscale_view();ax.set_aspect('equal');ax.axis('off')
    title=row['part'].replace('_','\n',1)
    ax.set_title(title,fontsize=9)
    ax.text(.5,-.05,f'{float(row["x_mm"]):.1f} x {float(row["y_mm"]):.1f} x {float(row["z_mm"]):.1f} mm',transform=ax.transAxes,ha='center',fontsize=8)
fig.suptitle('10 isolated bench coupons | STL + editable CadQuery + STEP | NOT load-rated',fontsize=15)
fig.savefig(OUT/'views/coupon_contact_sheet.png',dpi=160);plt.close(fig)

# Original OpenBass assembly, direct STEP tessellations, reference-only view.
fig,axes=plt.subplots(1,2,figsize=(8,11),layout='constrained')
for ax,dims,title in zip(axes,[(0,1),(2,1)],['Front X / Y','Side Z / Y']):
    for i,path in enumerate(sorted((ROOT/'work').glob('openbass_reference_*.stl'))):
        m=trimesh.load_mesh(path);polys=m.triangles[:,:,dims]
        ax.add_collection(PolyCollection(polys,facecolor=plt.get_cmap('Set2')(i),edgecolor='#365366',linewidth=.07))
    ax.autoscale_view();ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_title(title);ax.set_xlabel('mm');ax.set_ylabel('mm')
fig.suptitle('OpenBass V2.1 | actual STEP source assembly\nConstruction reference only; no geometry incorporated',fontsize=13)
fig.savefig(OUT/'views/original_openbass_orthographic.png',dpi=160);plt.close(fig)

state_data=(OUT/'context/states.json').read_text()
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CelloBass V2 — prototype review</title><style>
*{box-sizing:border-box}body{margin:0;background:#edf3f5;color:#163249;font:16px/1.5 system-ui,sans-serif}main{max-width:1250px;margin:auto;padding:28px}h1{font-size:34px;letter-spacing:-1px;margin:0}p{max-width:920px}header p{color:#526f7d;margin:8px 0 22px}.status{background:#fff0df;border-left:4px solid #bf7830;padding:12px 16px;margin-bottom:20px}a{color:#086b72}nav{display:flex;gap:8px;flex-wrap:wrap}button{border:1px solid #acbdc6;background:white;border-radius:6px;padding:9px 16px;color:#163249;cursor:pointer;font:inherit}button.active{background:#136b70;color:white;border-color:#136b70}.panel{background:white;border:1px solid #cfdee3;border-radius:12px;overflow:hidden}canvas{width:100%;height:560px;display:block;touch-action:none;background:linear-gradient(#f9fbfc,#e6eff2)}.tools{padding:14px;display:flex;gap:20px;align-items:center;flex-wrap:wrap}.caption{padding:12px 20px;border-top:1px solid #dfE8ec;color:#526f7d}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:24px 0}.card{padding:20px;background:white;border-radius:10px;border:1px solid #cfdee3}.card h2{margin:0 0 10px;font-size:20px}img{display:block;width:100%;height:auto}li{margin:7px 0}footer{font-size:13px;color:#526f7d;margin-top:24px}@media(max-width:700px){.grid{grid-template-columns:1fr}main{padding:16px}canvas{height:430px}}
</style></head><body><main><header><h1>CelloBass V2</h1><p>Measured original cello geometry, four assembly states, and printable mechanism tests. Revision 0.2 • 10 November 2026.</p></header>
<div class="status"><strong>Prototype review — production release held.</strong> Rotating harness, positive metal-to-spine load path, full bow clearance and physical strength remain unverified. The wings shown are envelopes; print only the isolated bench coupons.</div>
<section class="panel"><div class="tools"><nav id="states"><button data-state="cello" class="active">Cello</button><button data-state="bass">Bass</button><button data-state="transition">Transition</button><button data-state="travel">Travel</button></nav><label>View <input id="view" type="range" min="-80" max="80" value="20"></label><button id="reset">Reset view</button></div><canvas id="cad" aria-label="Interactive view of actual source meshes and provisional wings"></canvas><div class="caption" id="caption"></div></section>
<div class="grid"><article class="card"><h2>Editable files</h2><ul><li><a href="CelloBass_r02_kinematic_study.blend">Open the four-scene Blender assembly</a></li><li><a href="source/build_coupons.py">Parametric coupon CAD source</a></li><li><a href="source/build_kinematics.py">Parametric wing / state study source</a></li><li><a href="step/hinge_bench_assembly.step">Bench hinge assembly STEP</a></li><li><a href="PRINT_AND_ASSEMBLE_COUPONS.md">Coupon printing and bench assembly instructions</a></li></ul></article>
<article class="card"><h2>Measured, assumed, untested</h2><p>Live model: <strong>1,070 × 420 × 148 mm</strong>.<br>Folded model: <strong>1,070 × 187 × 148 mm</strong>.</p><p>These partial-model dimensions exclude real tuner hardware, locks, harness and padding. The core stays full length.</p><a href="reports/verification.md">Read checks, limitations and next test gate</a></article></div>
<section class="card"><h2>Bench coupons</h2><img src="views/coupon_contact_sheet.png" alt="Ten isolated fit coupons with dimensions"><p><a href="stl/coupons/">STL coupon folder</a> · <a href="step/coupons/">STEP coupon folder</a> · <a href="reports/coupon_checks.csv">Dimensions and mesh checks</a></p></section>
<div class="grid"><article class="card"><h2>Original O’Cello</h2><img src="views/original_ocello_orthographic.png" alt="Original O'Cello assembly front and side"><a href="reports/source_inventory.md">Source audit and attribution</a></article><article class="card"><h2>Original bridge and nut</h2><img src="views/musical_geometry_detail.png" alt="Original asymmetric bridge and original nut geometry"><p>Original surfaces are preserved. Exact speaking length and installed string contact points still require assignment.</p><a href="ELECTRONICS_AND_TRANSITION.md">Audio and performance transition plan</a></article></div>
<footer>O’Cello: Conor O’Kane, CC BY-NC 4.0. OpenBass: tbenen, CC BY-SA 4.0, construction reference only. No OpenBass geometry is incorporated. New geometry is an untested independent prototype.</footer></main><script>
const states=__STATES__;
const canvas=document.getElementById('cad'),ctx=canvas.getContext('2d');let state='cello',yaw=20,tilt=12,zoom=1;
const palette={original:[183,199,211],wing:[26,155,146],metal:[70,91,114],assumed:[225,161,62]};
const notes={cello:'Upright: same rigid core, wings deployed. Support/harness absent from this mesh viewer; see Blender routing sketches.',bass:'Horizontal: exactly the same deployed assembly after a global rotation. No wing adjustment or bridge movement.',transition:'45° orientation study. Human, bow, straps and cable sweeps remain NOT TESTED.',travel:'Only wings fold. The original chest rest and full-length reinforced core stay fixed. Model length remains 1,070 mm.'};
function render(){const dpr=window.devicePixelRatio||1,w=canvas.clientWidth,h=canvas.clientHeight;canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);let a=yaw*Math.PI/180,t=tilt*Math.PI/180,ca=Math.cos(a),sa=Math.sin(a),ct=Math.cos(t),st=Math.sin(t),scale=Math.min(w/1250,h/1200)*zoom;
let faces=[];for(const ob of states[state]){let v=ob.vertices.map(p=>{let x=p[0],y=p[1]+30,z=p[2]-285,u=x*ca-y*sa,d=x*sa+y*ca;return [w/2+u*scale,h/2-(z*ct-d*st)*scale,z*st+d*ct]});for(const f of ob.faces){let p=v[f[0]],q=v[f[1]],r=v[f[2]],area=(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]);if(Math.abs(area)<.015)continue;let b=palette[ob.role],shade=area<0?.80:1;faces.push({p,q,r,depth:(p[2]+q[2]+r[2])/3,color:`rgb(${b.map(n=>Math.round(n*shade)).join(',')})`})}}
faces.sort((a,b)=>a.depth-b.depth);for(const f of faces){ctx.beginPath();ctx.moveTo(f.p[0],f.p[1]);ctx.lineTo(f.q[0],f.q[1]);ctx.lineTo(f.r[0],f.r[1]);ctx.closePath();ctx.fillStyle=f.color;ctx.fill();ctx.strokeStyle=f.color;ctx.lineWidth=.35;ctx.stroke()}ctx.fillStyle='#526f7d';ctx.font='13px system-ui';ctx.fillText('Drag to orbit · Scroll to zoom · Gray source / teal envelopes',18,h-18);document.getElementById('caption').textContent=notes[state]}
document.querySelectorAll('[data-state]').forEach(b=>b.onclick=()=>{state=b.dataset.state;document.querySelectorAll('[data-state]').forEach(x=>x.classList.toggle('active',x===b));render()});document.getElementById('view').oninput=e=>{yaw=Number(e.target.value);render()};document.getElementById('reset').onclick=()=>{yaw=20;tilt=12;zoom=1;document.getElementById('view').value=20;render()};let drag=null;canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)};canvas.onpointerup=()=>drag=null;canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.25;tilt=Math.max(-65,Math.min(65,tilt+(e.clientY-drag[1])*.2));drag=[e.clientX,e.clientY];render()};canvas.onwheel=e=>{e.preventDefault();zoom=Math.max(.4,Math.min(2,zoom*Math.exp(-e.deltaY*.001)));render()};window.onresize=render;render();
</script></body></html>'''
(OUT/'CelloBass_Review.html').write_text(html.replace('__STATES__',state_data),encoding='utf-8')
print('Preview, contact sheet, source reference views and local interactive review created')
