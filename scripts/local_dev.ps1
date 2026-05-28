Param(
    [switch]$NoRunserver,
    [string]$AddrPort = "127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

$ProjectDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$WorkspaceDir = (Resolve-Path (Join-Path $ProjectDir "..")).Path

$PythonCandidates = @(
    (Join-Path $ProjectDir ".venv\Scripts\python.exe"),
    (Join-Path $WorkspaceDir ".venv\Scripts\python.exe")
)

$Python = $null
foreach ($Candidate in $PythonCandidates) {
    if (Test-Path $Candidate) {
        $Python = $Candidate
        break
    }
}

Push-Location $ProjectDir
try {
    if (-not $Python) {
        if (Get-Command py -ErrorAction SilentlyContinue) {
            $Python = "py"
        } else {
            throw "Python not found. Expected .venv in '$ProjectDir' or '$WorkspaceDir', or 'py' on PATH."
        }
    }

    Write-Host "Using Python: $Python"

    Write-Host "[1/4] Sync carousel to local media..."
    & $Python .\scripts\sync_carousel_to_local_media.py

    Write-Host "[2/4] Migrate database..."
    & $Python .\manage.py migrate --noinput

    Write-Host "[3/4] Load sample data (fixtures)..."
    & $Python .\manage.py loaddata web/fixtures/sample_data.json

    if (-not $NoRunserver) {
        Write-Host "[4/4] Starting dev server at http://$AddrPort ..."
        & $Python .\manage.py runserver $AddrPort
    } else {
        Write-Host "Done (NoRunserver)."
    }
}
finally {
    Pop-Location
}
