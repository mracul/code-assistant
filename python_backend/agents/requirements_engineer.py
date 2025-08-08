from orchestrator.agent_state import AgentState
import openai
import os

def run(state: AgentState):
    """
    This agent translates user requests into formal requirements.
    """
    with open("prompts/requirements_engineer.md", "r") as f:
        prompt_template = f.read()

    user_request = state.conversation[-1]['content']
    history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state.conversation])

    prompt = prompt_template.format(
        user_request=user_request,
        conversation_history=history
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a world-class agentic assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    state.requirements = response.choices[0].message.content
    return state
