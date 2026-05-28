Param(
  [switch]$NoCollectStatic
)

$ErrorActionPreference = 'Stop'

function Assert-Command([string]$Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $Name"
  }
}

Assert-Command python
Assert-Command docker

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot

try {
  Write-Host "==> Generating image thumbnails (carousel/iniciativas/obras)" -ForegroundColor Cyan
  python (Join-Path $PSScriptRoot 'make_site_thumbs.py')

  if (-not $NoCollectStatic) {
    Write-Host "==> Running Django collectstatic inside container" -ForegroundColor Cyan

    $containerId = (docker compose ps -q web)
    if (-not $containerId) {
      throw "No running 'web' service found. Start it first with: docker compose up -d"
    }

    docker compose exec web python manage.py collectstatic --noinput
  }

  Write-Host "Done." -ForegroundColor Green
  Write-Host "If images still look old, hard refresh the browser (Ctrl+F5)." -ForegroundColor DarkGray
  exit 0
}
finally {
  Pop-Location
}
