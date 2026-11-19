from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output'
files=[]
for path in OUT.rglob('*'):
    if not path.is_file():continue
    rel=path.relative_to(OUT)
    if any(part in ['native_units','__pycache__'] for part in rel.parts):continue
    if path.suffix in ['.blend1','.pyc','.zip']:continue
    if path.name=='package_manifest.json':continue
    files.append(path)
extra=[ROOT/'README.md',ROOT/'01_DESIGN_BRIEF/SOURCE_NOTES_AND_LICENSES.md']
extra.extend(p for p in (ROOT/'tools').glob('*') if p.is_file() and p.suffix in ['.py','.ps1','.txt','.csv'])
files.extend(extra)
manifest=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p in sorted(files)]
(OUT/'reports/package_manifest.json').write_text(json.dumps(manifest,indent=2))
files.append(OUT/'reports/package_manifest.json')
revision='r03' if (OUT/'r03').exists() else 'r02'
target=ROOT/f'CelloBass_{revision}_Prototype_Package.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for path in sorted(files):archive.write(path,path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
print('Design ZIP',target.stat().st_size,'bytes;',len(files),'files')
print('Excludes tools binaries, Python environment, raw native-unit dumps and original archives.')
