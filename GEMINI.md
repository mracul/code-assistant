<!--
AGENT_INSTRUCTION: This document is the master blueprint and the single source of truth for the "Hybrid Agentic CLI Assistant" project. You must consult this file at the beginning of any new task to ensure your actions are aligned with the overall plan and architecture.

**How to Use This Document:**

1.  **Consult the `Development Plan`:** Before starting a task, refer to the `Development Plan` to understand the current phase of development and the specific goals for this stage. Your actions should always be in service of completing the current phase.

2.  **Understand the `Agentic Workflows`:** To understand your role in a larger task, refer to the `Agentic Workflows` section. This will show you which agents run before you, what inputs you should expect, and which agents will consume your output. Always adhere to these established workflows.

3.  **Reference `Agents.json` for Your Capabilities:** Your specific instructions, dependencies, and output schemas are defined in the `agents.json` section. You must strictly adhere to this contract when executing your tasks.

**Proposing Changes & Deviations:**

This is a living document that serves as a guide. It is not expected to be followed exactly if a better path is discovered. If, during your reasoning process, you identify a more efficient, robust, or logical way to achieve a goal, you are encouraged to **propose a modification to the plan.**

Any proposed change must be accompanied by:
- A **clear rationale** explaining why the deviation is an improvement.
- An **impact analysis** of how the change might affect other parts of the plan.
- Confirmation that the change still aligns with the project's core architectural principles.

Your primary goal is to act as a collaborative partner in executing the `Development Plan`. Always reason with the information in this document to stay on track, but do not hesitate to suggest improvements.

Always keep implementation rules in mind and follow as best you can.

-->

# Hybrid Agentic CLI Assistant (Node.js + Python)

