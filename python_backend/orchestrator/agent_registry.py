# python_backend/orchestrator/agent_registry.py
import json
import importlib
import os
from typing import Dict, Any

class AgentRegistry:
    """
    Dynamically loads and provides access to agent modules based on agents.json.
    """
    def __init__(self, agents_file_path: str = 'agents.json'):
        # Build a path to agents.json relative to this file's location
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Go up one level from orchestrator to the python_backend root, then to the project root
        full_path = os.path.join(dir_path, '..', '..', agents_file_path)
        
        with open(full_path, 'r') as f:
            self._agent_definitions = json.load(f)
        self._loaded_agents = {}

    def _load_agent_module(self, agent_name: str) -> Any:
        """Dynamically imports an agent's module."""
        if agent_name in self._loaded_agents:
            return self._loaded_agents[agent_name]

        # Convert PascalCase agent name to snake_case module name
        module_name = ''.join(['_' + i.lower() if i.isupper() else i for i in agent_name]).lstrip('_')
        
        try:
            # The agent modules are expected to be in the `agents` directory
            module = importlib.import_module(f"agents.{module_name}")
            self._loaded_agents[agent_name] = module
            return module
        except ImportError:
            raise ValueError(f"Could not find or import the module for agent: {agent_name}. Expected agents/{module_name}.py")

    def get_agent_definition(self, agent_name: str) -> Dict[str, Any]:
        """Retrieves the JSON definition for a specific agent."""
        for agent_def in self._agent_definitions:
            if agent_def["name"] == agent_name:
                return agent_def
        raise ValueError(f"Agent '{agent_name}' not found in definitions.")

    def run_agent(self, agent_name: str, state: 'AgentState') -> 'AgentState':
        """
        Loads and runs the specified agent's `run` method.
        """
        agent_module = self._load_agent_module(agent_name)
        
        if not hasattr(agent_module, 'run'):
            raise NotImplementedError(f"Agent module for '{agent_name}' does not have a 'run' function.")
            
        print(f"Executing agent: {agent_name}")
        return agent_module.run(state)

# A single, shared instance of the registry
agent_registry = AgentRegistry()
