# python_backend/agents/version_control_agent.py
from orchestrator.agent_state import AgentState

def run(state: AgentState, file_path: str):
    """
    Generates the git commands required to stage and commit the changes.
    """
    if not state.commit_message:
        return "Error: No commit message found in the state."
    
    commands = [
        f"git add {file_path}",
        f"git commit -m \"{state.commit_message}\""
    ]
    
    state.git_commands = commands
    return state