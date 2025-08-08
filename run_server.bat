@echo off
set "PROJECT_ROOT=%1"
cd python_backend
echo "Activating virtual environment..."
call .venv\Scripts\activate
echo "Starting server for project at %PROJECT_ROOT%..."
uvicorn main:app --host 0.0.0.0 --port 8000
