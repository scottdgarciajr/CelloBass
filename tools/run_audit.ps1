$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    & .\.venv\Scripts\python.exe tools/audit_sources.py
    if ($LASTEXITCODE -ne 0) { throw 'Source audit failed' }
    $blenderExe = Join-Path $projectRoot 'tools/blender/blender-4.5.15-windows-x64/blender.exe'
    & $blenderExe --background --disable-autoexec work/source_unpacked/O-Cello/O-Cello_Source.blend --python tools/inspect_blender.py
    if ($LASTEXITCODE -ne 0) { throw 'Blender audit failed' }
    & .\.venv\Scripts\python.exe tools/audit_openbass.py
    if ($LASTEXITCODE -ne 0) { throw 'OpenBass audit failed' }
} finally { Pop-Location }
