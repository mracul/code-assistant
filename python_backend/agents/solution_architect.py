from orchestrator.agent_state import AgentState
import openai
import os
import json

def run(state: AgentState):
    """
    This agent designs a high-level solution to meet the requirements.
    """
    with open("prompts/solution_architect.md", "r") as f:
        prompt_template = f.read()

    # Create a simplified technical context for the prompt
    technical_context = {
        "rag_search_results": state.get("rag_search_results", "Not available."),
        "recently_changed_files": state.get("recently_changed_files", "Not available."),
        "ast_analysis": state.get("ast_analysis", "Not available.")
    }

    prompt = prompt_template.format(
        requirements=state.requirements,
        technical_context=json.dumps(technical_context, indent=2)
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a world-class agentic assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    state.solution = response.choices[0].message.content
    return state
