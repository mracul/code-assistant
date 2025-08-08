# python_backend/agents/creative_architect_agent.py
import openai
import os
import json
from orchestrator.agent_state import AgentState

def run(state: AgentState):
    """
    Generates 2-3 distinct, high-level solution strategies based on the requirements.
    """
    if not state.requirements:
        state.last_agent_output = {"error": "Requirements not found in state."}
        return state

    with open("python_backend/prompts/creative_architect.md", "r") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(
        requirements=state.requirements,
        technical_context=json.dumps(state.get_full_context_for_prompt(), indent=2)
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    strategies = json.loads(response.choices[0].message.content)
    state.proposed_strategies = strategies.get("strategies", [])
    state.last_agent_output = state.proposed_strategies
    
    return state