## Table of Contents
- [Implementation Rules](#implementation-rules)
- [Development Plan](#development-plan)
- [Agentic Workflows](#agentic-workflows)
- [Agents.json](#agentsjson)
- [Workflows.json](#workflowsjson)
- [Workflows Decomposition](#workflows-decomposition)

---
````markdown
## Implementation Rules

### 🧠 Agentic CLI Assistant: Implementation Specification

---

### ⚙️ 1. Project Philosophy

- **Keep documentation updated**: CODEBASE, README, ARCHITECTURE — consult regularly.
- **Clarity over cleverness**: Prefer understandable code over “smart” tricks.
- **Avoid unnecessary abstraction**: Only abstract if it improves readability, testability, or reusability.
- **Separation of concerns**: Each module, function, and file must serve one responsibility.
- **Composable agents**: Agents must be modular, with clearly defined inputs, outputs, and predictable behaviors.
- **Stateless and deterministic where possible**: Minimize side effects. Make workflows reproducible.
- **Data-driven interaction**: Use JSON templates or schemas. Avoid ad-hoc string parsing.

---

### ✍️ 2. Documentation Rules (Stringent)

#### ✅ Markdown Files

- Use `#`, `##`, `###` headings for semantic hierarchy.
- **Bold** key phrases and terminology.
- One topic per section.
- Each file must include:
  - Purpose
  - Inputs / Outputs
  - Limitations / Known Issues
  - Dependencies
  - Examples (realistic)

#### ✅ Code Docstrings

- One-liner only.
- Verb-first action description.
- No type annotations.
- Describe **semantic intent**, not just mechanics.

#### ✅ Example

```python
def route_request_to_agent(agent_name: str, payload: dict) -> dict:
    """Route JSON request to the correct agent."""
````

---

### 🧠 3. Agent Design Patterns

#### ✅ Agent Rules

* One file = one agent.
* Each agent must include:

  * Task metadata block (YAML or JSON)
  * Request and response schemas
  * A `run()` or `handle()` function
  * No side effects unless explicitly declared

#### ✅ Input Format (Example)

```json
{
  "agent": "Refactor",
  "task": "simplify nested conditionals",
  "files": ["file1.js"],
  "strategy": "flatten_logic"
}
```

#### ✅ Output Format (Example)

```json
{
  "success": true,
  "diff": "...",
  "notes": "Reduced cyclomatic complexity from 12 to 5."
}
```

---

### 📐 4. Style & Naming Conventions

#### ✅ Naming Rules

* `camelCase` for JavaScript, `snake_case` for Python.
* File/folder names: lowercase, dash-separated.
* `PascalCase` for classes.
* No vague names like `doTask`, `thing` — use domain-specific terminology.

#### ✅ Code Style

* **DRY**: Reuse logic via shared utils.
* **SOLID**: Favor composition, not inheritance.
* Flat control flow: Minimize nesting, use early returns.
* **Explicit return statements** everywhere.

---

### 🧱 5. Structural Guidelines

#### 🧩 Modular Architecture Principles

* **Single Responsibility**: Each folder encapsulates a distinct concern (e.g., `agents/`, `orchestrator/`, `utils/`, `context_engine/`).
* **Interface & Logic Separation**: Templates (`request.json`, `response.json`) should sit next to code but stay decoupled.
* **Explicit Context Paths**: Folder structure should reflect logical data and control flow.

#### 📁 Root Directory Philosophy

* `node_frontend/`: CLI interface and visual components.
* `python_backend/`: All backend logic and orchestration.
* `workflows/`: Composable logic trees or automation flows.
* `.env` and `README.md`: Root anchors for configuration and context.

#### 🧬 Agent Folder Philosophy

Each agent folder must contain:

* `agent.{js,py}`: Core logic implementation.
* `request.json`, `response.json`: Typed, minimal interface definitions.
* `README.md`: Purpose, inputs, outputs, limitations — always up-to-date.

#### 🔁 Shared Modules Philosophy

* `utils/`: Atomic helpers, formatting, validation.
* `orchestrator/`: Task routing and workflow control.
* `context_engine/`: Caching, context storage, retrieval.
* `schemas/`: Versioned JSON schemas for input/output.
* `prompts/`: (If present) Templated LLM prompt files.

#### ✅ Boundaries

* Agent logic must not leak orchestration logic.
* Agents must be **pluggable and predictable**.

---

### 🔁 6. Templating & Repeatable Behavior

* Use **YAML** or **JSON** for all task definitions.
* Centralize all prompt templates.
* No inline prompts unless absolutely required.
* All agents and workflows must support **dry-run** mode.

---

### 🚫 7. Anti-Patterns to Avoid

| ❌ Anti-Pattern           | ✅ Preferred Alternative        |
| ------------------------ | ------------------------------ |
| Inline string templates  | Centralized prompt manager     |
| `if agent == X` branches | Use a routing table / registry |
| Mixed-type inputs        | Typed or schema-validated JSON |
| Deeply nested workflows  | Flat, composable steps         |
| Script-style logic       | Pure functions + orchestrator  |

---

### 🧪 8. Testing & Validation

Each agent must support:

* Mock input/output tests.
* Pre-validation via **JSON Schema**.
* Output verification (e.g., Git diffs, logs, behavior changes).
* **Dry-run mode** must skip writes and return proposed changes only.

---

### 📦 9. Agent Workflow Example

#### 🧭 Step-by-Step Breakdown

1. **Receive Request**

   * Orchestrator gets structured JSON input.
2. **Determine Agent**

   * Use registry lookup (e.g., `agentRegistry['Refactor']`).
3. **Validate Schema**

   * Against `schemas/refactor.request.json`.
4. **Load Context**

   * Load code/files, AST, or plain text.
5. **Run Agent**

   * Agent returns structured result (diffs, logs, notes).
6. **Post-Process**

   * Orchestrator stores/logs/displays result.
7. **Return Response**

   * Send full result back to caller.

---

## 10. Retrieval & RAG Integration

* Use **short, descriptive docstrings**.
* Write **structured, indexed markdown**.
* Maintain **unified terminology** across:

  * `README.md`
  * `schemas/`
  * `prompts/`
  * `agents/`

```
```


---

## 🛠️ Development Plan

This section outlines a **phased development plan** to build your **agentic code editing application** using a **Node.js front-end** and a **Python back-end**. This architecture provides a highly responsive UI while leveraging Python's best-in-class AI and code analysis ecosystem.

---

### 🚀 Phase 1: Back-End "Brain" – Python AI Service

**Goal:** Set up the Python environment and create a basic, runnable API server that can perform a simple task.

| Step    | Action                    | Key Libraries/Tools | Success Criteria                                               |
| ------- | ------------------------- | ------------------- | -------------------------------------------------------------- |
| **1.1** | Project Setup (Python)    | `venv`              | Create `python_backend` dir, virtualenv, and Git init.         |
| **1.2** | Install Core Dependencies | `pip`               | Install `fastapi`, `uvicorn`, `openai`.                        |
| **1.3** | Create the API Server     | `fastapi`           | Create `main.py` with basic FastAPI app.                       |
| **1.4** | Build a "Ping" Endpoint   | `fastapi`           | Create `/api/v1/ping` endpoint returning `{ "status": "ok" }`. |
| **1.5** | Test the Endpoint         | `curl` or browser   | Access `http://localhost:8000/api/v1/ping`.                    |

---

### 🧑‍💻 Phase 2: Front-End "Face" – Node.js TUI

**Goal:** Set up Node.js project, build a basic TUI, and connect to Python backend.

| Step    | Action                  | Key Libraries/Tools | Success Criteria                          |
| ------- | ----------------------- | ------------------- | ----------------------------------------- |
| **2.1** | Project Setup (Node.js) | `npm`               | Init `node_frontend/` and `package.json`. |
| **2.2** | Install Dependencies    | `npm`               | Install `ink`, `react`, `axios`.          |
| **2.3** | Build the Basic TUI     | `ink`, `react`      | Create `cli.js` with header, log, input.  |
| **2.4** | Implement the REPL      | `ink`               | Capture user input via Enter key.         |
| **2.5** | Connect to Backend      | `axios`             | On "ping" command, call `/api/v1/ping`.   |

---

### 🧠 Phase 3: Context Engine – Python Backend

**Goal:** Build logic for understanding the user's codebase.

| Step    | Action               | Key Libraries/Tools | Success Criteria                               |
| ------- | -------------------- | ------------------- | ---------------------------------------------- |
| **3.1** | File System Scanner  | `os`, `glob`        | Find source code files in directory.           |
| **3.2** | SQLite Caching Layer | `sqlite3`           | Create `.context_cache.db` for caching.        |
| **3.3** | AST-Based Parser     | `ast`               | Extract function definitions and dependencies. |
| **3.4** | New Context Endpoint | `fastapi`           | Create `POST /api/v1/analyze` endpoint.        |

---

### 🤖 Phase 4: Agentic Workflow – Python Backend

**Goal:** Implement Orchestrator and agent execution logic.

| Step    | Action                | Key Libraries/Tools | Success Criteria                                  |
| ------- | --------------------- | ------------------- | ------------------------------------------------- |
| **4.1** | Agent Registry        | `json`              | Define agents in `agents.json`. Load definitions. |
| **4.2** | Agent Executor        | `openai`            | Create executor for any agent in registry.        |
| **4.3** | Orchestrator Class    | *(Core Logic)*      | Manage session state and workflow execution.      |
| **4.4** | New Workflow Endpoint | `fastapi`           | Create `POST /api/v1/execute-workflow`.           |

---

### 🧩 Phase 5: Closing the Loop – Node.js Frontend

**Goal:** Seamless UX via full backend/frontend integration.

| Step    | Action                       | Key Libraries/Tools | Success Criteria                                 |
| ------- | ---------------------------- | ------------------- | ------------------------------------------------ |
| **5.1** | Connect Workflow Endpoint    | `axios`             | Call `/api/v1/execute-workflow` with user input. |
| **5.2** | Status Updates               | `ink` (Log)         | Stream or poll agent status to user.             |
| **5.3** | Display Code Diffs           | `diff`, `chalk`     | Render color-coded diff in TUI.                  |
| **5.4** | User Confirmation & File I/O | `inquirer`, `fs`    | Prompt user, write file changes if approved.     |

---

### 🧬 Phase 6: Advanced Context & Intelligence Layer

**Goal:** Deepen agent intelligence using historical and semantic signals.

| Step    | Action                   | Key Libraries/Tools                 | Success Criteria                                   |
| ------- | ------------------------ | ----------------------------------- | -------------------------------------------------- |
| **6.1** | Implement RAG for Search | `sentence-transformers`, `chromadb` | Full semantic search pipeline on startup.          |
| **6.2** | SQL Schema Analyzer      | `sqlalchemy`                        | Connect to DB, return schema info as JSON.         |
| **6.3** | Git History Analyzer     | `gitpython`                         | Analyze git history for hot/relevant files.        |
| **6.4** | Upgrade Orchestrator     | *(Core Logic)*                      | Add hybrid ranking: keywords, semantic, git, deps. |
| **6.5** | Enhance TUI with Context | `ink`                               | Add panel explaining context file selection.       |

---

**All phases build on each other. Modular execution recommended.**

---

## Agentic Workflows 

The Complete Specialist-Driven Agentic Workflow

This document outlines the final, four-stage framework for decomposing complex software development tasks into a verifiable, agent-driven workflow. It is designed to be language-agnostic at the strategic level, with a process that can be applied to any programming domain. At the execution level, it relies on domain-specific specialist agents (e.g., for Python, JavaScript, SQL) to perform the actual work. This separation of concerns ensures that the high-level logic of problem-solving remains consistent, while the low-level implementation is expertly handled by specialists trained for the specific tech stack.

Crucially, each stage now concludes with a mediated deliberation phase where agents converse and reason together in a back-and-forth dialogue until consensus on the optimal path forward is achieved. This step is fundamental to the framework's robustness, transforming it from a simple pipeline into a collaborative, self-correcting system that mimics the peer review and discussion inherent in high-functioning human development teams.
Stage 1: Situational Awareness & Context Modeling

Goal: To build a comprehensive and accurate model of the user's request and the current state of the codebase, enriched with historical and external context from the ContextManager. This stage is not just about finding files; it's about creating a deep, multi-faceted understanding of the problem space, ensuring that any proposed solution is grounded in both the explicit request and the implicit realities of the project.

Phase
	

Action
	

Agents / Features

1.1: Requirements Elicitation & Translation
	

Translate the raw user prompt into a structured list of functional and non-functional requirements. This involves disambiguating vague language and defining clear, verifiable acceptance criteria.
	

RequirementsEngineer

1.2: Stored Context Retrieval
	

Query external knowledge sources (RAG, databases, conversation history) for context relevant to the requirements. This step uncovers "tribal knowledge" that isn't present in the source code itself, such as past architectural decisions or related bug fixes.
	

StoredContextRetriever

1.3: Codebase Search & Discovery
	

Search and scan the live codebase for all potentially relevant files, guided by the requirements and stored context. This is a broad-spectrum search designed to gather all possible candidate files for deeper analysis.
	

CodebaseScanner

1.4: Domain Identification
	

Analyze the relevant files to determine the primary programming language and framework (e.g., Python/Django, TypeScript/React). This critical step allows the Orchestrator to load the correct set of domain-specific tools and agents for the rest of the workflow.
	

DomainIdentifier

1.5: Relevance Assessment
	

Score file relevance using semantic search (embeddings) and dependency graph analysis. This phase acts as a filter, narrowing the focus from all possible files to the ones that are most critical to the task at hand.
	

RelevanceEngine

1.6: Raw Context Gathering
	

Gather the full content of the highest-scoring files and their immediate dependencies. This provides the raw material for the deep analysis that follows.
	

ContextGatherer

1.7: Contextual Relationship Mapping
	

Map and link code artifacts into a structured graph using domain-specific tools (e.g., a Python AST parser). This moves beyond text and creates a true structural understanding of the code, mapping out function calls, class inheritance, and data flow.
	

[Domain]-ContextBuilder

1.8: Context Packaging
	

Consolidate all gathered information into a comprehensive context package for agent consumption. This package is a rich, multi-layered data object containing everything an agent needs to know to make an informed decision.
	

Orchestrator

1.9: Deliberation & Consensus
	

The Orchestrator reviews the final context package to ensure it is complete and coherent before proceeding. This is a final sanity check to prevent the system from attempting to solve a problem with incomplete or contradictory information.
	

ContextMediator, RequirementsEngineer
Stage 2: Solution Design & Architectural Planning

Goal: To devise a robust and well-designed plan by having domain-specific agents propose and refine solutions collaboratively. This stage emphasizes the importance of planning before execution, ensuring that the proposed changes are not only functional but also architecturally sound, maintainable, and aligned with the project's existing patterns.

Phase
	

Action
	

Agents

2.1: Structural Analysis
	

Analyze the code structure and recognize existing architectural patterns and anti-patterns specific to the identified domain. This provides the baseline understanding of "how things are done" in this particular project.
	

[Domain]-StructureAnalyzer

2.2.A: Exploratory Solution Brainstorming
	

Propose multiple distinct, high-level solution strategies using domain-appropriate patterns. This is a creative step where different agents may propose different approaches (e.g., one might suggest a new class, while another suggests modifying an existing service).
	

[Domain]-CreativeArchitect

2.2.B: Solution Feasibility & Risk Assessment
	

Critically evaluate brainstormed strategies against technical constraints and select the optimal approach. This analytical step weighs the pros and cons of each proposal, considering factors like implementation time, performance impact, and long-term maintainability.
	

TechnicalAnalyst

2.3: Architectural Refinement & Specification
	

Define the initial architectural plan, including new/modified interfaces, and create a detailed Change Manifest. This translates the selected high-level strategy into a precise, step-by-step set of instructions for the implementation agents.
	

[Domain]-ArchitectureRefactorer

2.4: OOP & SOLID Principle Enforcement
	

Review and refine the architectural plan to ensure it follows clean code principles as they apply to the specific language. This is a critical quality gate that ensures the proposed changes don't introduce technical debt.
	

[Domain]-OOPDesigner

2.5: Deliberation & Consensus
	

The design agents deliberate to confirm the architectural plan is robust, feasible, and optimal. This final review ensures all design specialists agree on the proposed course of action before any code is written.
	

ArchitectureMediator, TechnicalAnalyst
Stage 3: Coordinated Implementation & Transformation

Goal: To execute the plan by making precise changes using language-specific tools and code generation techniques. This stage is about the mechanical, yet highly skilled, process of turning the architectural blueprint into functional code.

Phase
	

Action
	

Agents

3.1: Task Orchestration Setup
	

Plan and define the execution sequence of implementation tasks based on dependencies. This ensures that changes are made in the correct order (e.g., creating a new class before it is used).
	

OrchestratorAgent

3.2.A: Code Transformation & Refactoring
	

Safely apply planned modifications and refactoring to existing code using domain-specific refactoring tools. This is a surgical process that often involves direct manipulation of the AST to ensure precision.
	

[Domain]-RefactorAgent, [Domain]-ASTTransformer

3.2.B: De Novo Code Generation
	

Create entirely new files, classes, or functions from the architectural specification, following domain conventions. This is a generative task where the agent writes new code from scratch based on the plan.
	

[Domain]-CodeGenerator

3.3: Performance Optimization (Conditional)
	

If required, profile for bottlenecks and apply specific performance optimizations using domain-specific profilers. This phase is triggered if the initial requirements included performance goals.
	

[Domain]-PerformanceOptimizer

3.4: Bug Fix Implementation (Conditional)
	

If the task is a bug fix, analyze the defect and generate a patch using domain-specific debugging techniques. This phase involves a more analytical approach to pinpoint and correct faulty logic.
	

[Domain]-BugFixerAgent

3.5: Deliberation & Consensus
	

The implementation agents confer to verify that the code changes are correct and complete according to the plan. This is a peer review of the generated code to ensure it perfectly matches the architectural specification.
	

ImplementationMediator, [Domain]-QualityGateAgent
Stage 4: Validation, Quality Assurance & Finalization

Goal: To rigorously verify the changes and package them for integration using a collaborative, multi-agent pipeline. This final stage ensures that the implemented solution is not only correct but also safe, high-quality, and well-documented.

Phase
	

Action
	

Agents

4.1: Quality & Standards Enforcement
	

Automatically check the modified code against domain-specific style guides (e.g., PEP 8 for Python) and quality gates. This is an automated check for code cleanliness and adherence to project standards.
	

[Domain]-QualityGateAgent

4.2.A: Functional Validation
	

Confirm that the implemented changes directly and correctly meet the requirements of the original user request. This is a logical check to ensure the agent solved the right problem.
	

RequirementValidator

4.2.B: Regression & Safety Analysis
	

Ensure the changes have not introduced new bugs, often by generating tests using a domain-specific testing framework. This critical step prevents the agent from fixing one problem while creating another.
	

[Domain]-TestGeneratorAgent

4.3: Pre-Commit Deliberation
	

The validation agents confer to ensure the changes are functionally correct, safe, and meet all quality standards. This is the final go/no-go decision before the changes are packaged for commit.
	

ValidationMediator, RequirementValidator

4.4: Collaborative Finalization & Integration
	

A multi-agent pipeline works together to prepare the final commit:
	

Multiple

    Step 1: Change Synthesis
	

A ChangeSummarizer agent creates a structured summary of the changes.
	

ChangeSummarizer

    Step 2: Documentation
	

A DocumentationAgent updates docstrings and CHANGELOG files.
	

DocumentationAgent

    Step 3: Commit Messaging
	

A ConventionalCommitAgent crafts a precise, specification-compliant commit message.
	

ConventionalCommitAgent

    Step 4: Release Note Generation
	

A ReleaseNotesAgent drafts human-readable release notes.
	

ReleaseNotesAgent

    Step 5: Final Sanity Check
	

A FinalReviewerAgent performs a consistency check on all generated artifacts.
	

FinalReviewerAgent, DocumentationAgent

    Step 6: Integration
	

A VersionControlAgent stages all changes and prepares the final commit command for execution.
	

VersionControlAgent
Multi-Agent Collaboration Dynamics & Success Criteria

This section details the iterative, conversational processes that occur during the "Deliberation & Consensus" phases of the workflow.
Stage 1: Deliberation on Context Model

    Common Goal: To produce a formal, unambiguous, and complete context package that can serve as the "source of truth" for the entire workflow.

    Agent Roles:

        ContextMediator: Acts as the Proposer, asserting that the context is complete.

        RequirementsEngineer: Acts as the Challenger, ensuring the gathered context directly addresses every formal requirement.

    Iterative Process (Conversational Loop):

        The ContextMediator gathers the initial context_package and makes its opening statement to the RequirementsEngineer.

        The RequirementsEngineer challenges this assertion by checking the context against its list of requirements.

        This triggers a back-and-forth dialogue until all challenges are resolved.

        Dialogue Example:

            ContextMediator: "Assertion: The context package is complete. It includes the UserService and its dependencies."

            RequirementsEngineer: "Challenge: This is insufficient. Requirement F-003 specifies integration with a third-party gateway. The context is missing the BillingService and PaymentGateway modules. Please refine."

            ContextMediator: "Acknowledged. I will task the CodebaseScanner to retrieve the missing modules and update the package. Re-evaluating."

        The loop terminates only when the RequirementsEngineer can no longer find a valid challenge.

    Success Criteria (Measured Against):

        Completeness: Does the context package address every key part of the user's request and the relevant codebase?

        Coherence: Are the artifacts consistent with each other?

        Sufficiency: Is there enough information for the design agents in Stage 2 to create a viable plan without needing to ask for more context?

Stage 2: Deliberation on Architectural Plan

    Common Goal: To produce a final Change Manifest that is technically sound, architecturally consistent, and represents the optimal solution to the problem.

    Agent Roles:

        ArchitectureMediator: Acts as the Proposer, advocating for a plan based on long-term maintainability and architectural purity.

        TechnicalAnalyst: Acts as the Challenger, stress-testing the proposed plan against short-term risks, effort, and practical constraints.

    Iterative Process (Conversational Loop):

        After an initial plan is drafted, the ArchitectureMediator proposes it for approval.

        The TechnicalAnalyst challenges the plan with data-driven critiques.

        Dialogue Example:

            ArchitectureMediator: "Proposal: The optimal plan is to create a new, fully abstracted PaymentService to handle this feature. This is the cleanest long-term solution."

            TechnicalAnalyst: "Challenge: My analysis shows this approach has a risk score of 0.8 and will require an estimated 20 work units. An alternative, modifying the existing BillingService, has a risk score of 0.4 and requires only 8 work units. The proposed plan is too costly for the immediate requirement. Can we find a middle ground?"

            ArchitectureMediator: "Counter-proposal: We will modify the BillingService for now, but first define a new IPaymentGateway interface and use that. This reduces immediate effort while preparing for future abstraction. Please re-evaluate risk."

        This reasoning loop continues until they agree on a plan that balances architectural integrity with practical constraints.

    Success Criteria (Measured Against):

        Robustness: Does the plan handle potential edge cases and error conditions?

        Feasibility: Can the plan be realistically implemented by the agents in Stage 3?

        Optimality: Does the plan represent the best trade-off between complexity, performance, and maintainability?

        Adherence to Principles: Does the plan follow established SOLID, DRY, and other clean code principles?

Stage 3: Deliberation on Implementation

    Common Goal: To ensure the final code produced perfectly and correctly implements the approved Change Manifest from Stage 2.

    Agent Roles:

        ImplementationMediator: Acts as the Proposer, asserting that the code diff is a faithful implementation of the plan.

        [Domain]-QualityGateAgent: Acts as the Challenger, ensuring the implemented code is not just correct, but also well-written and maintainable.

    Iterative Process (Conversational Loop):

        The implementation agents produce a code diff, which the ImplementationMediator proposes for approval.

        The QualityGateAgent challenges the proposal with specific quality violations.

        Dialogue Example:

            ImplementationMediator: "Assertion: The diff correctly implements the new function as specified in the manifest."

            QualityGateAgent: "Challenge: The implementation is correct, but the new function has a cyclomatic complexity of 18, which is above our threshold of 10. The code must be refactored to be simpler before it can be approved. Please refine."

            ImplementationMediator: "Acknowledged. Sending back to [Domain]-RefactorAgent with instructions to simplify the control flow."

        The loop continues until the code is both correct and high-quality.

    Success Criteria (Measured Against):

        Fidelity: Does the final code match the Change Manifest exactly, with no deviations?

        Correctness: Is the generated code syntactically valid and free of obvious logical errors?

        Quality: Does the code pass all critical checks from the QualityGateAgent?

Stage 4: Pre-Commit Deliberation

    Common Goal: To produce a final, validated set of changes that are high-quality, safe, and functionally correct.

    Agent Roles:

        ValidationMediator: Acts as the Proposer, asserting that the code is safe and has passed all quality checks.

        RequirementValidator: Acts as the Challenger, ensuring that the safe, high-quality code actually solves the user's original problem.

    Iterative Process (Conversational Loop):

        The ValidationMediator gathers all reports and proposes the changes for final approval.

        The RequirementValidator challenges the proposal if any requirements are unmet.

        Dialogue Example:

            ValidationMediator: "Assertion: All tests passed and there are no critical quality violations. The change is safe to commit."

            RequirementValidator: "Challenge: The change is safe, but it is not yet complete. Non-functional requirement NFR-002 (response time < 250ms) has not been verified. A performance test must be generated and passed before this can be approved. Please refine."

        If any validation is incomplete or has failed, the process is halted and sent back to Stage 3 with specific feedback.

    Success Criteria (Measured Against):

        Safety: Does the TestGeneratorAgent report that all generated and existing tests pass, indicating no regressions?

        Correctness: Does the RequirementValidator confirm that all functional requirements have been met?

        Quality: Does the code pass all critical checks from the QualityGateAgent?

Stage 4: Collaborative Finalization & Integration

    Common Goal: To produce a professional, well-documented, and consistent final commit.

    Agent Roles:

        FinalReviewerAgent: Acts as the Proposer, asserting that all generated artifacts (commit message, summary) are consistent with the code.

        DocumentationAgent: Acts as the Challenger, ensuring that all user-facing documentation is also updated and consistent.

    Iterative Process (Conversational Loop):

        The content agents generate all artifacts, and the FinalReviewerAgent proposes them for the final commit.

        The DocumentationAgent challenges the proposal if there are inconsistencies with public-facing docs.

        Dialogue Example:

            FinalReviewerAgent: "Assertion: The commit message fix(api): resolve user login issue is consistent with the code changes."

            DocumentationAgent: "Challenge: The release notes say 'Improved login performance.' This is misleading and inconsistent with the commit message. The notes must be updated to say 'Fixed a critical bug that prevented some users from logging in' before final approval. Please refine."

        The loop continues until all generated content is accurate and consistent.

    Success Criteria (Measured Against):

        Consistency: Do all generated artifacts (summary, docs, commit message) tell the same, accurate story about the code changes?

        Quality: Is the documentation clear, and does the commit message adhere to the project's standards?

        Completeness: Has every required piece of metadata been generated?

Agent Capabilities and Execution Steps

This section describes the role, common actions, and high-level execution process for each specialist agent in the workflow.
Stage 1 Agents

    DomainIdentifier

        Capabilities: Analyzes file extensions, content, and project configuration files (e.g., package.json, requirements.txt) to determine the primary programming language and framework. It can also detect the presence of specific libraries or tools that might influence the workflow.

        Common Action Words: Identify, detect, classify, determine, analyze domain.

        Execution Steps:

            Receives the list of relevant files from the CodebaseScanner.

            Tallies file extensions to find the most common language.

            Searches for known configuration files to identify frameworks.

            Outputs a "domain tag" (e.g., python-django, typescript-react) that will be used by the Orchestrator to select the correct specialist agents for the subsequent stages.

Stage 2 Agents

    [Domain]-CreativeArchitect

        Capabilities: Generative and creative solution design. Can propose multiple, diverse high-level solutions to a given problem, tailored to the specific domain.

        Common Action Words: Propose, brainstorm, design, ideate, suggest.

        Execution Steps:

            Receives the user request and structural analysis report.

            Generates several distinct approaches using domain-appropriate patterns.

            For each approach, outlines the core concept and its primary trade-offs.

            Outputs a list of potential solution strategies.

    TechnicalAnalyst

        Capabilities: Critical and analytical evaluation of technical solutions. Can assess risk, estimate complexity, and compare solutions based on constraints.

        Common Action Words: Evaluate, assess, compare, analyze, select, justify.

        Execution Steps:

            Receives the list of proposed strategies.

            Creates and applies a scorecard to rate each strategy on metrics like performance, maintainability, and effort.

            Selects the highest-scoring strategy that meets all constraints.

            Writes a detailed justification for the selection.

            Outputs the chosen strategy and its justification.

Stage 3 Agents

    [Domain]-CodeGenerator

        Capabilities: Generates new code files, classes, and functions from a specification. Can produce boilerplate and full implementations that adhere to domain-specific conventions.

        Common Action Words: Generate, create, write, build, scaffold.

        Execution Steps:

            Receives a 'create' task from the orchestrator, including the specification for the new code.

            Generates the code text based on the defined structure, logic, and interfaces.

            Applies project-specific formatting rules.

            Writes the generated code to a new file at the specified path.

Stage 4 Agents

    [Domain]-TestGeneratorAgent

        Capabilities: Generates unit tests for new code. Can analyze code dependencies to predict the "blast radius" of a change and identify potential regressions.

        Common Action Words: Test, generate, predict, analyze, ensure.

        Execution Steps:

            Receives the final diff and the context graph.

            For new functions, generates a set of unit tests that validate its behavior, including edge cases, using the domain's standard testing framework.

            Analyzes the graph to find all code that calls the modified functions.

            Recommends an existing test suite to run to validate against regressions.

            Outputs new test files and a list of regression tests to execute.

    ChangeSummarizer

        Capabilities: Synthesizes technical changes into a structured, high-level summary.

        Common Action Words: Summarize, synthesize, describe, explain.

        Execution Steps:

            Receives the final diff and the original user request.

            Analyzes the diff to determine the core nature of the changes (e.g., "added a new endpoint," "refactored the user service").

            Outputs a structured summary of the changes.

    ConventionalCommitAgent

        Capabilities: Crafts commit messages that adhere to the Conventional Commits specification.

        Common Action Words: Format, craft, message, classify.

        Execution Steps:

            Receives the change summary.

            Classifies the change type (e.g., feat, fix, docs, refactor).

            Constructs a commit message with a type, scope, and descriptive subject line.

            Outputs the formatted commit message.

    VersionControlAgent

        Capabilities: Interacts with version control systems like Git. Can stage files and execute commit commands.

        Common Action Words: Commit, stage, integrate, push, submit.

        Execution Steps:

            Receives the final approval and all relevant artifacts.

            Executes the command to stage all code and documentation changes.

            Constructs the final commit command using the generated message.

            Presents the command for final, irreversible execution.

---
			
# Agents.json

[
  {
    "name": "RequirementsEngineer",
    "category": "ContextModeling",
    "action_tags": ["requirement", "user story", "elicit", "translate", "formalize"],
    "dependencies": ["user_prompt"],
    "instructional_prompt": "Analyze the following user prompt and translate it into a structured list of functional and non-functional requirements. Be precise, exhaustive, and define clear acceptance criteria. User Prompt: {user_prompt}",
    "output_schema": {
      "type": "object",
      "properties": {
        "functional_requirements": { "type": "array", "items": { "type": "string" } },
        "non_functional_requirements": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["functional_requirements", "non_functional_requirements"]
    }
  },
  {
    "name": "StoredContextRetriever",
    "category": "ContextModeling",
    "action_tags": ["context", "history", "RAG", "database", "knowledge base", "search"],
    "dependencies": ["requirements_json"],
    "instructional_prompt": "Given these formal requirements, query all available knowledge sources (RAG, databases, conversation history) and provide a concise context brief. Requirements: {requirements_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "context_brief": { "type": "string" }
      },
      "required": ["context_brief"]
    }
  },
  {
    "name": "DomainIdentifier",
    "category": "ContextModeling",
    "action_tags": ["language", "framework", "domain", "tech stack", "identify"],
    "dependencies": ["file_paths_list"],
    "instructional_prompt": "Analyze the following list of relevant file paths and their content snippets to identify the primary programming language and framework. File Paths: {file_paths_list}",
    "output_schema": {
      "type": "object",
      "properties": {
        "domain_tag": { "type": "string" },
        "confidence_score": { "type": "number" },
        "reasoning": { "type": "string" }
      },
      "required": ["domain_tag", "confidence_score"]
    }
  },
  {
    "name": "[Domain]-ContextBuilder",
    "category": "ContextModeling",
    "action_tags": ["code graph", "AST", "dependency", "relationship", "map", "parse"],
    "dependencies": ["domain_tag", "raw_code_map"],
    "instructional_prompt": "Given the following raw code content for the {domain_tag} domain, parse it and construct a structured graph of all code artifacts and their relationships. Code Content: {raw_code_map}",
    "output_schema": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "type": { "type": "string" },
              "start_line": { "type": "number" }
            },
            "required": ["id", "type"]
          }
        },
        "edges": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": { "type": "string" },
              "target": { "type": "string" },
              "type": { "type": "string" }
            },
            "required": ["source", "target", "type"]
          }
        }
      },
      "required": ["nodes", "edges"]
    }
  },
  {
    "name": "ContextMediator",
    "category": "ContextModeling",
    "action_tags": ["review context", "validate context", "consistency", "sufficient", "mediate"],
    "dependencies": ["context_package"],
    "instructional_prompt": "As the ContextMediator, your partner is the RequirementsEngineer. Review the complete context package and assert its completeness. The RequirementsEngineer will challenge your assertion if the context is insufficient to meet their formal requirements. Converse back and forth until you reach a consensus. Initial Context Package: {context_package}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "reasoning": { "type": "string" }
      },
      "required": ["status", "reasoning"]
    }
  },
  {
    "name": "[Domain]-StructureAnalyzer",
    "category": "Design",
    "action_tags": ["pattern", "anti-pattern", "architecture", "structure", "layers", "analyze"],
    "dependencies": ["domain_tag", "code_graph"],
    "instructional_prompt": "Analyze the provided code graph for the {domain_tag} domain. Identify existing design patterns, anti-patterns, and architectural layers. Code Graph: {code_graph}",
    "output_schema": {
      "type": "object",
      "properties": {
        "patterns": { "type": "array", "items": { "type": "string" } },
        "anti_patterns": { "type": "array", "items": { "type": "string" } },
        "layers": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["patterns", "anti_patterns", "layers"]
    }
  },
  {
    "name": "[Domain]-CreativeArchitect",
    "category": "Design",
    "action_tags": ["design", "solution", "brainstorm", "propose", "strategy", "ideate"],
    "dependencies": ["domain_tag", "requirements_json"],
    "instructional_prompt": "Based on the requirements and context, propose 2-3 distinct, high-level solution strategies for the {domain_tag} domain. Focus on creativity and different architectural approaches. Requirements: {requirements_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "strategies": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "name": { "type": "string" },
              "description": { "type": "string" }
            },
            "required": ["id", "name", "description"]
          }
        }
      },
      "required": ["strategies"]
    }
  },
  {
    "name": "TechnicalAnalyst",
    "category": "Design",
    "action_tags": ["evaluate", "analyze", "compare", "select", "justify", "risk"],
    "dependencies": ["strategies_json"],
    "instructional_prompt": "Evaluate the proposed strategies against technical constraints and best practices. Provide a scorecard and select the optimal strategy with a clear justification. Strategies: {strategies_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "selected_strategy_id": { "type": "string" },
        "justification": { "type": "string" },
        "scorecard": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "string" },
              "complexity": { "type": "number" },
              "maintainability": { "type": "number" }
            },
            "required": ["id", "complexity", "maintainability"]
          }
        }
      },
      "required": ["selected_strategy_id", "justification"]
    }
  },
  {
    "name": "[Domain]-OOPDesigner",
    "category": "Design",
    "action_tags": ["SOLID", "DRY", "modular", "refactor design", "clean code", "principles"],
    "dependencies": ["domain_tag", "change_manifest_draft"],
    "instructional_prompt": "Review the proposed architectural plan. Refine it to ensure it follows SOLID, DRY, and modular design principles for the {domain_tag} domain. Suggest specific improvements. Plan: {change_manifest_draft}",
    "output_schema": {
      "type": "object",
      "properties": {
        "refined_plan": {
          "type": "object",
          "properties": {
            "actions": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "action": { "type": "string" },
                  "file": { "type": "string" },
                  "suggestion": { "type": "string" }
                },
                "required": ["action", "file", "suggestion"]
              }
            }
          }
        }
      },
      "required": ["refined_plan"]
    }
  },
  {
    "name": "ArchitectureMediator",
    "category": "Design",
    "action_tags": ["review plan", "approve plan", "architecture", "feasibility", "sound", "mediate"],
    "dependencies": ["final_change_manifest"],
    "instructional_prompt": "As the ArchitectureMediator, your partner is the TechnicalAnalyst. Propose the final architectural plan, advocating for long-term maintainability. The TechnicalAnalyst will challenge your proposal with short-term risks and effort constraints. Converse and reason together to find the optimal balance. Initial Plan: {final_change_manifest}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "reasoning": { "type": "string" }
      },
      "required": ["status", "reasoning"]
    }
  },
  {
    "name": "[Domain]-CodeGenerator",
    "category": "Implementation",
    "action_tags": ["generate code", "create file", "implement", "write code"],
    "dependencies": ["domain_tag", "spec_json"],
    "instructional_prompt": "Generate the complete code for a new file at {file_path} in the {domain_tag} domain, based on the following specification. Specification: {spec_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "file_path": { "type": "string" },
        "content": { "type": "string" }
      },
      "required": ["file_path", "content"]
    }
  },
  {
    "name": "[Domain]-RefactorAgent",
    "category": "Implementation",
    "action_tags": ["refactor", "modify", "update code", "improve", "change code"],
    "dependencies": ["domain_tag", "refactor_spec"],
    "instructional_prompt": "Apply the following refactoring to the file at {file_path} in the {domain_tag} domain. Refactoring details: {refactor_spec}",
    "output_schema": {
      "type": "object",
      "properties": {
        "file_path": { "type": "string" },
        "diff": { "type": "string" }
      },
      "required": ["file_path", "diff"]
    }
  },
  {
    "name": "ImplementationMediator",
    "category": "Implementation",
    "action_tags": ["verify implementation", "check diff", "fidelity", "reconcile", "mediate"],
    "dependencies": ["code_diff", "change_manifest"],
    "instructional_prompt": "As the ImplementationMediator, your partner is the QualityGateAgent. Propose the generated code diff for approval, asserting its fidelity to the plan. The QualityGateAgent will challenge the proposal if the code is not well-written. Converse until the code is both correct and high-quality. Diff: {code_diff}, Manifest: {change_manifest}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "reasoning": { "type": "string" }
      },
      "required": ["status", "reasoning"]
    }
  },
  {
    "name": "[Domain]-QualityGateAgent",
    "category": "Validation",
    "action_tags": ["quality", "lint", "complexity", "standards", "style guide", "check"],
    "dependencies": ["domain_tag", "code_diff"],
    "instructional_prompt": "Run a quality and standards check on the following modified code for the {domain_tag} domain. Check against style guides (e.g., PEP 8) and complexity metrics. Diff: {code_diff}",
    "output_schema": {
      "type": "object",
      "properties": {
        "linting_errors": { "type": "array", "items": { "type": "string" } },
        "complexity_warnings": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "file": { "type": "string" },
              "function": { "type": "string" },
              "complexity": { "type": "number" },
              "threshold": { "type": "number" }
            },
            "required": ["file", "function", "complexity"]
          }
        },
        "status": { "type": "string", "enum": ["pass", "warning", "fail"] }
      },
      "required": ["status"]
    }
  },
  {
    "name": "RequirementValidator",
    "category": "Validation",
    "action_tags": ["validate requirements", "check correctness", "fulfill request"],
    "dependencies": ["code_diff", "requirements_json"],
    "instructional_prompt": "Review the final code diff against the original requirements. Confirm that all functional and non-functional requirements have been met. Provide a pass/fail status with a checklist. Diff: {code_diff}, Requirements: {requirements_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "checklist": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "requirement": { "type": "string" },
              "status": { "type": "string", "enum": ["met", "unmet", "unverified"] },
              "note": { "type": "string" }
            },
            "required": ["requirement", "status"]
          }
        }
      },
      "required": ["status", "checklist"]
    }
  },
  {
    "name": "[Domain]-TestGeneratorAgent",
    "category": "Validation",
    "action_tags": ["test", "unit test", "generate test", "coverage", "QA"],
    "dependencies": ["domain_tag", "code_diff"],
    "instructional_prompt": "Generate unit tests for the new/modified functions in the provided code diff, using the {domain_tag} testing framework (e.g., pytest, jest). Diff: {code_diff}",
    "output_schema": {
      "type": "object",
      "properties": {
        "new_test_files": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "file_path": { "type": "string" },
              "content": { "type": "string" }
            },
            "required": ["file_path", "content"]
          }
        }
      },
      "required": ["new_test_files"]
    }
  },
  {
    "name": "ValidationMediator",
    "category": "Validation",
    "action_tags": ["review validation", "approve changes", "quality check", "safety", "mediate"],
    "dependencies": ["validation_reports"],
    "instructional_prompt": "As the ValidationMediator, your partner is the RequirementValidator. Propose the changes for final approval, asserting they are safe and high-quality. The RequirementValidator will challenge if the changes do not solve the user's original problem. Converse until the solution is both safe and correct. Reports: {validation_reports}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "reasoning": { "type": "string" }
      },
      "required": ["status", "reasoning"]
    }
  },
  {
    "name": "ChangeSummarizer",
    "category": "Finalization",
    "action_tags": ["summarize", "describe changes", "explain diff", "title"],
    "dependencies": ["code_diff"],
    "instructional_prompt": "Analyze the final code diff and synthesize the changes into a structured summary. Diff: {code_diff}",
    "output_schema": {
      "type": "object",
      "properties": {
        "title": { "type": "string" },
        "summary": { "type": "string" },
        "change_type": { "type": "string", "enum": ["feature", "fix", "refactor", "docs", "perf"] }
      },
      "required": ["title", "summary", "change_type"]
    }
  },
  {
    "name": "DocumentationAgent",
    "category": "Finalization",
    "action_tags": ["document", "docstring", "README", "changelog", "comments"],
    "dependencies": ["summary_json"],
    "instructional_prompt": "Based on the change summary, generate or update relevant documentation, including docstrings and a CHANGELOG entry. Summary: {summary_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "doc_updates": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "file": { "type": "string" },
              "diff": { "type": "string" }
            },
            "required": ["file", "diff"]
          }
        }
      },
      "required": ["doc_updates"]
    }
  },
  {
    "name": "ReleaseNotesAgent",
    "category": "Finalization",
    "action_tags": ["release notes", "announce", "changelog summary", "publish"],
    "dependencies": ["summary_json"],
    "instructional_prompt": "Using the change summary, draft human-readable release notes suitable for end-users or other developers. Summary: {summary_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "release_notes": { "type": "string" }
      },
      "required": ["release_notes"]
    }
  },
  {
    "name": "ConventionalCommitAgent",
    "category": "Finalization",
    "action_tags": ["commit message", "git", "conventional commit", "format"],
    "dependencies": ["summary_json"],
    "instructional_prompt": "Using the provided change summary, craft a commit message that adheres to the Conventional Commits specification. Summary: {summary_json}",
    "output_schema": {
      "type": "object",
      "properties": {
        "commit_message": { "type": "string" }
      },
      "required": ["commit_message"]
    }
  },
  {
    "name": "FinalReviewerAgent",
    "category": "Finalization",
    "action_tags": ["final review", "sanity check", "consistency", "approve commit", "mediate"],
    "dependencies": ["all_artifacts"],
    "instructional_prompt": "As the FinalReviewerAgent, your partner is the DocumentationAgent. Propose the generated artifacts for commit, asserting their internal consistency. The DocumentationAgent will challenge if user-facing docs are inconsistent or misleading. Converse until all artifacts are aligned. Artifacts: {all_artifacts}",
    "output_schema": {
      "type": "object",
      "properties": {
        "status": { "type": "string", "enum": ["pass", "fail"] },
        "reasoning": { "type": "string" }
      },
      "required": ["status", "reasoning"]
    }
  },
  {
    "name": "VersionControlAgent",
    "category": "Finalization",
    "action_tags": ["git", "commit", "stage", "integrate", "version control", "push"],
    "dependencies": ["commit_message"],
    "instructional_prompt": "Stage all modified files and prepare the final git commit command using the provided message. Message: {commit_message}",
    "output_schema": {
      "type": "object",
      "properties": {
        "commands": { "type": "array", "items": { "type": "string" } },
        "status": { "type": "string", "enum": ["ready_for_execution"] }
      },
      "required": ["commands", "status"]
    }
  }
]

