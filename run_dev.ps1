param (
    [string]$ProjectRoot = ".." # Default to the parent directory of the script's location
)

# Resolve the absolute path for the project root
$ResolvedProjectRoot = (Resolve-Path -Path $ProjectRoot).Path

Write-Host "Using project root: $ResolvedProjectRoot"

# Start the Python backend server in a new PowerShell window
$backendCommand = "Write-Host 'Starting Python backend...'; cd python_backend; `$env:PROJECT_ROOT='$ResolvedProjectRoot'; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --host 127.0.0.1 --port 8000; Read-Host 'Press Enter to close this window...'"
Start-Process pwsh -ArgumentList "-NoExit", "-Command", $backendCommand

# Start the Node.js frontend in a new PowerShell window
$frontendCommand = "Write-Host 'Starting Node.js frontend...'; cd node_frontend; npm start; Read-Host 'Press Enter to close this window...'"
Start-Process pwsh -ArgumentList "-NoExit", "-Command", $frontendCommand
