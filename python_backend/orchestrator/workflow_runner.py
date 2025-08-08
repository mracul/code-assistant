# python_backend/orchestrator/workflow_runner.py
import json
import asyncio
from orchestrator.agent_state import AgentState
from orchestrator.agent_registry import agent_registry

class WorkflowRunner:
    def __init__(self, state: AgentState):
        with open('workflows.json', 'r') as f:
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
            # The step can be a simple string (agent name) or a dict for complex steps
            if isinstance(step, str):
                agent_name = step
                await self._run_standard_step(agent_name)
            elif isinstance(step, dict):
                # For now, we only have standard steps, but this is where
                # deliberation or other complex steps would be handled.
                agent_name = step.get("agent")
                if agent_name:
                    await self._run_standard_step(agent_name)
                else:
                    await self.state.send_log(f"Skipping complex step (not implemented): {step.get('step')}")
            
            # Check if the last agent produced an error
            if self.state.last_agent_output and isinstance(self.state.last_agent_output, dict) and self.state.last_agent_output.get('error'):
                error_message = self.state.last_agent_output['error']
                await self.state.send_log(f"Workflow halted due to an error in agent '{agent_name}': {error_message}")
                return

        await self.state.send_log("Workflow finished successfully.")

    async def _run_standard_step(self, agent_name: str):
        """Executes a single, standard agent step using the registry."""
        await self.state.send_log(f"--- Running Agent: {agent_name} ---")
        try:
            # The agent_registry handles loading and running the agent's `run` method
            agent_registry.run_agent(agent_name, self.state)
        except (ValueError, NotImplementedError) as e:
            await self.state.send_log(f"Error executing agent '{agent_name}': {e}")
            # Set an error state to halt the workflow
            self.state.last_agent_output = {"error": str(e)}
