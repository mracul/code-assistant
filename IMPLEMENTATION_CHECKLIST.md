# Implementation Checklist

## Phase 1: The Back-End "Brain" - The Python AI Service
- [ ] **1.1 Project Setup (Python):** Create a `python_backend` directory, set up a Python virtual environment, and initialize a git repository for the whole project.
- [ ] **1.2 Install Core Dependencies:** Install `fastapi` and `uvicorn`.
- [ ] **1.3 Create the API Server:** In `python_backend/main.py`, create a basic FastAPI app.
- [ ] **1.4 Build a "Ping" Endpoint:** Create a simple API endpoint at `/api/v1/ping` that returns `{"status": "ok"}`.
- [ ] **1.5 Test the Endpoint:** Access `http://localhost:8000/api/v1/ping` and verify the JSON response.

## Phase 2: The Front-End "Face" - The Node.js TUI
- [ ] **2.1 Project Setup (Node.js):** Create a `node_frontend` directory and run `npm init`.
- [ ] **2.2 Install Core Dependencies:** Install `ink`, `react`, and `axios`.
- [ ] **2.3 Build the Basic TUI:** In `node_frontend/cli.js`, create a basic Ink application with a header, a log area, and an input box.
- [ ] **2.4 Implement the REPL:** Implement the core Read-Eval-Print Loop.
- [ ] **2.5 Connect to the Backend:** Use `axios` to make a GET request to the Python server's `/api/v1/ping` endpoint.

## Phase 3: Building the Context Engine (Python Backend)
- [ ] **3.1 File System Scanner:** Implement a function that scans a given directory for source code files.
- [ ] **3.2 SQLite Caching Layer:** Set up a local SQLite database (`.context_cache.db`).
- [ ] **3.3 AST-Based Parser:** Create a `ContextBuilder` service to parse a Python file's content into an AST.
- [ ] **3.4 New Context Endpoint:** Create a new API endpoint, `POST /api/v1/analyze`.

## Phase 4: Implementing the Agentic Workflow (Python Backend)
- [ ] **4.1 Agent Registry:** Create the `agents.json` file and a Python class to manage agent definitions.
- [ ] **4.2 Agent Executor Service:** Create a generic function to execute any agent from the registry.
- [ ] **4.3 Orchestrator Class:** Build the `Orchestrator` class in Python.
- [ ] **4.4 New Workflow Endpoint:** Create the main endpoint, `POST /api/v1/execute-workflow`.

## Phase 5: Closing the Loop (Node.js Frontend)
- [ ] **5.1 Connect to Workflow Endpoint:** Update the Node.js app to call the new `/api/v1/execute-workflow` endpoint.
- [ ] **5.2 Implement Status Updates:** Stream status updates from the Python service to the TUI.
- [ ] **5.3 Display Code Diffs:** Render a color-coded diff in the TUI.
- [ ] **5.4 User Confirmation & File I/O:** Prompt the user for confirmation and write changes to the local file system.

## Phase 6: Advanced Context & Intelligence Layer
- [ ] **6.1 Implement RAG for Semantic Search:** Implement the full RAG pipeline.
- [ ] **6.2 Implement SQL Schema Analyzer:** Create a service to inspect a project's database schema.
- [ ] **6.3 Implement Git History Analyzer:** Create a service to analyze the Git history.
- [ ] **6.4 Upgrade Orchestrator:** Enhance the Orchestrator to use new context sources.
- [ ] **6.5 Enhance TUI with Context:** Add a new panel or command to the TUI to show context.
