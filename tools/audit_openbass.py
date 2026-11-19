from pathlib import Path
import json
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'work/source_unpacked/OpenBass/OpenBass V2.1/openbass-v21-v27.step'
assembly = cq.importers.importStep(str(path))
shape = assembly.val()
box = shape.BoundingBox()
result = {'source': path.relative_to(ROOT).as_posix(), 'unit': 'mm',
          'valid': shape.isValid(), 'solid_count': len(assembly.solids().vals()),
          'bounds': [[box.xmin,box.ymin,box.zmin],[box.xmax,box.ymax,box.zmax]],
          'dimensions': [box.xlen,box.ylen,box.zlen],
          'role': 'REFERENCE ONLY; no OpenBass geometry incorporated into CelloBass'}
(ROOT / 'output/reports/openbass_audit.json').write_text(json.dumps(result, indent=2))
for i, solid in enumerate(assembly.solids().vals()):
    cq.exporters.export(solid, str(ROOT / f'work/openbass_reference_{i}.stl'))
print(json.dumps(result))
