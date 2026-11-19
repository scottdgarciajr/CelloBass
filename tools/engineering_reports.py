"""Reproducible measurements and transparent mass/torque estimates, never certification."""
from pathlib import Path
import csv,json,math
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
audit=json.loads((OUT/'reports/blender_audit.json').read_text())
obs={o['name']:o for o in audit['objects']}
rows=[]
def row(item,value,unit,status,provenance,notes=''):
    rows.append(dict(item=item,value=value,unit=unit,status=status,provenance=provenance,notes=notes))
row('Blender scale conversion',1000,'mm per scene unit','MEASURED','scene.unit_settings METRIC, scale_length=1.0','Length display METERS; evaluated matrix_world applied before conversion')
for name in ['Bridge','Center bar','Part 1','Part 2','Part 3','Part 4','Part 5','Part 6','Chest rest','Knee bar','Knee rest left','Knee rest right']:
    for axis,value in zip('XYZ',obs[name]['dimensions']):
        row(f'{name} {axis} extent',round(value*1000,5),'mm','MEASURED',f'Blender evaluated {name} world mesh','Envelope; not automatically a functional mating dimension')
row('Rod nominal diameter',12,'mm','DOCUMENTED','Official O-Cello assembly guide page 1','Not independently caliper measured')
row('Rod nominal length',1000,'mm','DOCUMENTED','Official O-Cello assembly guide page 1','Source Center bar Z extent is about 1000; modeled cap-to-cap axis is slightly different')
row('Modeled bar maximum X width',12.2000007,'mm','MEASURED','Center bar evaluated bounds','12.2 model versus 12 nominal hardware; do not silently shrink source')
core=[obs[f'Part {i}']['bounds'] for i in range(1,7)]
row('Six printed core sections longitudinal envelope',round((max(b[1][2] for b in core)-min(b[0][2] for b in core))*1000,4),'mm','MEASURED','Parts 1-6 evaluated mesh','Excludes rod extension, supports, tuner hardware and endpin')
row('Effective speaking scale','','mm','UNRESOLVED','Nut ridge and bridge mesh preserved','Four string contact points and actual string diameters not assigned; do not manufacture a nominal replacement fingerboard')
nut_min=747.4924;nut_max=749.4467
br_min=obs['Bridge']['bounds'][0][2]*1000;br_max=obs['Bridge']['bounds'][1][2]*1000
row('Nut to bridge longitudinal contact bounding window',f'{nut_min-br_max:.3f} to {nut_max-br_min:.3f}','mm Z separation','MEASURED_BOUNDS_ONLY','Part 1 nut ridge vertices Z 747.4924..749.4467; full Bridge bounds','Not effective scale or a calibrated string contact measurement')
row('Nut outer groove nominal center spread','','mm','UNRESOLVED','Part 1 original notches','Approximate notch regions X +/-11.5..12.2; exact bearing points require assignment')
row('Bridge outer groove valley vertex spread',round(23.42573-(-23.81472),5),'mm X projected','MEASURED_VERTEX_PROXY','Bridge groove valley vertices listed in bridge_contact_candidates.json','Projected source-vertex spread only; not certified string-center spacing')
row('Bridge arch radius','','mm','UNRESOLVED','Bridge supplied asymmetric mesh','Do not replace with a fitted symmetric radius; full curve preserved')
row('Original neck/fingerboard profile','','','PRESERVED_MESH','Part 1-4 evaluated original meshes','No reconstructed parametric profile claimed; extents in object_dimensions.csv')
row('String anchor / tailpiece dimensions','','mm','UNRESOLVED','Part 1 rear anchor region; guide page 13','Source uses rear string anchoring, not a separate modeled conventional tailpiece')
row('Tuning key mounting pattern','','mm','UNRESOLVED','Part 6 tuner bores; guide pages 9-10','Actual purchased key shafts, screws and buttons absent; source interface retained')
row('Endpin tube diameter / length','10 / 450','mm','DOCUMENTED','Official guide pages 1,14','Tube absent from .blend; modeled stow tube is an assumption with assumed 1mm wall')
row('Existing part joins','','mm','UNRESOLVED_INTERFACE','Overlapping Parts 1-6; M5 hardware documented','Bounds include tongues; do not treat Z bounds as joint planes')
row('Reinforced harness interfaces','','mm','PROPOSAL_NOT_VALIDATED','Kinematic anchors (-40,-50,180),(-40,-50,460)','New metal rail envelope; positive metal-to-rod retention unresolved; no attachment in printed wing')
state=json.loads((OUT/'reports/state_bounds.json').read_text())
for mode in ['cello','travel']:
    row(f'{mode} study L x W x D',' x '.join(f'{state[mode]["xyz_mm"][i]:.3f}' for i in [2,0,1]),'mm','MEASURED_PARTIAL_MODEL','state_bounds.json','Excludes actual tuners, strap hardware, locks, protective shell and padding')
