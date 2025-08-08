# Codebase Guide

This document provides a developer-oriented overview of the key modules and files in the project.

## Root Directory

-   `start-dev-environment.ps1`: PowerShell script to launch the full development environment.
-   `ARCHITECTURE.md`: High-level overview of the system architecture.
-   `CODEBASE.md`: This file.
-   `GEMINI.md`: The master project blueprint and development plan.
-   `IMPLEMENTATION_CHECKLIST.md`: A checklist tracking the implementation of core features.
-   `workflows.json`: Defines the sequences of agent execution for high-level tasks.
-   `tools.json`: OpenAI-compatible function-calling specification for the core toolchain.

## Frontend (`node_frontend/`)

-   `cli.js`: The main entry point and component for the Ink-based TUI. It handles rendering all UI panels, managing frontend state, and communicating with the backend via WebSocket.

## Backend (`python_backend/`)

-   `main.py`: The main entry point for the FastAPI application. It defines all API endpoints and the primary WebSocket handler, and contains the core **Command Dispatcher** logic.

### Agents (`python_backend/agents/`)

-   `refactor_agent.py`: Implements safe, structural refactoring (e.g., renaming functions) using AST transformations.
-   `diff_agent.py`: Generates LLM-driven code modifications and creates a unified diff of the changes.
-   `code_search_agent.py`: Implements the hybrid search logic (AST + semantic).
-   `change_summarizer_agent.py`: Takes a code diff and uses an LLM to generate a structured summary.
-   `conventional_commit_agent.py`: Takes a structured summary and uses an LLM to create a conventional commit message.
-   `version_control_agent.py`: Generates `git` commands for staging and committing changes.

### Orchestrator (`python_backend/orchestrator/`)

-   `agent_state.py`: Defines the `AgentState` class, the central hub for managing session-specific data.
-   `context_builder.py`: Implements the incremental refinement loop to build high-confidence context for agents.
-   `conversation_history.py`: A robust, token-aware class for managing dialogue history with persistence.
-   `prompt_parser.py`: Parses the raw user input string to extract commands, arguments, and file tags.

### Utilities (`python_backend/utils/`)

-   `ast_search.py`: A tool for performing structural queries on a file's Abstract Syntax Tree.
-   `path_validator.py`: A security utility for validating and normalizing all file paths.
-   `swe_tools.py`: A module containing the core "Software Engineering" toolchain.

### Prompts (`python_backend/prompts/`)

-   This directory contains the structured Markdown prompt templates that guide the behavior of the LLM-powered agents.
