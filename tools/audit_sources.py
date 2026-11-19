"""Inventory immutable input archives and extract supplied reference text."""
from pathlib import Path
import csv, hashlib, json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/reports'
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for parent in ['02_ORIGINAL_PROJECTS', 'work/source_unpacked']:
    for path in sorted((ROOT / parent).rglob('*')):
        if path.is_file():
            rows.append(dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size,
                             sha256=hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()))
lock = ROOT / 'tools/source_hashes.lock.csv'
if lock.exists():
    expected = {r['path']:r['sha256'] for r in csv.DictReader(lock.open())}
    actual = {r['path']:r['sha256'] for r in rows}
    if expected != actual:
        raise ValueError('Original source inventory differs from locked first-audit hashes')
with (OUT / 'source_files.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, rows[0].keys()); writer.writeheader(); writer.writerows(rows)
for path in (ROOT / 'work/source_unpacked').rglob('*.pdf'):
    reader = PdfReader(path)
    text = '\n\n'.join(f'PAGE {i+1}\n{page.extract_text()}' for i, page in enumerate(reader.pages))
    (OUT / 'openbass_reference_text.txt').write_text(text, encoding='utf-8')
print(json.dumps({'files': len(rows), 'blend_header': (ROOT/'work/source_unpacked/O-Cello/O-Cello_Source.blend').read_bytes()[:12].decode(errors='replace')}))
