# python_backend/agents/technical_analyst.py
from orchestrator.agent_state import AgentState

def run(state: AgentState):
    """
    Analyzes the proposed strategies and selects the best one.
    This is a placeholder and will be replaced by a call to an LLM.
    """
    if not state.proposed_strategies:
        state.last_agent_output = {"error": "No proposed strategies found to analyze."}
        return state

    # In a real scenario, this would involve a more complex evaluation.
    # For now, we'll just select the first strategy as the "winner".
    selected_strategy = state.proposed_strategies[0]
    
    state.selected_solution = selected_strategy
    state.last_agent_output = {"selected_strategy_id": selected_strategy["id"], "justification": "This strategy was selected for its low effort and simplicity."}
    state.add_message("system", f"Selected solution: '{selected_strategy['name']}'")
    
    return state
