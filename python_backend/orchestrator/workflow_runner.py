# python_backend/orchestrator/workflow_runner.py
import json
import asyncio
import os
from orchestrator.agent_state import AgentState
from orchestrator.agent_registry import agent_registry

class WorkflowRunner:
    def __init__(self, state: AgentState):
        # Build a path to workflows.json relative to this file's location
        dir_path = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(dir_path, '..', '..', 'workflows.json')
        with open(full_path, 'r') as f:
            self.workflows = json.load()["workflows"]
        self.state = state

    async def execute_workflow(self, name: str):
        """Executes a workflow defined in workflows.json."""
        workflow = self.workflows.get(name)
        if not workflow:
            await self.state.send_log(f"Error: Workflow '{name}' not found.")
            return

        await self.state.send_log(f"Starting workflow: {workflow['description']}")

        for step in workflow["sequence"]:
            step_type = step.get("type", "standard")
            
            if step_type == "deliberation":
                await self._run_deliberation_step(step)
            else:
                agent_name = step.get("agent")
                if agent_name:
                    await self._run_standard_step(agent_name)
                else:
                    await self.state.send_log(f"Skipping invalid step: {step}")

            if self.state.last_agent_output and isinstance(self.state.last_agent_output, dict) and self.state.last_agent_output.get('error'):
                error_message = self.state.last_agent_output['error']
                agent_name_in_error = agent_name or step.get("proposer") # Best guess
                await self.state.send_log(f"Workflow halted due to an error in agent '{agent_name_in_error}': {error_message}")
                return

        await self.state.send_log("Workflow finished successfully.")
        
        # --- After workflow, handle the final output ---
        final_output = self.state.last_agent_output
        if final_output and isinstance(final_output, dict):
            if "diff" in final_output and "file_path" in final_output:
                await self.state.send_log("Displaying final proposed changes.")
                await self.state.send_diff(final_output["file_path"], final_output["diff"])
            else:
                # If it's not a diff, just log the summary if it exists
                summary = final_output.get("summary", json.dumps(final_output))
                await self.state.send_log(f"Final result: {summary}")

    async def _run_standard_step(self, agent_name: str):
        """Executes a single, standard agent step using the registry."""
        await self.state.send_log(f"--- Running Agent: {agent_name} ---")
        try:
            agent_registry.run_agent(agent_name, self.state)
        except (ValueError, NotImplementedError) as e:
            await self.state.send_log(f"Error executing agent '{agent_name}': {e}")
            self.state.last_agent_output = {"error": str(e)}

    async def _run_deliberation_step(self, step: dict):
        """Manages a conversational loop between two agents to reach a decision."""
        proposer_name = step["proposer"]
        challenger_name = step["challenger"]
        max_turns = step.get("max_turns", 2)

        await self.state.send_log(f"--- Starting Deliberation: {proposer_name} vs. {challenger_name} ---")

        for i in range(max_turns):
            await self.state.send_log(f"Deliberation Turn {i+1}...")
            
            # 1. Proposer makes a suggestion
            await self._run_standard_step(proposer_name)
            if self.state.last_agent_output.get('error'): return # Halt on error

            # 2. Challenger evaluates the proposal
            await self._run_standard_step(challenger_name)
            if self.state.last_agent_output.get('error'): return # Halt on error

            # 3. Check for consensus
            if self.state.selected_solution:
                await self.state.send_log("Consensus reached. Optimal solution selected.")
                return

        await self.state.send_log("Deliberation failed to reach consensus after max turns.")
        # In a real system, an escalation policy would be triggered here.
        self.state.last_agent_output = {"error": "Deliberation failed."}