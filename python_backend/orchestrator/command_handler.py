# python_backend/orchestrator/command_handler.py
from orchestrator.agent_state import AgentState
from utils.path_validator import PathValidator
from context_engine.file_discovery import discover_files
from agents.code_search_agent import CodeSearchAgent
from agents import diff_agent, refactor_agent, change_summarizer_agent, conventional_commit_agent, version_control_agent
import json

# --- Command Implementations ---

async def handle_index(state: AgentState, args: list):
    target_path = args[0] if args else "."
    validator = PathValidator(target_path)
    if not validator.validate():
        await state.send_log(f"Error: {validator.error}")
        return

    await state.send_log(f"Starting codebase indexing at: {validator.absolute_path}...")
    file_count = 0
    for file_path in discover_files(validator.absolute_path):
        if file_path.endswith('.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                state.codebase_index.index_file(file_path, content)
                file_count += 1
            except Exception:
                continue
    
    state.codebase_index.build_call_graph()
    await state.send_log(f"Indexing complete. Parsed {file_count} Python files and built function call graph.")

async def handle_impact(state: AgentState, args: list):
    if len(args) != 1 or ':' not in args[0]:
        await state.send_log("Usage: /impact <file_path>:<function_name>")
        return
    
    file_path, function_name = args[0].split(':', 1)
    validator = PathValidator(file_path)
    if not validator.validate():
        await state.send_log(f"Error: {validator.error}")
        return

    await state.send_log(f"Analyzing impact of changes to {function_name} in {file_path}...")
    impact_results = state.codebase_index.get_impacted_functions(validator.absolute_path, function_name)
    
    await state.websocket.send_text(json.dumps({
        "type": "impact_analysis",
        "data": {"target": f"{file_path}:{function_name}", "impacted_functions": impact_results}
    }))

async def handle_refactor(state: AgentState, args: list):
    if len(args) < 3:
        await state.send_log("Usage: /refactor <file_path> <old_name> <new_name>")
        return
    
    file_path, old_name, new_name = args[0], args[1], args[2]
    # ... (validation and file loading logic would go here) ...
    refactor_agent.run(state, file_path, old_name, new_name)
    await state.send_diff(file_path, state.last_agent_output)

async def handle_commit(state: AgentState, args: list):
    if not state.last_agent_output or not state.modified_buffers:
        await state.send_log("Error: No pending changes to commit.")
        return
    
    target_file = list(state.modified_buffers.keys())[0]
    await state.send_log(f"Finalizing changes for {target_file}...")
    
    change_summarizer_agent.run(state, target_file)
    conventional_commit_agent.run(state)
    version_control_agent.run(state, target_file)
    
    await state.websocket.send_text(json.dumps({
        "type": "final_commands",
        "data": {
            "commit_message": state.commit_message,
            "commands": state.git_commands
        }
    }))

# --- Command Registry ---

COMMAND_REGISTRY = {
    "index": handle_index,
    "impact": handle_impact,
    "refactor": handle_refactor,
    "commit": handle_commit,
    # Add other commands like 'search', 'diff' here
}
