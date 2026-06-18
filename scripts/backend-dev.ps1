$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location "$root\backend"

python -m uvicorn app.main:app --reload