# swe_tools.py
import ast
import json
import networkx as nx
import tiktoken
import diff_match_patch as dmp_module
from context_engine import vector_store # Corrected import path

# 1. ASTParserTool
class ASTParserTool:
    """Parses source code to build and inspect its Abstract Syntax Tree."""
    def parse(self, file_content: str) -> ast.AST:
        return ast.parse(file_content)

    def find_nodes(self, tree: ast.AST, node_type: str) -> list:
        return [node for node in ast.walk(tree) if isinstance(node, getattr(ast, node_type))]

# 2. CodeRetrieverTool (Semantic Search)
class CodeRetrieverTool:
    """Finds relevant code chunks using semantic search (RAG)."""
    def __init__(self, db_path="./chroma_db"):
        self.vector_store = vector_store.ChromaVectorStore(path=db_path)

    def search(self, query: str, k: int = 5) -> list[dict]:
        query_embedding = vector_store.generate_embeddings([query])
        if not query_embedding:
            return []
        return self.vector_store.search(query, k=k)

# 3. TokenEstimateTool
class TokenEstimateTool:
    """Estimates token count to optimize context windows."""
    def __init__(self, model_name="gpt-4.1-mini"):
        self.encoding = tiktoken.encoding_for_model(model_name)

    def count(self, text: str) -> int:
        return len(self.encoding.encode(text))

# 4. PromptContextBuilderTool
class PromptContextBuilderTool:
    """Builds LLM-optimized prompt structures from multiple files and context sources."""
    def build_prompt(self, template: str, context: dict) -> str:
        return template.format(**context)

# 5. DiffFormatterTool
class DiffFormatterTool:
    """Provides clear feedback loops by creating and formatting diffs."""
    def __init__(self):
        self.dmp = dmp_module.diff_match_patch()

    def create_diff(self, text1: str, text2: str) -> str:
        patches = self.dmp.patch_make(text1, text2)
        return self.dmp.patch_toText(patches)

    def apply_diff(self, diff_text: str, original_text: str) -> str:
        patches = self.dmp.patch_fromText(diff_text)
        new_text, _ = self.dmp.patch_apply(patches, original_text)
        return new_text

# NOTE: DependencyGraphTool and RuntimeFlowAnalyzerTool have been removed
# as their logic is now centralized in context_engine/codebase_index.py for efficiency.

# 6. DesignRefactorTool (Placeholder)
class DesignRefactorTool:
    """Embeds architectural improvements via design patterns."""
    def refactor_with_pattern(self, code: str, pattern_name: str, instructions: str) -> str:
        # Placeholder for a future LLM call
        return f"# LLM-driven refactoring placeholder for pattern: {pattern_name}\n{code}"