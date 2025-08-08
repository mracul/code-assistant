# python_backend/agents/conventional_commit_agent.py
from orchestrator.agent_state import AgentState
from services.llm_service import LLMService
import json

def run(state: AgentState):
    """
    Generates a conventional commit message using the LLMService.
    """
    if not state.change_summary:
        state.last_agent_output = {"error": "No change summary found."}
        return state

    with open("python_backend/prompts/conventional_commit_agent.md", "r") as f:
        prompt_template = f.read()
    
    context = {"summary_json": json.dumps(state.change_summary, indent=2)}
    
    llm = LLMService()
    response_json = llm.execute_prompt(prompt_template, context, is_json=True)
    
    state.commit_message = response_json.get("commit_message")
    state.last_agent_output = state.commit_message
    
    return state
