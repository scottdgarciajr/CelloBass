"""Download an official portable Blender release, verify SHA256, unpack locally."""
from pathlib import Path
import hashlib
import requests
import zipfile

root = Path(__file__).resolve().parents[1]
version = '4.5.15'
base = 'https://mirror.blender.org/release/Blender4.5/'
filename = f'blender-{version}-windows-x64.zip'
target = root / 'tools/downloads' / filename
target.parent.mkdir(parents=True, exist_ok=True)
print('Downloading', base + filename, flush=True)
with requests.get(base + filename, stream=True, timeout=120) as response:
    response.raise_for_status()
    with target.open('wb') as stream:
        for chunk in response.iter_content(4 * 1024 * 1024):
            stream.write(chunk)
response = requests.get(base + f'blender-{version}.sha256', timeout=60)
response.raise_for_status()
checksums = response.text
expected = next(line.split()[0] for line in checksums.splitlines() if filename in line)
actual = hashlib.file_digest(target.open('rb'), 'sha256').hexdigest()
if actual.lower() != expected.lower():
    raise ValueError('Blender SHA256 mismatch')
(target.parent / f'blender-{version}.sha256').write_text(checksums)
print('SHA256 verified:', actual, flush=True)
with zipfile.ZipFile(target) as archive:
    archive.extractall(root / 'tools/blender')
print('Blender ready', flush=True)
