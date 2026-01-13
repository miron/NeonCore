
param(
    [switch]$Local
)

$ErrorActionPreference = "Stop"

$VenvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found at $VenvPython. Please set up the environment first."
    exit 1
}

if ($Local) {
    Write-Error "Local mode has been deprecated. Please run without -Local to start the server."
    exit 1
} else {
    Write-Host "Starting NeonCore Server & Client..."
    $ServerScript = Join-Path $PSScriptRoot "server.py"
    $ClientScript = Join-Path $PSScriptRoot "client.py"
    
    # Start server in background
    # using Start-Process to allow it to run asynchronously
    $ServerProcess = Start-Process -FilePath $VenvPython -ArgumentList "-m uvicorn server:app --port 8000 --log-level error" -PassThru -NoNewWindow
    
    try {
        # Give server a moment to spin up
        Start-Sleep -Seconds 2
        
        # Start client in current window
        & $VenvPython $ClientScript
    }
    finally {
        # Kill server when client exits or script aborts
        if ($ServerProcess -and -not $ServerProcess.HasExited) {
            Write-Host "Shutting down server..."
            Stop-Process -Id $ServerProcess.Id -Force
        }
    }
}
