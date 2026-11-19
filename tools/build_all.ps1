$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location -LiteralPath $projectRoot
function Invoke-CheckedPython([string]$scriptPath) {
    & .\.venv\Scripts\python.exe $scriptPath
    if ($LASTEXITCODE -ne 0) { throw "Failed: $scriptPath" }
}
try {
    & ./tools/run_audit.ps1
    Invoke-CheckedPython 'tools/measure_source.py'
    Invoke-CheckedPython 'output/source/build_coupons.py'
    Invoke-CheckedPython 'output/source/build_kinematics.py'
    Invoke-CheckedPython 'tools/engineering_reports.py'
    Invoke-CheckedPython 'tools/check_project.py'
    $blenderExe = Join-Path $projectRoot 'tools/blender/blender-4.5.15-windows-x64/blender.exe'
    & $blenderExe --background --factory-startup --python tools/make_blender_assembly.py
    if ($LASTEXITCODE -ne 0) { throw 'Assembly creation failed' }
    & $blenderExe --background output/CelloBass_r02_kinematic_study.blend --python tools/check_blender_assembly.py
    if ($LASTEXITCODE -ne 0) { throw 'Native assembly check failed' }
    Invoke-CheckedPython 'tools/make_preview.py'
    if (Test-Path -LiteralPath 'output/r03/source/build_connected_study.py') {
        Invoke-CheckedPython 'output/r03/source/build_connected_study.py'
        Invoke-CheckedPython 'tools/check_connected_study.py'
        & $blenderExe --background --factory-startup --python-exit-code 1 --python tools/audit_travel_sweep.py
        if ($LASTEXITCODE -ne 0) { throw 'Travel sweep audit failed' }
        & $blenderExe --background --factory-startup --python tools/make_connected_blender.py
        if ($LASTEXITCODE -ne 0) { throw 'Connected study creation failed' }
        Invoke-CheckedPython 'tools/build_connected_review.py'
    }
} finally { Pop-Location }
