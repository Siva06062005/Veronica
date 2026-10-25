[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'VERONICA setup is intended for Windows.' }
foreach ($command in @('python', 'node', 'npm')) { if (-not (Get-Command $command -ErrorAction SilentlyContinue)) { throw "Missing required command: $command" } }
$root = $PSScriptRoot
$venv = Join-Path $root '.venv'
if (-not (Test-Path $venv)) { python -m venv $venv }
& (Join-Path $venv 'Scripts\python.exe') -m pip install --upgrade pip
& (Join-Path $venv 'Scripts\python.exe') -m pip install -r (Join-Path $root 'backend\requirements.txt')
Push-Location (Join-Path $root 'frontend')
npm install
Pop-Location
$envFile = Join-Path $root 'backend\.env'
if (-not (Test-Path $envFile)) { Copy-Item (Join-Path $root 'backend\.env.example') $envFile }
& (Join-Path $venv 'Scripts\python.exe') -c "import fastapi, psutil, sqlalchemy; print('Backend dependency check passed.')"
Write-Host 'VERONICA setup is complete. Configure backend\.env, then run .\start_veronica.ps1.' -ForegroundColor Green
