# python_backend/agents/change_summarizer_agent.py
from orchestrator.agent_state import AgentState
from services.llm_service import LLMService

def run(state: AgentState, file_path: str):
    """
    Analyzes a diff using the LLMService to generate a structured summary.
    """
    diff_text = state.last_agent_output
    if not diff_text:
        state.last_agent_output = {"error": "No diff found in state."}
        return state

    with open("python_backend/prompts/change_summarizer.md", "r") as f:
        prompt_template = f.read()
    
    context = {"code_diff": diff_text}
    
    llm = LLMService()
    summary_json = llm.execute_prompt(prompt_template, context, is_json=True)
    
    state.change_summary = summary_json
    state.last_agent_output = summary_json
    
    return state
