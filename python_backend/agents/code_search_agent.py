# python_backend/agents/code_search_agent.py
from orchestrator.agent_state import AgentState
from utils.swe_tools import ASTParserTool, CodeRetrieverTool
import ast

class CodeSearchAgent:
    def __init__(self, state: AgentState):
        self.state = state
        self.ast_parser = ASTParserTool()
        self.code_retriever = CodeRetrieverTool()

    def run(self, query: str) -> list[dict]:
        """
        Runs a hybrid search, dispatching to AST or semantic search based on the query format.
        Query format for AST: "type:name" (e.g., "class:UserManager", "calls:authenticate_user")
        """
        if ':' in query:
            # Assume AST-based structural search
            try:
                search_type, search_name = query.split(':', 1)
                return self._run_ast_search(search_type.strip(), search_name.strip())
            except ValueError:
                # Fallback to semantic search if format is invalid
                return self._run_semantic_search(query)
        else:
            # Default to semantic search
            return self._run_semantic_search(query)

    def _run_ast_search(self, search_type: str, search_name: str) -> list[dict]:
        """Performs a search on the AST of all loaded files."""
        results = []
        for file_path, content in self.state.loaded_files.items():
            if not file_path.endswith('.py'):
                continue # AST search is for Python files
            
            try:
                tree = self.ast_parser.parse(content)
                search_tool = self.state.get_ast_search_tool(file_path, tree) # Get or create tool
                
                found_nodes = []
                if search_type == 'class':
                    node = search_tool.find_class(search_name)
                    if node: found_nodes.append(node)
                elif search_type == 'function':
                    node = search_tool.find_function(search_name)
                    if node: found_nodes.append(node)
                elif search_type == 'calls':
                    found_nodes = search_tool.find_function_calls(search_name)
                
                for node in found_nodes:
                    results.append({
                        "type": "AST Match",
                        "file_path": file_path,
                        "name": search_name,
                        "line": node.lineno,
                        "preview": ast.get_source_segment(content, node).splitlines()[0]
                    })
            except Exception:
                continue # Ignore files that fail to parse
        return results

    def _run_semantic_search(self, query: str) -> list[dict]:
        """Performs a semantic vector search."""
        search_results = self.code_retriever.search(query)
        # Format results for consistent output
        return [{
            "type": "Semantic Match",
            "file_path": r.get("file_path", "N/A"),
            "name": r.get("name", "N/A"),
            "line": r.get("start_line", "N/A"),
            "preview": r.get("content_preview", "")
        } for r in search_results]

