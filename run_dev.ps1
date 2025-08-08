# Start the Python backend server in a new PowerShell window
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Python backend...'; cd python_backend; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --host 127.0.0.1 --port 8000"

# Start the Node.js frontend in a new PowerShell window
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "Write-Host 'Starting Node.js frontend...'; cd node_frontend; npm start"
