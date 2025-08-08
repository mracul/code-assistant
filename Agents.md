1. High-Level Architecture

This system employs a structured, four-phase workflow that is logged and orchestrated through a single, shared Markdown file (log.md). All agent outputs, conversations, and phase transitions are appended to this central document, creating a complete, chronological, and human-readable record of the project.

Core Principles:

    Single Source of Truth: The log.md file is the primary medium for state, communication, and history. Agents read from it to gain context and append to it to contribute their work.

    Chronological & Immutable Log: The log is append-only. Nothing is ever overwritten, providing a perfect audit trail.

    Hierarchical Headings: A structured heading system is used to differentiate between phases, repeated runs of phases (due to clarification loops), and individual agent outputs within each run.

2. The Markdown-Centric Workflow

The four phases (Definition, Deliberation, Implementation, Finalization) remain the same, but agent interaction is now mediated through the log.md.

Example log.md structure:

# Project Log: Create User Authentication API

## Phase 1: Definition - 1.0

### [RequirementsAgent] - 1.1
* **Functional:** User must be able to register, login, and logout.
* **Non-Functional:** API response time must be < 250ms.

### [ContextAgent] - 1.2
* **Files to Create:** `auth_controller.py`, `user_model.py`.

---
## Phase 2: Deliberation - 2.0

### [API_Design_Agent] - 2.0.1
```json
{
  "endpoints": {
    "/register": "POST",
    "/login": "POST"
  }
}

[SecurityAnalyst] - 2.0.2

Request to API_Design_Agent: The design lacks a password hashing mechanism. Please specify one.
[API_Design_Agent] - 2.0.3

Response to SecurityAnalyst: Acknowledged. Will use bcrypt for password hashing.

{
  "endpoints": { "...": "..." },
  "security": { "password_hashing": "bcrypt" }
}

Phase 3: Implementation - 3.0
[SpecialistProgrammerAgent] - 3.0.1

Request to API_Design_Agent: The /login endpoint does not specify the structure of the JWT to be returned. Please clarify.
Phase 2: Deliberation - 2.1 (Clarification Round)
[ProjectManagerAgent] - 2.1.0

    Reason: Clarification requested by SpecialistProgrammerAgent.

    Goal: Resolve JWT structure for the /login endpoint.

...and so on.


---

### **3. Core Components & Data Structures**

#### **3.1. The `shared_state` Schema**

The `shared_state` is now dramatically simplified.

```json
{
  "prompt": "string",
  "status": "string", // "definition_in_progress", "deliberation_ready", etc.
  "run_history": { // Tracks runs to number headings correctly
    "definition": 1,
    "deliberation": 1,
    "implementation": 1,
    "finalization": 1
  },
  "log.md": "string" // The single string containing the entire Markdown log.
}

3.2. Agent Interaction with log.md

    Reading: Before running, an agent must parse the entire log.md string. It needs logic to find the most recent version of its dependencies. For example, the OOP_Design_Agent would scan from the bottom up to find the latest [RequirementsAgent] output.

    Writing: When an agent has completed its task, it appends its output as a new section to the log.md.

        The content can be Markdown text, a JSON object within a fenced code block, or any other structured format.

        The heading for this new section is critical for organization.

3.3. Heading Generation

    The ProjectManagerAgent is responsible for generating unique, hierarchical headings.

    When an agent is ready to write, it requests a heading.

    The manager uses the current status and the run_history to construct the heading. For example, if the status is deliberation_in_progress and the current run is 2, the heading for the SecurityAnalyst would be ### [SecurityAnalyst] - Deliberation - Run 2.X, where X is an incrementing counter for actions within that phase run.

4. Agent Responsibilities in a Markdown-Centric System

    ProjectManagerAgent:

        Manages the status and the run_history counters. When a phase is re-entered (e.g., for clarification), it increments the corresponding run counter (e.g., deliberation becomes 2).

        Generates the major phase headings (e.g., ## Phase 2: Deliberation - Run 2) and the specific sub-headings for each agent's output.

        New Responsibility: In the Definition phase, it analyzes the prompt to determine the project's domain and instantiates the DomainExpertConsultant with an appropriate name (e.g., [FinanceExpert]).

    All Other Agents:

        Their process method is now a read-process-append cycle:

            Read: Parse log.md to get inputs.

            Process: Perform analysis or generate content.

            Append: Request a heading from the ProjectManagerAgent and append the new section to the log.md string in the shared_state.

    FinalizationAgent (Phase 4):

        Its role is now to process the final, complete log.md file.

        It generates a summary of the entire log.

        It determines the final version number.

        The log.md file itself becomes the primary artifact to be committed to version control, serving as a complete, self-contained record of the agent team's work. The commit message can be generated from the finalization summary.

5. Conversational Mechanics & Clarification Loops

This section details the dynamic, request-driven conversations that occur within and between the workflow phases. All conversations are managed via the agent_requests queue in the log.md itself.
5.1. Inter-Consultant Deliberation (Phase 2)

    Scenario: The SecurityAnalyst reviews the API_Design_Agent's plan and finds that it doesn't specify authentication methods.

    Process: The SecurityAnalyst posts a request in the log targeting the API_Design_Agent. The API_Design_Agent is activated, updates its plan, and posts its response.

5.2. Programmer-to-Consultant Clarification (Phase 3)

    Scenario: The SpecialistProgrammerAgent finds an ambiguity in the plan.

    Process: The programmer posts a request targeting a specific consultant. The ProjectManagerAgent detects this and reverts the status to deliberation_in_progress, re-activating the consultant team to resolve the issue.

5.3. Consultant-to-Definition Team Clarification (Phase 2 "Reach-Back")

    Scenario: A consultant finds a requirement from Phase 1 is too vague.

    Process: The consultant posts a request targeting the RequirementsAgent. The RequirementsAgent is activated (despite its phase being over) and posts a clarification, which triggers a cascade of updates among the consultants.

5.4. Cross-Consultant Optimisation (Phase 2)

    Scenario: The Algorithms_Optimisation_Expert identifies a potential performance issue in the OOP_Design_Agent's plan.

    Process: The optimization expert posts a request for a more efficient algorithm. The OOP designer updates its plan in response.

5.5. Domain-Specific Guidance (Phase 2)

    Scenario: The project involves financial data. The ProjectManagerAgent has instantiated the DomainExpertConsultant as [FinanceExpert]. This expert reviews the API_Design_Agent's plan.

    Process:

        Observation: The [FinanceExpert] sees that the API plan includes an endpoint to delete transaction records.

        Request: It posts a request targeting both the API_Design_Agent and the RequirementsAgent: "Financial regulations require that all transaction records be retained for 7 years. The DELETE /transaction/{id} endpoint violates this. Please update the requirements and API design to use a soft-delete pattern instead, marking records as 'voided' but not removing them."

        Cascade: This request triggers the RequirementsAgent to update its functional requirements and the API_Design_Agent to change the endpoint from DELETE to PUT or POST for voiding transactions. This ensures the technical solution is compliant with real-world industry rules.

--- 