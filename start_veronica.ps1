[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { throw 'Virtual environment missing. Run .\setup.ps1 first.' }
if (-not (Test-Path (Join-Path $root 'frontend\node_modules'))) { throw 'Frontend dependencies missing. Run .\setup.ps1 first.' }
$pidFile = Join-Path $root '.veronica-pids.json'
if (Test-Path $pidFile) { throw 'VERONICA may already be running. Use .\stop_veronica.ps1 first.' }
$backend = Start-Process -FilePath $python -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8765' -WorkingDirectory (Join-Path $root 'backend') -WindowStyle Hidden -PassThru
$frontend = Start-Process -FilePath 'npm.cmd' -ArgumentList 'run','dev','--','--host','127.0.0.1' -WorkingDirectory (Join-Path $root 'frontend') -WindowStyle Hidden -PassThru
@{ backend = $backend.Id; frontend = $frontend.Id } | ConvertTo-Json | Set-Content -Path $pidFile -Encoding ASCII
Start-Sleep -Seconds 2
try { $health = Invoke-RestMethod 'http://127.0.0.1:8765/health'; Write-Host "VERONICA is running. HUD: http://127.0.0.1:5173  Backend: $($health.status)" -ForegroundColor Green } catch { Write-Warning 'Processes started, but the backend health check did not respond yet. Check backend logs by launching it manually.' }
