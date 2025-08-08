# python_backend/utils/ast_search.py
import ast

class ASTSearchTool:
    def __init__(self, tree: ast.AST):
        self.tree = tree

    def find_class(self, name: str) -> ast.ClassDef | None:
        """Finds a class definition by name."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and node.name == name:
                return node
        return None

    def find_function(self, name: str) -> ast.FunctionDef | None:
        """Finds a function definition by name."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                return node
        return None

    def find_imports(self, module_name: str) -> list:
        """Finds all imports of a specific module."""
        imports = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import) and any(alias.name == module_name for alias in node.names):
                imports.append(node)
            elif isinstance(node, ast.ImportFrom) and node.module == module_name:
                imports.append(node)
        return imports

    def find_function_calls(self, function_name: str) -> list[ast.Call]:
        """Finds all calls to a specific function."""
        calls = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
                calls.append(node)
        return calls
