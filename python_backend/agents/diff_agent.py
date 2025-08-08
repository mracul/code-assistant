# python_backend/agents/diff_agent.py
from orchestrator.agent_state import AgentState
from utils.swe_tools import DiffFormatterTool
from services.llm_service import LLMService
import json

def run(state: AgentState, file_path: str, instruction: str):
    """
    Generates a code modification using the LLMService and returns a diff.
    """
    original_content = state.get_file_content(file_path)
    if not original_content:
        state.last_agent_output = f"Error: File '{file_path}' not found in state."
        return state

    # For simplicity, we'll create a dedicated prompt file for this agent.
    prompt_template = """
# ROLE: Expert Software Engineer
# OBJECTIVE: Modify the code in the target file based on the user's instruction and the provided context.
# INSTRUCTIONS: Your output MUST ONLY be the raw, complete source code for the modified file.

# USER INSTRUCTION:
{instruction}

# FULL CONTEXT:
{full_context}

# TARGET FILE (`{file_path}`):
```python
{original_code}
```

# MODIFIED CODE FOR `{file_path}`:
"""

    context = {
        "instruction": instruction,
        "file_path": file_path,
        "original_code": original_content,
        "full_context": json.dumps(state.get_full_context_for_prompt(), indent=2)
    }

    llm = LLMService()
    modified_content = llm.execute_prompt(prompt_template, context)

    if isinstance(modified_content, dict) and "error" in modified_content:
        state.last_agent_output = f"Error from LLM: {modified_content['error']}"
        return state

    diff_tool = DiffFormatterTool()
    diff_text = diff_tool.create_diff(original_content, modified_content)

    state.modify_buffer(file_path, modified_content)
    state.last_agent_output = diff_text
    
    return state