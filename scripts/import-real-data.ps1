$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$csvPath = "$root\data\raw\ofertas_ti_chile_2026_06.csv"

Set-Location "$root\backend"


Write-Host "Validando e importando dataset real" -ForegroundColor Cyan

Write-Host "`n[1/3] Validando CSV..." -ForegroundColor Yellow
python -m app.scripts.validate_csv $csvPath

if ($LASTEXITCODE -ne 0) {
    throw "El CSV tiene errores. Corrige el archivo antes de importar."
}

Write-Host "`n[2/3] Reseteando base de datos..." -ForegroundColor Yellow
python -m app.scripts.reset_db

Write-Host "`n[3/3] Importando CSV real..." -ForegroundColor Yellow
python -m app.scripts.import_csv $csvPath --replace

Write-Host "`nDataset real importado correctamente." -ForegroundColor Green