# start-dev-environment.ps1
# This script sets up and starts the complete development environment.
# It assumes Python (with venv) and Node.js are in your PATH.

# --- Setup Python Virtual Environment ---
Write-Host "Setting up Python virtual environment..."
if (-not (Test-Path "python_backend\.venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv python_backend\.venv
}

Write-Host "Installing Python dependencies..."
$pipCommand = ".\python_backend\.venv\Scripts\python.exe -m pip install -r .\python_backend\requirements.txt"
Invoke-Expression $pipCommand

# --- Setup Node.js Dependencies ---
Write-Host "Installing Node.js dependencies..."
$npmCommand = "npm install --prefix .\node_frontend"
Invoke-Expression $npmCommand

# --- Start Backend and Frontend ---
Write-Host "Starting backend and frontend servers in new windows..."
# This reuses the logic from the now-fixed run_dev.ps1
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Python backend...'; cd python_backend; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --host 127.0.0.1 --port 8000"
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Node.js frontend...'; cd node_frontend; npm start"

Write-Host "Development environment setup is complete and servers are starting."