with (OUT/'reports/source_dimensions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
candidates=[[-23.81472,25.12385,52.25145],[-8.02448,30.73357,52.1927],[8.1719,31.81029,52.1833],[23.42573,27.28815,52.23201]]
(OUT/'reports/bridge_contact_candidates.json').write_text(json.dumps({'unit':'mm','status':'source groove valley vertices ONLY; not assigned string center/contact points','points':candidates},indent=2))

# Source detail plots preserve the actual asymmetry, showing both thickness faces.
fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
for ax,name in zip(axes,['Bridge','Part_1']):
    m=trimesh.load_mesh(OUT/f'source_meshes/mm/{name}.stl')
    face=m.triangles
    if name=='Part_1':face=face[(face[:,:,2].min(axis=1)>746)&(face[:,:,2].max(axis=1)<751)]
    ax.add_collection(PolyCollection(face[:,:,:2],facecolor='#c8dfdf',edgecolor='#426675',linewidth=.4))
    ax.autoscale_view();ax.set_aspect('equal');ax.set_xlabel('X mm');ax.set_ylabel('Y mm (front)');ax.grid(alpha=.15)
    ax.set_title('Original asymmetric bridge' if name=='Bridge' else 'Original nut ridge / notch mesh')
fig.suptitle('Source geometry preserved | groove contact assignment remains unresolved',fontsize=13)
fig.savefig(OUT/'views/musical_geometry_detail.png',dpi=170);plt.close(fig)

# Mass budget: effective printed-material fraction is a sensitivity assumption, NOT infill setting.
params=json.loads((OUT/'source/kinematic_parameters.json').read_text())
budget=[]
core_names=[f'Part_{i}' for i in range(1,7)]+['Bridge','Nameplate','Chest_rest']
for name in core_names:
    m=trimesh.load_mesh(OUT/f'source_meshes/mm/{name}.stl')
    mass=m.volume*1.27e-6*.35
    budget.append({'part':name,'mass_kg':mass,'center_mm':m.center_mass.tolist(),'basis':'PETG 1.27 g/cm3, effective volume fraction 0.35 ASSUMED'})
for name,mass,center,basis in [
    ('Steel rod',math.pi*6**2*1000*7.85e-6,[0,7.8,251.8],'12mm x 1000mm solid steel; nominal BOM'),
    ('Rear rail',25*10*680*2.70e-6,[-40,-50,150],'25x10x680 solid aluminum ENVELOPE assumption'),
    ('Endpin tube',math.pi*(5**2-4**2)*450*2.70e-6,[27,-55,65],'10mm OD, 1mm wall, 450mm aluminum ASSUMED'),
    ('Tuners and fasteners',.45,[0,-10,-25],'ASSUMED lumped mass; actual hardware not supplied'),
    ('Pickup jack wire locks',.15,[-10,-50,150],'ASSUMED lumped mass'),
    ('Wings and hinge hardware',.22,[0,-75,165],'ASSUMED pair total; coupon geometry not integrated'),
]:budget.append({'part':name,'mass_kg':mass,'center_mm':center,'basis':basis})
total=sum(b['mass_kg'] for b in budget)
com=sum((b['mass_kg']*np.array(b['center_mm']) for b in budget),np.zeros(3))/total
pivot=np.array(params['rotation_center_mm']);lever=np.linalg.norm((com-pivot)[[0,2]])/1000
torque=total*9.80665*lever
estimate={'status':'PRELIMINARY ASSUMED MATERIALS/MASSES; NOT TESTED', 'mass_kg':total,'center_mm':com.tolist(),
          'rotation_center_mm':pivot.tolist(),'max_gravity_torque_about_Y_Nm':torque,
          'assumed_anchor_spacing_mm':280,'force_couple_at_280mm_N':torque/.28,
          'sensitivity_mass_range_kg':[2.5,5], 'sensitivity_horizontal_lever_mm':[100,300],
          'sensitivity_max_torque_Nm':5*9.80665*.3,
          'limitations':'Does not calculate rod stress, connection strength, dynamic loads, strap tensions, harness stiffness, player dimensions or bearing pressure',
          'budget':budget}
(OUT/'reports/mass_balance.json').write_text(json.dumps(estimate,indent=2))
print('Assumed mass',total,'COM',com,'max gravity torque',torque)
