<!--
AGENT_INSTRUCTION: This file contains the primary overview and setup instructions for the project. Refer to this to understand the project's main goal and how to get it running.
-->

# Hybrid Agentic CLI Assistant (Node.js + Python)

This project is a hybrid command-line application that acts as an AI-powered coding partner. It combines a responsive Node.js-based terminal user interface (TUI) with a powerful Python backend that hosts AI agents, a context engine, and workflow orchestration.

The primary goal of this project is to provide a tool that can understand a user's codebase, assist with complex tasks like refactoring, bug fixing, and feature development, and automate the generation of documentation and commit messages.

## Architecture Overview

The system is composed of two main services:

*   **Node.js Frontend ("The Face"):** A terminal UI built with Ink and React, providing an interactive REPL for users to interact with the AI agents.
*   **Python Backend ("The Brain"):** A FastAPI server that runs the AI logic, including a context engine for code analysis, agent execution, and workflow orchestration.

For a more detailed explanation of the architecture, please see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

## Getting Started

### Prerequisites

*   Node.js and npm
*   Python 3 and pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Setup the Python Backend:**
    ```bash
    cd python_backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    cd ..
    ```

3.  **Setup the Node.js Frontend:**
    ```bash
    cd node_frontend
    npm install
    cd ..
    ```

### Running the Application

1.  **Start the Python Backend:**
    ```bash
    cd python_backend
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    uvicorn main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

2.  **Start the Node.js Frontend:**
    In a new terminal window:
    ```bash
    cd node_frontend
    npm start
    ```

## Usage

Once the application is running, you can interact with the agentic assistant through the terminal. The TUI provides a REPL where you can type commands and receive feedback from the agents.

Example commands:
*   `ping`: To check the connection to the backend.
*   `analyze <path>`: To have the context engine analyze a directory.
*   `execute <workflow> <...args>`: To run a specific agentic workflow.

## Contributing

We welcome contributions! Before you start, please read the following documents to understand the project's philosophy, architecture, and codebase.

*   **[`GEMINI.md`](./GEMINI.md):** The master blueprint for the project. It contains the development plan, agentic workflows, and overall project vision.
*   **[`ARCHITECTURE.md`](./ARCHITECTURE.md):** A detailed description of the system's architecture.
*   **[`CODEBASE.md`](./CODEBASE.md):** A semantic map of the codebase to help you navigate the project.