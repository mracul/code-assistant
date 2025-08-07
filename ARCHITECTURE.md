<!--
AGENT_INSTRUCTION: This document is the definitive architecture reference for the Hybrid Agentic CLI Assistant.  
Consult it for any design, implementation, refactoring, or feature extension to ensure consistency with the system’s core principles and architecture.  
Maintain and update this file with all architectural decisions, including rationale and trade-offs, to keep it as the single source of truth.
-->

# Architecture Overview

This document details the architecture of the Hybrid Agentic CLI Assistant, a distributed system designed to combine a highly responsive terminal UI with a powerful AI-driven backend. The architecture balances modularity, scalability, and maintainability, supporting complex agent workflows driven by advanced semantic context retrieval.

---

## System Composition

The system consists of **two primary services** working in tandem:

- **Node.js TUI Frontend ("The Face")**
- **Python AI Backend ("The Brain")**

This separation enables a lightweight, responsive user interface tightly integrated with a robust AI and semantic analysis engine.

---

## Frontend: Node.js Terminal UI

### Role

The frontend provides an **interactive command-line interface** where users input commands, review agent suggestions, and approve or reject code changes.

### Core Technologies

- **Ink** — React renderer tailored for terminal apps, facilitating dynamic and declarative UI construction.
- **React** — Component-based UI architecture, enabling modular and reusable interface elements.
- **Axios** — HTTP client responsible for reliable communication with the backend API.

### Responsibilities

- **User Interaction & REPL:** Captures and processes user commands in a classic Read-Eval-Print Loop.
- **Rendering UI:** Displays agent activity logs, real-time status updates, and structured, color-coded code diffs.
- **Backend Communication:** Sends JSON-formatted requests to backend endpoints and streams back results.
- **User Confirmation Workflow:** Handles user approval or rejection of proposed code changes, enabling controlled file system modifications.

### Architectural Rationale

- Decoupling UI from backend logic optimizes responsiveness.
- Using React/Ink promotes modular UI components, enabling easy extension.
- RESTful communication simplifies integration and future scalability.

---

## Backend: Python AI Service

### Role

The backend hosts the core AI logic, semantic context engines, and orchestrates agent workflows that analyze, modify, and generate code and other artifacts.

### Core Technologies

- **FastAPI + Uvicorn:** High-performance ASGI web framework and server providing RESTful API endpoints.
- **SQLite:** Lightweight local database caching parsed code, vector embeddings, and dependency graphs.
- **SQLAlchemy:** ORM for inspecting and interacting with project databases.
- **GitPython:** Tool for accessing Git metadata and history to inform semantic relevance heuristics.
- **AI/ML Stack:** Embedding models (`sentence-transformers`), vector DB (`chromadb`), and LLM providers (e.g., OpenAI).

### Key Components

#### API Server

- Handles frontend requests with endpoints like `/ping`, `/analyze`, and `/execute-workflow`.
- Delegates to orchestration layer for agent-driven workflows.

#### Context Engine

- **Source Scanner:** Recursively scans project directories for source files.
- **AST Parser:** Transforms code into Abstract Syntax Trees to extract declarations, dependencies, and structure.
- **Cache Layer:** Persists parsed data and embeddings for fast subsequent retrieval.

#### Intelligence Layer

- **RAG (Retrieval-Augmented Generation):** Combines vector embeddings and keyword search for semantically rich context retrieval.
- **Schema Analyzer:** Inspects connected databases to inform agents about schema structure.
- **Git Analyzer:** Leverages commit history and co-change heuristics to prioritize relevant files.

#### Agentic Workflow Orchestrator

- **Agent Registry:** Dynamically loads agent definitions and capabilities.
- **Agent Executor:** Executes agents in isolated contexts with strict input/output contracts.
- **Workflow Manager:** Coordinates multi-agent sequences according to `workflows.json`, handling retries, confidence scoring, and escalation policies.

### Architectural Rationale

- Modular separation of concerns improves maintainability and testability.
- Stateless agents with defined I/O schemas enable predictable, composable workflows.
- Use of caching and vector search balances performance with semantic depth.
- Leveraging existing AI/ML libraries accelerates development and future-proofs the stack.

---

## Project Structure

```plaintext
project-root/
├── node_frontend/       # TUI client
│   ├── cli.js           # REPL entry point
│   ├── components/      # React UI components
│   └── services/        # API clients, state management
├── python_backend/      # AI and orchestration backend
│   ├── main.py          # FastAPI server entrypoint
│   ├── orchestrator/    # Workflow and agent management
│   ├── agents/          # Individual AI agents with JSON I/O
│   ├── context_engine/  # Parsers, caches, vector DB integration
│   ├── services/        # Shared logic, API clients
│   ├── utils/           # Utilities and helpers
│   └── .context_cache.db# SQLite cache
├── workflows/           # Workflow definitions (JSON)
│   └── default.json
├── .env                 # Environment variable templates
└── README.md            # Project overview and instructions

Design Principles & Best Practices

    Single Responsibility: Each module, agent, or service addresses a distinct concern.

    Stateless Agents: Agent executions are deterministic, relying solely on explicit inputs.

    JSON Schemas: Agents communicate via well-defined input/output JSON templates.

    Separation of Concerns: UI, orchestration, context retrieval, and AI logic are cleanly separated.

    Extensibility: New agents and workflows can be added without disrupting existing pipelines.

    Semantic Contextualization: Context engine and RAG system provide precise, relevant information to agents.

    Documentation-Driven Development: Architecture and design decisions are continuously documented to maintain a shared understanding.

    Confidence & Escalation: Workflows include mechanisms to retry or escalate based on quantitative confidence scores.

Usage & Extension Notes

    When adding new features or refactoring, adhere to the existing architectural patterns and style.

    Focus on enhancing context awareness and modularity rather than restructuring core components.

    Maintain and extend this document to record architectural changes and rationale.

    Agent inputs and outputs should always be expressed with JSON schemas to ensure interoperability and traceability.