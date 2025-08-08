# python_backend/agents/base_agent.py
import openai
import os
from orchestrator.agent_state import AgentState
import json

def run_agent(agent_name: str, state: AgentState, prompt_template_path: str, prompt_context: dict) -> AgentState:
    """
    A generic function to run any agent that uses a prompt template.
    """
    with open(prompt_template_path, "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(**prompt_context)

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini", # Using the specified model
        messages=[
            {"role": "system", "content": "You are a world-class agentic assistant. Follow the user's instructions precisely."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Assumes the agent's output is stored in a key matching its name
    output_key = agent_name.lower()
    state[output_key] = response.choices[0].message.content
    
    # A simple confidence score placeholder
    state.last_agent_confidence = response.choices[0].finish_reason != 'length'
    
    return state
