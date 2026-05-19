$ErrorActionPreference = "Stop"

python -m PyInstaller --clean --noconfirm Vireon.spec

Write-Host ""
Write-Host "Build complete: dist\Vireon.exe"
Write-Host "Keep MySQL running and make sure the vireon database exists before opening the app."
