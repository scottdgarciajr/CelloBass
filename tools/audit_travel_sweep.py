"""Run with Blender's Python to screen the modeled travel sweep for surface intersections."""
import json
import math
from pathlib import Path

from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


root = Path(__file__).resolve().parents[1]
model_dir = root / 'output/r03'
model = json.loads((model_dir / 'study/connected_model.json').read_text())
parts = model['parts']


def tree(part, rotation=None, shift=None):
    vertices = [Vector(point) for point in part['vertices']]
    if rotation is not None:
        pivot, matrix = rotation
        vertices = [pivot + matrix @ (point - pivot) for point in vertices]
    if shift is not None:
        vertices = [point + shift for point in vertices]
    return BVHTree.FromPolygons(vertices, part['faces'], all_triangles=True)


fixed = {part['name']: tree(part) for part in parts if part['motion'] == 'fixed'}
wing_parts = [part for part in parts if part['motion'] == 'wing']
locks = [part for part in parts if part['motion'] == 'lock']
hits = {}
for step in range(201):
    # Follow the existing travel viewer: pull out, turn, relocate, push in.
    t = step / 200
    fold = 90 * max(0, min(1, (t - .2) / .6))
    withdraw = t / .2 if t < .2 else 1 if t < .85 else (1 - t) / .15
    relocate = max(0, min(1, (t - .8) / .05))
    moving = []
    for part in wing_parts:
        side = part['side']
        hinge = Vector(model['parameters']['hinges'][str(side)])
        rotation = Matrix.Rotation(math.radians(-side * fold), 3, 'Y')
        moving.append((part, tree(part, rotation=(hinge, rotation))))
    for part in locks:
        shift = Vector((-part['side'] * 24 * relocate, -35 * withdraw, 24 * relocate))
        moving.append((part, tree(part, shift=shift)))
    for index, (part, mesh) in enumerate(moving):
        others = list(fixed.items())
        others.extend((other['name'], other_mesh) for other, other_mesh in moving[index+1:]
                      if other['side'] != part['side'] or other['motion'] != part['motion'])
        for name, other_mesh in others:
            # The local solid sweep checks deliberate tongue contact at its two end stops.
            if part['name'].startswith('hinged_tongue_') and name == f"clevis_base_{part['side']}":
                continue
            if mesh.overlap(other_mesh):
                hits.setdefault(f"{part['name']} / {name}", []).append(step / 2)

report = {
    'method': 'Surface intersection screen of the modeled travel animation at 201 positions',
    'overlaps_at_percent_of_animation': hits,
    'limits': 'Sampled triangle surfaces. Contact flags need interpretation. Excludes human, cable, tethers, tolerances, and loads.',
}
(model_dir / 'reports/travel_sweep_screen.json').write_text(json.dumps(report, indent=2))
for pair, samples in hits.items():
    print(f'{pair}: {len(samples)} positions from {samples[0]} to {samples[-1]} percent')
print(f'{len(hits)} flagged pairs in the travel sweep')
