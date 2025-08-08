# python_backend/agents/refactor_agent.py
import ast
from orchestrator.agent_state import AgentState
from utils.swe_tools import DiffFormatterTool

class RenameTransformer(ast.NodeTransformer):
    """
    An AST NodeTransformer to safely rename functions and their calls.
    """
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def visit_FunctionDef(self, node):
        if node.name == self.old_name:
            node.name = self.new_name
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.old_name:
            node.func.id = self.new_name
        self.generic_visit(node)
        return node

def run(state: AgentState, file_path: str, old_name: str, new_name: str):
    """
    Performs an AST-based refactoring to rename a function and its usages.
    """
    original_content = state.get_file_content(file_path)
    if not original_content:
        return f"Error: File '{file_path}' not found in state."

    tree = state.codebase_index.asts.get(file_path)
    if not tree:
        return f"Error: AST for '{file_path}' not found in the codebase index. Please run /index first."

    # 1. Transform the AST
    transformer = RenameTransformer(old_name, new_name)
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    # 2. Unparse the new AST back to source code
    try:
        modified_content = ast.unparse(new_tree)
    except Exception as e:
        return f"Error unparsing the modified AST: {e}"

    # 3. Generate a diff
    diff_tool = DiffFormatterTool()
    diff_text = diff_tool.create_diff(original_content, modified_content)

    # 4. Update the state and buffer
    state.modify_buffer(file_path, modified_content)
    state.last_agent_output = diff_text
    
    return state
