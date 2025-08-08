# System Architecture

This document outlines the high-level architecture of the Hybrid Agentic CLI Assistant. The system is designed with a clear separation of concerns between the user interface, the backend orchestration logic, and the AI-powered agentic core.

## Core Components

1.  **Node.js TUI Frontend (`node_frontend/`)**:
    *   A rich, multi-panel terminal interface built with **Ink** and **React**.
    *   Provides regions for logs, active file lists, and a main content view for file previews and diffs.
    *   Communicates with the backend exclusively via a **WebSocket** for real-time, bidirectional updates and a REST API for initial commands.

2.  **Python FastAPI Backend (`python_backend/`)**:
    *   Serves as the central "brain" of the application, powered by the **GPT-4.1-mini** model.
    *   Exposes a WebSocket endpoint for persistent communication with the TUI.
    *   Exposes REST endpoints for stateless commands and receiving user input.

3.  **Orchestrator & Command Dispatcher (`python_backend/orchestrator/`)**:
    *   **Prompt Parser**: Analyzes raw user input to distinguish between commands (e.g., `/load`, `/refactor`, `/commit`) and natural language prompts.
    *   **Command Dispatcher**: Routes parsed commands to the appropriate agent or workflow.
    *   **Context Builder**: Incrementally gathers, evaluates, and refines context (files, history, search results) until a confidence threshold is met before passing it to an agent.

4.  **State & Context Manager (`python_backend/orchestrator/`)**:
    *   **AgentState**: A structured class managing the complete state for a user session, including loaded files, ASTs, modified code buffers, and conversation history.
    *   **ConversationHistory**: A token-aware class that manages the dialogue, supporting truncation and persistent storage to disk.

5.  **Hybrid Search & Context Engine (`python_backend/context_engine/`)**:
    *   **AST-Aware Chunking & Search**: Intelligently chunks Python code by functions/classes and provides tools for precise, structural code queries.
    *   **Vector Store**: Uses **ChromaDB** to store embeddings of code chunks for fast semantic retrieval (RAG).

6.  **Agentic Core (`python_backend/agents/`)**:
    *   A collection of specialized agents, each responsible for a specific task. Key agents include:
        *   `CodeSearchAgent`: Performs hybrid AST and semantic searches.
        *   `DiffAgent`: Generates LLM-driven code changes and presents them as a diff.
        *   `RefactorAgent`: Performs safe, structural refactoring using AST transformations.
        *   `ChangeSummarizerAgent`: Summarizes a code diff into a structured format.
        *   `ConventionalCommitAgent`: Creates a conventional commit message from a summary.
        *   `VersionControlAgent`: Generates the final `git` commands.

## Data Flow: Example End-to-End Workflow (`/refactor` -> `/commit`)

1.  User issues a command: `/refactor main.py old_func new_func`.
2.  The **Command Dispatcher** validates the path and invokes the **RefactorAgent**.
3.  The `RefactorAgent` performs an AST transformation, generates a diff, and sends it to the **TUI** for confirmation.
4.  User confirms the diff by typing `yes`. The change is written to disk.
5.  User issues a new command: `/commit`.
6.  The **Command Dispatcher** invokes the finalization workflow:
    a.  The **ChangeSummarizerAgent** is called with the last diff. It uses the LLM to generate a structured summary (title, description, type).
    b.  The **ConventionalCommitAgent** takes this summary and uses the LLM to format a perfect conventional commit message.
    c.  The **VersionControlAgent** takes the commit message and generates the final `git add` and `git commit` commands.
7.  The final commands and commit message are sent to the **TUI** for the user to copy and execute.