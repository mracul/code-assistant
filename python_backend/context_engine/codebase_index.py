# python_backend/context_engine/codebase_index.py
import ast
import networkx as nx
from typing import Dict

class CodebaseIndex:
    def __init__(self):
        self.asts: Dict[str, ast.AST] = {}
        self.call_graph = nx.DiGraph()

    def index_file(self, file_path: str, content: str):
        """Parses a file into an AST and adds it to the index."""
        try:
            tree = ast.parse(content, filename=file_path)
            self.asts[file_path] = tree
        except (SyntaxError, ValueError):
            self.asts[file_path] = None # Mark as unparsable

    def build_call_graph(self):
        """
        Builds a complete function call graph from all indexed ASTs.
        This should be called after all initial files have been indexed.
        """
        self.call_graph.clear()
        for file_path, tree in self.asts.items():
            if not tree: continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    caller_node = (file_path, node.name)
                    self.call_graph.add_node(caller_node)
                    
                    for sub_node in ast.walk(node):
                        if isinstance(sub_node, ast.Call) and isinstance(sub_node.func, ast.Name):
                            # Simplified resolver: assumes local calls for now
                            callee_node = (file_path, sub_node.func.id)
                            self.call_graph.add_edge(caller_node, callee_node)
        return self.call_graph

    def get_impacted_functions(self, target_file: str, target_function: str) -> list:
        """
        Analyzes the pre-built graph to find functions impacted by a change.
        """
        target_node = (target_file, target_function)
        if not self.call_graph.has_node(target_node):
            return []
        
        impacted_nodes = nx.ancestors(self.call_graph, target_node)
        return [f"{file}:{func}" for file, func in impacted_nodes]