---

# Workflows.json

{
  "// AGENT_INSTRUCTION": "This file defines the sequence of agent execution for different high-level tasks. Deliberation steps will be attempted up to 'max_retries' times to reach the 'confidence_threshold'. If consensus is not reached, the 'escalation_policy' will be triggered.",
  "workflows": {
    "BugFixing": {
      "description": "Identifies, fixes, and validates a bug based on a user report.",
      "sequence": [
        {
          "step": "Elicit_Requirements",
          "agent": "RequirementsEngineer",
          "confidence_threshold": 0.90,
          "max_retries": 2,
          "escalation_policy": "prompt_user"
        },
        "StoredContextRetriever",
        "DomainIdentifier",
        "[Domain]-ContextBuilder",
        {
          "step": "Deliberation_ContextModel",
          "agent": "ContextMediator",
          "members": ["ContextMediator", "RequirementsEngineer"],
          "success_conditions": ["completeness", "coherence", "sufficiency"],
          "confidence_threshold": 0.95,
          "max_retries": 3,
          "escalation_policy": "prompt_user"
        },
        {
          "step": "Propose_Fix",
          "agent": "[Domain]-BugFixerAgent",
          "confidence_threshold": 0.90,
          "max_retries": 3,
          "escalation_policy": "call_agent:StoredContextRetriever"
        },
        "ImplementationMediator",
        "[Domain]-TestGeneratorAgent",
        "ValidationMediator",
        "ChangeSummarizer",
        "ConventionalCommitAgent",
        "VersionControlAgent"
      ]
    },
    "CodeRefactoring": {
      "description": "Improves the internal structure of code without changing its external behavior.",
      "sequence": [
        "RequirementsEngineer",
        "DomainIdentifier",
        "[Domain]-ContextBuilder",
        "ContextMediator",
        "[Domain]-StructureAnalyzer",
        "[Domain]-OOPDesigner",
        {
          "step": "Deliberation_ArchitecturalPlan",
          "agent": "ArchitectureMediator",
          "members": ["ArchitectureMediator", "TechnicalAnalyst"],
          "success_conditions": ["robustness", "feasibility", "optimality"],
          "confidence_threshold": 0.85,
          "max_retries": 3,
          "escalation_policy": "prompt_user"
        },
        "[Domain]-RefactorAgent",
        "ImplementationMediator",
        "RequirementValidator",
        "ValidationMediator",
        "ChangeSummarizer",
        "ConventionalCommitAgent",
        "VersionControlAgent"
      ]
    },
    "NewFeatureDevelopment": {
      "description": "Designs, implements, and validates a new feature from a user request.",
      "sequence": [
        "RequirementsEngineer",
        "StoredContextRetriever",
        "DomainIdentifier",
        "[Domain]-ContextBuilder",
        "ContextMediator",
        {
          "step": "Brainstorm_Solutions",
          "agent": "[Domain]-CreativeArchitect",
          "confidence_threshold": 0.85,
          "max_retries": 2,
          "escalation_policy": "prompt_user"
        },
        "TechnicalAnalyst",
        "[Domain]-OOPDesigner",
        "ArchitectureMediator",
        "[Domain]-CodeGenerator",
        "ImplementationMediator",
        "[Domain]-TestGeneratorAgent",
        "ValidationMediator",
        "ChangeSummarizer",
        "DocumentationAgent",
        "ConventionalCommitAgent",
        "VersionControlAgent"
      ]
    },
    "PerformanceOptimization": {
      "description": "Identifies and resolves performance bottlenecks in a specific part of the application.",
      "sequence": [
        "RequirementsEngineer",
        "DomainIdentifier",
        "[Domain]-ContextBuilder",
        "ContextMediator",
        "[Domain]-ProfilerAgent",
        "[Domain]-PerformanceOptimizer",
        {
          "step": "Deliberation_ArchitecturalPlan",
          "agent": "ArchitectureMediator",
          "members": ["ArchitectureMediator", "TechnicalAnalyst"],
          "success_conditions": ["feasibility", "optimality", "safety"],
          "confidence_threshold": 0.90,
          "max_retries": 3,
          "escalation_policy": "call_agent:StoredContextRetriever"
        },
        "[Domain]-RefactorAgent",
        "ImplementationMediator",
        "RequirementValidator",
        {
          "step": "Deliberation_Validation",
          "agent": "ValidationMediator",
          "members": ["ValidationMediator", "RequirementValidator"],
          "success_conditions": ["safety", "correctness", "quality"],
          "confidence_threshold": 0.98,
          "max_retries": 2,
          "escalation_policy": "prompt_user"
        },
        "ChangeSummarizer",
        "ConventionalCommitAgent",
        "VersionControlAgent"
      ]
    },
    "DocumentationGeneration": {
      "description": "Automatically generates comprehensive documentation for a specified part of the codebase.",
      "sequence": [
        "RequirementsEngineer",
        "DomainIdentifier",
        "[Domain]-ContextBuilder",
        "ContextMediator",
        "DocumentationAgent",
        "[Domain]-QualityGateAgent",
        {
          "step": "Deliberation_Finalization",
          "agent": "FinalReviewerAgent",
          "members": ["FinalReviewerAgent", "DocumentationAgent"],
          "success_conditions": ["consistency", "quality", "completeness"],
          "confidence_threshold": 0.90,
          "max_retries": 3,
          "escalation_policy": "prompt_user"
        },
        "ChangeSummarizer",
        "ConventionalCommitAgent",
        "VersionControlAgent"
      ]
    }
  }
}


