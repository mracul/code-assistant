# python_backend/agents/technical_analyst_agent.py
import openai
import os
import json
from orchestrator.agent_state import AgentState

def run(state: AgentState):
    """
    Evaluates the proposed strategies and selects the optimal one.
    """
    if not state.proposed_strategies:
        state.last_agent_output = {"error": "Proposed strategies not found in state."}
        return state

    with open("python_backend/prompts/technical_analyst.md", "r") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(
        strategies_json=json.dumps(state.proposed_strategies, indent=2),
        requirements=state.requirements
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    analysis = json.loads(response.choices[0].message.content)
    state.solution_analysis = analysis
    state.last_agent_output = analysis
    
    return state
