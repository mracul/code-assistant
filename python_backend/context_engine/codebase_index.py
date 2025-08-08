# python_backend/context_engine/codebase_index.py
import os
import ast
import networkx as nx
from typing import Dict
from .file_discovery import discover_files

class CodebaseIndex:
    def __init__(self):
        self.asts: Dict[str, ast.AST] = {}
        self.call_graph = nx.DiGraph()
        self._is_indexed = False

    def is_indexed(self) -> bool:
        """Checks if the codebase has been indexed."""
        return self._is_indexed

    def index_directory(self, directory_path: str):
        """
        Indexes all parsable files in a directory and builds the call graph.
        """
        all_files = discover_files(directory_path)
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.index_file(file_path, content)
            except Exception:
                # Ignore files that can't be read
                continue
        
        self.build_call_graph()
        self._is_indexed = True
        print(f"Codebase indexing complete. Indexed {len(self.asts)} files.")

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