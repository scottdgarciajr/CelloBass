from pathlib import Path
import json,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output';NEW=OUT/'r03'
model=json.loads((NEW/'study/connected_model.json').read_text())
data={'parameters':model['parameters'],'parts':model['parts']}
template=(NEW/'source/review_template.html').read_text(encoding='utf-8')
backup=OUT/'CelloBass_r02_Review.html'
if not backup.exists():shutil.copyfile(OUT/'CelloBass_Review.html',backup)
(OUT/'CelloBass_Review.html').write_text(template.replace('__MODEL__',json.dumps(data,separators=(',',':'))),encoding='utf-8')
print('Updated main review: connected seated-bass design and live/travel animations')
