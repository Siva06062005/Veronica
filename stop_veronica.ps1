[CmdletBinding()]
param()
$ErrorActionPreference = 'Continue'
$pidFile = Join-Path $PSScriptRoot '.veronica-pids.json'
if (-not (Test-Path $pidFile)) { Write-Host 'No Veronica process record found.'; exit 0 }
$pids = Get-Content $pidFile | ConvertFrom-Json
foreach ($id in @($pids.backend, $pids.frontend)) { if ($id) { Stop-Process -Id $id -ErrorAction SilentlyContinue } }
Remove-Item -LiteralPath $pidFile
Write-Host 'VERONICA processes stopped.' -ForegroundColor Yellow