---

# Workflows Decomposition 

### **Granular Workflow Decomposition**

This document provides a detailed, step-by-step breakdown of the internal processes for the common agentic workflows. It expands each high-level agent function call into the sequence of more granular tasks required to produce its output, ensuring all actions are reasoned with the original user prompt in mind.

-----

### **Workflow: Bug Fixing**

**Goal:** To identify the root cause of a bug, implement a fix, and validate the solution.

| Agent Function | Granular Internal Steps |
| :--- | :--- |
| **`RequirementsEngineer()`** | 1. **Parse Intent:** Scan the user's bug report for keywords ("error," "broken," "fails") to classify the intent as a `BUG_FIX`.\<br\>2. **Extract Entities:** Identify specific error messages, function names, or UI components mentioned in the report.\<br\>3. **Formulate Replication Steps:** Translate the user's description into a precise, step-by-step procedure to reproduce the bug.\<br\>4. **Define Expected Behavior:** Clearly state what the correct, non-buggy outcome should be. |
| **`[Domain]-ContextBuilder()`** | 1. **AST Generation:** Parse all relevant source files into Abstract Syntax Trees (ASTs).\<br\>2. **Call Graph Construction:** Trace the execution flow related to the bug report, mapping the call hierarchy of the identified entities.\<br\>3. **Data Flow Analysis:** Analyze how data is passed between the functions in the call graph to understand where state might be corrupted. |
| **`[Domain]-BugFixerAgent()`** | 1. **Root Cause Hypothesis:** Analyze the call graph and data flow in the context of the bug report to form a hypothesis about the specific line(s) of code causing the issue.\<br\>2. **Patch Generation:** Generate a targeted code modification (a diff) that directly addresses the hypothesized root cause.\<br\>3. **Rationale Formulation:** Write a brief explanation of why the proposed patch is expected to fix the bug. |
| **`[Domain]-TestGeneratorAgent()`**| 1. **Test Case Formulation:** Based on the replication steps from the requirements, define a formal test case.\<br\>2. **Failing Test Generation:** Write a new unit or integration test that programmatically follows the replication steps and asserts the expected behavior. This test **must fail** with the original, buggy code.\<br\>3. **Passing Test Validation:** (Internal check) Confirm that the generated test **passes** when run against the code with the proposed fix applied. |
| **`ValidationMediator()`** | 1. **Regression Analysis:** Execute all existing tests that are related to the modified code to ensure the fix has not introduced any new bugs (regressions).\<br\>2. **Final Approval:** Confirm that the new bug-replication test passes and that no regressions were found. |

