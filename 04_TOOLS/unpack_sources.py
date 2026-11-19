"""Safely unpack the two supplied original source archives into work/source_unpacked."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "O-Cello_Source.zip": "O-Cello",
    "OpenBass_Original.zip": "OpenBass",
}

for filename, folder in SOURCES.items():
    path = ROOT / '02_ORIGINAL_PROJECTS' / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    out = ROOT / 'work' / 'source_unpacked' / folder
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'r') as z:
        for member in z.infolist():
            if member.is_dir():
                continue
            target = (out / member.filename).resolve()
            if not target.is_relative_to(out.resolve()):
                raise ValueError(f'Unsafe filename in archive: {member.filename}')
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(member) as reader, target.open('wb') as writer:
                while True:
                    chunk = reader.read(1024 * 1024)
                    if not chunk: break
                    writer.write(chunk)
    print(f"Extracted {filename} -> {out}")
