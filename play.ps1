
$ErrorActionPreference = "Stop"

$VenvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
$GameScript = Join-Path $PSScriptRoot "run_game.py"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found at $VenvPython. Please set up the environment first."
    exit 1
}

# Run the game using the venv python directly, bypassing the need for explicit activation
& $VenvPython $GameScript @args