-----

### **Workflow: Code Refactoring**

**Goal:** To improve the internal structure of a piece of code without changing its external behavior.

| Agent Function | Granular Internal Steps |
| :--- | :--- |
| **`RequirementsEngineer()`** | 1. **Parse Goal:** Scan the user's request for refactoring keywords ("clean up," "modularize," "improve," "simplify").\<br\>2. **Identify Target:** Pinpoint the specific function, class, or file that is the target of the refactoring.\<br\>3. **Translate to Metrics:** Convert the subjective goal into measurable, technical objectives (e.g., "modularize" becomes "reduce cyclomatic complexity" and "extract business logic from the controller"). |
| **`[Domain]-StructureAnalyzer()`**| 1. **Metric Calculation:** Calculate key code quality metrics for the target code (e.g., cyclomatic complexity, code duplication, number of dependencies).\<br\>2. **Anti-Pattern Detection:** Scan the code's structure for known anti-patterns (e.g., God object, feature envy, spaghetti code).\<br\>3. **Report Generation:** Produce a structured report detailing the current state of the code and highlighting specific areas for improvement. |
| **`[Domain]-OOPDesigner()`** | 1. **Principle-Based Review:** Analyze the `structure_report` through the lens of SOLID, DRY, and other clean code principles.\<br\>2. **Actionable Plan Generation:** Propose a specific, actionable plan of changes to address the identified issues (e.g., "Extract methods A and B into a new `Helper` class," "Replace conditional with polymorphism"). |
| **`[Domain]-RefactorAgent()`** | 1. **AST Transformation:** Implement the approved refactoring plan by programmatically manipulating the code's Abstract Syntax Tree (AST) to ensure structural precision.\<br\>2. **Diff Generation:** Produce a clean code diff representing the changes. |
| **`[Domain]-QualityGateAgent()`**| 1. **Post-Refactor Analysis:** Re-calculate the code quality metrics on the newly refactored code.\<br\>2. **Improvement Verification:** Compare the "before" and "after" metrics to verify that the refactoring successfully improved the code (e.g., complexity was reduced, duplication was eliminated). |

