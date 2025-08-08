import ast

class ASTParser:
    def __init__(self, file_content):
        self.tree = ast.parse(file_content)
        self.results = {
            "imports": [],
            "functions": [],
            "classes": []
        }

    def parse(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.results["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                self.results["imports"].append(node.module)
            elif isinstance(node, ast.FunctionDef):
                self.results["functions"].append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args]
                })
            elif isinstance(node, ast.ClassDef):
                self.results["classes"].append({
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
        return self.results
