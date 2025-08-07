<!--
AGENT_INSTRUCTION: This document is a comprehensive **semantic map** of the codebase for the Hybrid Agentic CLI Assistant. Use it to locate key modules, understand architectural relationships, and grasp design rationale. It is optimized for RAG, vector search, and semantic retrieval.

**Implementation details, design decisions, and rationale must be maintained and updated in this document** to ensure a single source of truth for developers and AI agents.

**Any changes to this file or related documentation must adhere to the existing style and rationale of the current implementation.**  
Focus on **adding meaningful context, clarifications, or new functionality** rather than removing or refactoring existing content unless absolutely necessary and justified.
-->

# Codebase Overview

This document details the core **modules**, **patterns**, and **terminology** of the project. It explains the structure, responsibilities, and interactions to facilitate efficient code comprehension and retrieval.

---

## Core Concepts

- **Agent:** Modular logic units performing **single-responsibility** tasks. Communicate via **JSON input/output schemas**.
- **Orchestrator:** Controls and manages **agent workflows**, handling retries, escalation, and session state.
- **Context Engine:** Provides **semantic context** using AST parsing, caching, embeddings, and Git history.
- **Workflow:** Predefined sequences of agents for tasks like **bug fixing** or **code refactoring**.
- **REPL:** The **interactive command loop** in the Node.js front-end capturing user commands and displaying output.

---

## `/python_backend`

The **backend service** implementing all AI logic, agent workflows, and context processing.

### `/python_backend/main.py`

- **Purpose:** FastAPI app entry point exposing all REST API endpoints.
- **Role:** Manages HTTP requests, delegates to orchestrator and agents.
- **Design:** Separates route definitions from business logic for clarity.

### `/python_backend/orchestrator/`

- **Purpose:** Houses the **Orchestrator** class managing workflow execution.
- **Responsibilities:** Loads agents, runs workflows from `workflows.json`, manages **confidence scoring** and **retry policies**.
- **Architecture:** Decouples **workflow management** from agent implementation, promoting modularity.

### `/python_backend/agents/`

- **Contents:** Individual **agent modules** encapsulating specific tasks.
- **Design:** Each agent follows strict **input/output JSON schema** contracts.
- **Principles:** Implements **single responsibility** and is **stateless** where possible.

### `/python_backend/context_engine/`

- **Function:** Extracts and caches **project context**.
- **Components:** AST parsers, semantic vector stores, dependency analyzers, Git history readers.
- **Goal:** Ground agent queries in **accurate, up-to-date context**.

### `/python_backend/services/` and `/utils/`

- **Purpose:** Shared **utilities**, logging, schema validation, and helpers.
- **Benefit:** Enables code reuse and separation of concerns.

---

## `/node_frontend`

The **Node.js TUI client** providing an interactive user interface.

### `/node_frontend/cli.js`

- **Role:** Entry point rendering the Ink React components.
- **Function:** Implements the **REPL**, sending commands to the backend and displaying streamed results.
- **Significance:** Acts as the **user interface**, abstracting backend complexity.

### `/node_frontend/components/`

- **Purpose:** UI building blocks like logs, inputs, and diff views.
- **Design:** Modular React components for composability and reuse.

### `/node_frontend/services/`

- **Role:** API client wrappers, state management, caching layers.
- **Separation:** Decouples network logic from UI components.

---

## Architectural Principles

- **Modularity:** Agents encapsulate **one responsibility**; communicate via **JSON contracts**.
- **Statelessness:** Components are designed to be **idempotent** and **reproducible**.
- **Separation of Concerns:** Clear division between UI, orchestration, agent logic, and context.
- **Documentation-Driven:** Maintain updated markdown docs (`README.md`, `ARCHITECTURE.md`, `CODEBASE_OVERVIEW.md`) for context and design rationale.
- **Design Patterns:**  
  - **Command pattern** for workflows in Orchestrator.  
  - **Microservice-like isolation** of agents within a monorepo.  
  - **Caching and indexing** strategies in Context Engine.

---

This overview is your **first reference point** for understanding, navigating, and contributing to the project. It ensures efficient retrieval of critical design and implementation knowledge using semantic search tools.

**All implementation details, including design decisions and changes, must be documented here to keep this file as the single source of truth for both developers and AI-driven tooling.**  
**When updating this or related documentation, preserve the existing style and rationale, emphasizing additions and improvements over removals.**
