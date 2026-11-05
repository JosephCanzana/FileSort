$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot       # go to this script's own folder

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    if ($LASTEXITCODE -ne 0) { throw "Failed to install uv" }
}

$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"   # now always runs

uv tool install --python 3.12 --force .
if ($LASTEXITCODE -ne 0) { throw "Failed to install filesort" }

Write-Host "Installed! Open a new terminal and run: filesort"