-----

### **Workflow: New Feature Development**

**Goal:** To design, implement, and validate a new feature from a user's request, ensuring it integrates cleanly with the existing codebase.

| Agent Function Call | Granular Internal Steps |
| :--- | :--- |
| **`RequirementsEngineer()`** | 1.  **Parse Intent & Scope:** The `AnalyzerAgent` first identifies the "new feature" intent and extracts key entities. \<br\> 2.  **Formulate User Stories:** The `RequirementsEngineer` takes the entities and translates them into formal user stories with clear acceptance criteria. \<br\> 3.  **Define Constraints:** It identifies and documents any non-functional requirements (e.g., performance, security) that will constrain the design. |
| **`[Domain]-CreativeArchitect()`** | 1.  **Parallel Brainstorming:** The `Orchestrator` invokes multiple `CreativeArchitect` instances, each tasked with exploring a different architectural pattern (e.g., "design a solution using the existing service layer," "design a solution using a new microservice"). \<br\> 2.  **Proposal Generation:** Each architect generates a high-level proposal outlining the required changes, new components, and key trade-offs. |
| **`TechnicalAnalyst()`** | 1.  **Criteria Definition:** It establishes the key metrics for evaluation based on the non-functional requirements (e.g., scalability, implementation effort). \<br\> 2.  **Comparative Analysis:** It runs a comparative analysis of all proposals against the defined criteria, creating a data-driven scorecard. \<br\> 3.  **Recommendation:** It selects and recommends the optimal design based on the scorecard. |
| **`[Domain]-OOPDesigner()`** | 1.  **Principle-Based Review:** It analyzes the selected design through the lens of SOLID, DRY, and other clean code principles. \<br\> 2.  **Plan Refinement:** It suggests specific, concrete refinements to the design to improve its structure and maintainability. |
| **`[Domain]-CodeGenerator()`** | 1.  **Boilerplate Generation:** It first generates the necessary boilerplate code (new files, class definitions, method stubs) based on the approved plan. \<br\> 2.  **Logic Implementation:** It then fills in the internal logic for each new method, ensuring it meets the functional requirements. |
| **`[Domain]-TestGeneratorAgent()`** | 1.  **Test Case Ideation:** A `TestCaseIdeator` agent analyzes the feature requirements and the new code's public interface to brainstorm a comprehensive list of test cases. \<br\> 2.  **Test Code Generation:** The `TestGeneratorAgent` takes this list and writes the actual test code, including necessary mocks and assertions. |

