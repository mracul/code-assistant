# python_backend/agents/structure_analyzer.py
from orchestrator.agent_state import AgentState

def run(state: AgentState):
    """
    Analyzes the codebase to build a structural understanding (ASTs, call graphs).
    This agent assumes the codebase has already been indexed.
    """
    if not state.codebase_index.is_indexed():
        state.last_agent_output = {"error": "Codebase has not been indexed. Cannot perform structure analysis."}
        return state

    # The main work is already done during the initial indexing.
    # Here, we can just report on the results.
    num_asts = len(state.codebase_index.asts)
    num_nodes = state.codebase_index.call_graph.number_of_nodes()
    num_edges = state.codebase_index.call_graph.number_of_edges()

    summary = (
        f"Code structure analysis complete.\n"
        f"- Parsed {num_asts} files into ASTs.\n"
        f"- Built a call graph with {num_nodes} functions (nodes) and {num_edges} calls (edges)."
    )
    
    state.last_agent_output = {"summary": summary}
    state.add_message("system", summary)
    
    return state
