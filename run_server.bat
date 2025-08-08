@echo off
cd python_backend
echo "Activating virtual environment..."
call .venv\Scripts\activate
echo "Starting server..."
uvicorn main:app --host 0.0.0.0 --port 8000