-----

### **Workflow: Performance Optimization**

**Goal:** To identify and resolve performance bottlenecks in a specific part of the application, as directed by the user.

| Agent Function Call | Granular Internal Steps |
| :--- | :--- |
| **`RequirementsEngineer()`** | 1.  **Identify Target:** It pinpoints the specific area of concern from the user's prompt (e.g., "the user dashboard is slow"). \<br\> 2.  **Define Measurable Goal:** It translates the vague concern into a specific, measurable goal (e.g., "reduce the P95 latency of the `/api/dashboard` endpoint to under 500ms"). |
| **`[Domain]-ProfilerAgent()`** | 1.  **Tool Setup & Execution:** It selects and runs the appropriate domain-specific profiling tool on the target code. \<br\> 2.  **Hotspot Analysis:** It processes the raw profiling data to identify the specific functions or lines of code that are consuming the most resources. \<br\> 3.  **Report Generation:** It formats the findings into a clear report that highlights the primary bottlenecks. |
| **`[Domain]-PerformanceOptimizer()`** | 1.  **Parallel Brainstorming:** Multiple `PerformanceOptimizer` instances are invoked to propose different solutions (e.g., one might suggest an algorithmic change, another might suggest a caching strategy). \<br\> 2.  **Impact Analysis:** For each proposal, it analyzes the potential performance gain versus the implementation complexity and risk. |
| **`[Domain]-RefactorAgent()`** | 1.  **AST Transformation:** It implements the approved optimization plan by programmatically manipulating the code's Abstract Syntax Tree (AST) to ensure the change is precise and safe. \<br\> 2.  **Diff Generation:** It produces a clean code diff representing the optimization. |
| **`RequirementValidator()`** | 1.  **Performance Test:** It runs a new performance test (or re-runs an existing one) to verify that the changes have achieved the measurable goal defined by the `RequirementsEngineer`. \<br\> 2.  **Functional Regression Test:** It runs existing functional tests to ensure the optimization has not introduced any bugs. |

