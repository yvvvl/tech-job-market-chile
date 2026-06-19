$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host " BACKEND TESTS" -ForegroundColor Cyan

Write-Host "`n[1/4] Levantando PostgreSQL de tests..." -ForegroundColor Yellow
docker compose --profile test up -d postgres_test

Write-Host "`n[2/4] Esperando PostgreSQL de tests..." -ForegroundColor Yellow

$ready = $false

for ($i = 1; $i -le 30; $i++) {
    docker exec tech_jobs_postgres_test pg_isready -U techuser -d tech_jobs_chile_test | Out-Null

    if ($LASTEXITCODE -eq 0) {
        $ready = $true
        break
    }

    Start-Sleep -Seconds 1
}

if (-not $ready) {
    throw "PostgreSQL de tests no respondió a tiempo."
}

Write-Host "PostgreSQL de tests listo." -ForegroundColor Green

Write-Host "`n[3/4] Ejecutando checks backend..." -ForegroundColor Yellow
Set-Location "$root\backend"

$env:TEST_DATABASE_URL = "postgresql+psycopg2://techuser:techpass@localhost:5434/tech_jobs_chile_test"

ruff check . --fix
ruff format .
ruff check .

Write-Host "`n[4/4] Ejecutando pytest..." -ForegroundColor Yellow
python -m pytest

Write-Host "`nBackend tests completados." -ForegroundColor Green