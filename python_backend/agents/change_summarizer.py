from orchestrator.agent_state import AgentState

def run(state: AgentState):
    """
    This agent summarizes the changes.
    """
    # In a real implementation, this agent would use an LLM to generate a summary
    state.summary = "This change adds a new button."
    return state
