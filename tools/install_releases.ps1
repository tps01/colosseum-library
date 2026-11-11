# Create a .venv next to this script and pip-install local Colosseum release wheels.
# Expects wheels from download_releases.ps1 in the same folder. Uses `python` on PATH.

$ErrorActionPreference = 'Stop'

$Dir = $PSScriptRoot
$VenvPath = Join-Path $Dir '.venv'
$Wheels = @(Get-ChildItem -Path $Dir -Filter '*.whl' -File | Sort-Object Name)

if ($Wheels.Count -eq 0) {
    throw "No .whl files found in $Dir. Run download_releases.ps1 first."
}

$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    throw "'python' was not found on PATH."
}

if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment: $VenvPath"
    & python -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create virtual environment at $VenvPath."
    }
} else {
    Write-Host "Using existing virtual environment: $VenvPath"
}

$VenvPython = Join-Path $VenvPath 'Scripts\python.exe'
if (-not (Test-Path $VenvPython)) {
    throw "Virtual environment Python was not found: $VenvPython"
}

Write-Host "Upgrading pip ..."
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Failed to upgrade pip."
}

Write-Host "Installing $($Wheels.Count) wheel(s) from $Dir ..."
foreach ($wheel in $Wheels) {
    Write-Host "  $($wheel.Name)"
}
& $VenvPython -m pip install @($Wheels.FullName)
if ($LASTEXITCODE -ne 0) {
    throw "pip install failed."
}

$Vsix = @(Get-ChildItem -Path $Dir -Filter '*.vsix' -File)
if ($Vsix.Count -gt 0) {
    Write-Host "Note: $($Vsix.Count) .vsix file(s) were left for manual Cursor/VS Code install (not pip)."
}

Write-Host "Done. Activate with: & '$VenvPath\Scripts\Activate.ps1'"
