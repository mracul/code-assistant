# Implementation Checklist

This checklist is synchronized with the **Development Plan** in [`GEMINI.md`](./GEMINI.md).

## 🚀 Phase 1: Back-End "Brain" – Python AI Service
- [ ] **1.1 Project Setup (Python):** Action: `Create python_backend dir, virtualenv, and Git init.` | Tools: `venv`
- [ ] **1.2 Install Core Dependencies:** Action: `Install fastapi, uvicorn, openai.` | Tools: `pip`
- [ ] **1.3 Create the API Server:** Action: `Create main.py with basic FastAPI app.` | Tools: `fastapi`
- [ ] **1.4 Build a "Ping" Endpoint:** Action: `Create /api/v1/ping endpoint returning { "status": "ok" }.` | Tools: `fastapi`
- [ ] **1.5 Test the Endpoint:** Action: `Access http://localhost:8000/api/v1/ping.` | Tools: `curl` or browser

## 🧑‍💻 Phase 2: Front-End "Face" – Node.js TUI
- [ ] **2.1 Project Setup (Node.js):** Action: `Init node_frontend/ and package.json.` | Tools: `npm`
- [ ] **2.2 Install Dependencies:** Action: `Install ink, react, axios.` | Tools: `npm`
- [ ] **2.3 Build the Basic TUI:** Action: `Create cli.js with header, log, input.` | Tools: `ink`, `react`
- [ ] **2.4 Implement the REPL:** Action: `Capture user input via Enter key.` | Tools: `ink`
- [ ] **2.5 Connect to Backend:** Action: `On "ping" command, call /api/v1/ping.` | Tools: `axios`

## 🧠 Phase 3: Context Engine – Python Backend
- [ ] **3.1 File System Scanner:** Action: `Find source code files in directory.` | Tools: `os`, `glob`
- [ ] **3.2 SQLite Caching Layer:** Action: `Create .context_cache.db for caching.` | Tools: `sqlite3`
- [ ] **3.3 AST-Based Parser:** Action: `Extract function definitions and dependencies.` | Tools: `ast`
- [ ] **3.4 New Context Endpoint:** Action: `Create POST /api/v1/analyze endpoint.` | Tools: `fastapi`

## 🤖 Phase 4: Agentic Workflow – Python Backend
- [ ] **4.1 Agent Registry:** Action: `Define agents in agents.json. Load definitions.` | Tools: `json`
- [ ] **4.2 Agent Executor:** Action: `Create executor for any agent in registry.` | Tools: `openai`
- [ ] **4.3 Orchestrator Class:** Action: `Manage session state and workflow execution.` | Tools: `(Core Logic)`
- [ ] **4.4 New Workflow Endpoint:** Action: `Create POST /api/v1/execute-workflow.` | Tools: `fastapi`

## 🧩 Phase 5: Closing the Loop – Node.js Frontend
- [ ] **5.1 Connect Workflow Endpoint:** Action: `Call /api/v1/execute-workflow with user input.` | Tools: `axios`
- [ ] **5.2 Status Updates:** Action: `Stream or poll agent status to user.` | Tools: `ink` (Log)
- [ ] **5.3 Display Code Diffs:** Action: `Render color-coded diff in TUI.` | Tools: `diff`, `chalk`
- [ ] **5.4 User Confirmation & File I/O:** Action: `Prompt user, write file changes if approved.` | Tools: `inquirer`, `fs`

## 🧬 Phase 6: Advanced Context & Intelligence Layer
- [ ] **6.1 Implement RAG for Search:** Action: `Full semantic search pipeline on startup.` | Tools: `sentence-transformers`, `chromadb`
- [ ] **6.2 SQL Schema Analyzer:** Action: `Connect to DB, return schema info as JSON.` | Tools: `sqlalchemy`
- [ ] **6.3 Git History Analyzer:** Action: `Analyze git history for hot/relevant files.` | Tools: `gitpython`
- [ ] **6.4 Upgrade Orchestrator:** Action: `Add hybrid ranking: keywords, semantic, git, deps.` | Tools: `(Core Logic)`
- [ ] **6.5 Enhance TUI with Context:** Action: `Add panel explaining context file selection.` | Tools: `ink`