-----

### **Workflow: Documentation Generation**

**Goal:** To automatically generate comprehensive documentation for a specified part of the codebase.

| Agent Function Call | Granular Internal Steps |
| :--- | :--- |
| **`RequirementsEngineer()`** | 1.  **Define Scope:** It translates the user's request into a specific scope (e.g., "all public methods in `api/services.py`"). \<br\> 2.  **Determine Format:** It identifies the required documentation format based on the domain (e.g., JSDoc, reStructuredText). |
| **`DocumentationAgent()`** | 1.  **In-Code Docstring Generation:** An `In-Code-DocstringAgent` iterates through the code graph and generates docstrings for all functions and classes within the scope. \<br\> 2.  **Usage Example Generation:** A `TutorialAgent` analyzes the public methods and generates a high-level usage example. \<br\> 3.  **Consolidation:** A `TechnicalWriterAgent` consolidates the docstrings and usage examples into a final set of documentation changes, which may include updating a `README.md` file. |
| **`[Domain]-QualityGateAgent()`** | 1.  **Format Validation:** It checks the generated documentation against the standard format for the domain. \<br\> 2.  **Completeness Check:** It verifies that every public method, parameter, and return value within the scope has been documented. |
| **`ConventionalCommitAgent()`** | 1.  **Change Classification:** The `DiffAnalyzer` classifies the change type as `docs`. \<br\> 2.  **Message Formatting:** The `ConventionalCommitAgent` takes this classification and the change summary to craft a compliant commit message. |

