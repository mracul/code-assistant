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

- **Agent:** A modular logic unit that performs a **single-responsibility** task, such as `CodeGenerator` or `RequirementsEngineer`. Agents communicate via structured **JSON input/output schemas**.
- **Orchestrator:** The central component that controls and manages **agent workflows**. It is responsible for sequencing agents, handling retries, managing escalation policies, and maintaining session state.
- **Context Engine:** The system responsible for providing **semantic context** to the agents. It uses techniques like AST parsing, code caching, vector embeddings (RAG), and Git history analysis to build a comprehensive understanding of the user's codebase.
- **Workflow:** A predefined sequence of agents designed to accomplish a high-level task, such as **bug fixing** or **code refactoring**. Workflows are defined in `.json` files in the `/workflows` directory.
- **REPL:** The **interactive command loop** (Read-Eval-Print Loop) in the Node.js front-end that captures user commands and displays the output from the agentic workflows.
- **Mediator Agent:** A specialized type of agent (e.g., `ContextMediator`, `ArchitectureMediator`) whose role is to facilitate a **deliberation** process between other agents to reach a consensus on a specific goal.
- **Deliberation & Consensus:** The iterative, conversational process where agents challenge and refine proposals to reach a shared agreement. This is a core part of the agentic workflow, ensuring robust and well-vetted solutions.
- **Change Manifest:** A detailed, step-by-step plan of changes to be implemented, which is created and agreed upon by the agents during the design phase.

---

## `/python_backend`

The **backend service** that implements all AI logic, agent workflows, and context processing.

*Note: Some directories listed below (`orchestrator`, `agents`, `services`, `utils`) are part of the target architecture and will be created as the project develops.*

### `/python_backend/main.py`

- **Purpose:** The FastAPI application entry point that exposes all REST API endpoints for the frontend to consume.
- **Role:** Manages incoming HTTP requests and delegates them to the appropriate services, such as the orchestrator or individual agents.
- **Design:** Keeps route definitions separate from the core business logic for clarity and maintainability.

### `/python_backend/orchestrator/`

- **Purpose:** Will house the **Orchestrator** class that manages the execution of agentic workflows.
- **Responsibilities:** Will be responsible for loading agent definitions, running workflows as defined in `workflows.json`, and managing **confidence scoring** and **retry policies**.
- **Architecture:** Decouples the high-level **workflow management** from the specific implementation of individual agents, promoting modularity.

### `/python_backend/agents/`

- **Contents:** Will contain the individual **agent modules**, each encapsulating a specific task.
- **Design:** Each agent will adhere to a strict **input/output JSON schema** contract, ensuring predictable and composable behavior.
- **Principles:** Each agent implements the **single responsibility principle** and is designed to be **stateless** wherever possible.

### `/python_backend/context_engine/`

- **Function:** Extracts, caches, and provides **semantic context** about the user's project.
- **Components:** Contains modules for file discovery, AST parsing, and tokenization. Will be expanded to include semantic vector stores, dependency analyzers, and Git history readers.
- **Goal:** To ground agent queries in **accurate, up-to-date, and relevant context**.

### `/python_backend/services/` and `/utils/`

- **Purpose:** Will contain shared **utilities**, such as logging, schema validation, and other helper functions.
- **Benefit:** Enables code reuse and a clear separation of concerns.

---

## `/node_frontend`

The **Node.js TUI client** that provides an interactive user interface for the user.

*Note: Some directories listed below (`components`, `services`) are part of the target architecture and will be created as the project develops.*

### `/node_frontend/cli.js`

- **Role:** The main entry point for the TUI application, responsible for rendering the Ink React components.
- **Function:** Implements the **REPL**, sends user commands to the Python backend, and displays the streamed results and status updates from the agents.
- **Significance:** Acts as the primary **user interface**, abstracting the complexity of the backend services.

### `/node_frontend/components/`

- **Purpose:** Will contain the reusable UI building blocks for the TUI, such as logs, input boxes, and diff viewers.
- **Design:** Will be composed of modular React components to ensure a composable and easily extendable user interface.

### `/node_frontend/services/`

- **Role:** Will contain API client wrappers for communicating with the backend, as well as any client-side state management or caching layers.
- **Separation:** Decouples the network and communication logic from the UI components.

---

## `/workflows`

- **Purpose:** Contains the JSON definitions for the various agentic workflows.
- **Contents:** Each `.json` file in this directory defines a sequence of agents and the logic for their execution for a specific high-level task (e.g., `BugFixing`, `CodeRefactoring`).

---

## Architectural Principles

- **Modularity:** Agents encapsulate **one responsibility** and communicate via structured **JSON contracts**.
- **Statelessness:** Components are designed to be **idempotent** and **reproducible** to the greatest extent possible.
- **Separation of Concerns:** A clear division is maintained between the UI, orchestration, agent logic, and context engine.
- **Documentation-Driven:** All team members (including AI agents) are expected to maintain updated markdown documents (`README.md`, `ARCHITECTURE.md`, `CODEBASE.md`) to reflect the current state and design rationale of the project.
- **Design Patterns:**
  - **Command pattern** for executing workflows in the Orchestrator.
  - **Microservice-like isolation** of agents within the monorepo.
  - **Caching and indexing** strategies in the Context Engine to improve performance.

---

This overview is your **first reference point** for understanding, navigating, and contributing to the project. It ensures efficient retrieval of critical design and implementation knowledge using semantic search tools.

**All implementation details, including design decisions and changes, must be documented here to keep this file as the single source of truth for both developers and AI-driven tooling.**
**When updating this or related documentation, preserve the existing style and rationale, emphasizing additions and improvements over removals.**
