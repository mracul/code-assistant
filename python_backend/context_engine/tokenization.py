# python_backend/context_engine/tokenization.py
import ast
import tiktoken

# Using a model compatible with GPT-4.1-mini for tokenization
TOKENIZER = tiktoken.encoding_for_model("gpt-4.1-mini")

def get_tokenizer():
    """Returns the singleton tokenizer instance."""
    return TOKENIZER

def chunk_content_by_ast(file_content: str, file_path: str) -> list[dict]:
    """
    Chunks a Python file based on its AST structure (classes and functions).
    Each chunk is a dictionary containing the text and line numbers.
    """
    chunks = []
    try:
        tree = ast.parse(file_content, filename=file_path)
        
        # First, get top-level imports and code
        top_level_nodes = [node for node in tree.body if not isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        if top_level_nodes:
            start_node = top_level_nodes[0]
            end_node = top_level_nodes[-1]
            top_level_content = ast.get_source_segment(file_content, start_node)
            # This is a simplification; getting the end is tricky.
            # For now, we'll just take the segment of the first node.
            chunks.append({
                "type": "module_code",
                "name": file_path,
                "content": top_level_content,
                "start_line": start_node.lineno,
                "end_line": end_node.end_lineno if hasattr(end_node, 'end_lineno') else start_node.lineno
            })

        # Then, chunk classes and functions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                chunk_content = ast.get_source_segment(file_content, node)
                if chunk_content:
                    chunks.append({
                        "type": "class" if isinstance(node, ast.ClassDef) else "function",
                        "name": node.name,
                        "content": chunk_content,
                        "start_line": node.lineno,
                        "end_line": node.end_lineno
                    })
        return chunks
    except (SyntaxError, ValueError):
        # Fallback for non-Python files or files with syntax errors
        return chunk_content_by_tokens(file_content)

def chunk_content_by_tokens(file_content: str, max_tokens=500, overlap=50) -> list[dict]:
    """
    A fallback chunking mechanism based on simple token overlap.
    """
    tokens = TOKENIZER.encode(file_content)
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = TOKENIZER.decode(chunk_tokens)
        chunks.append({
            "type": "text_chunk",
            "name": f"chunk_{chunk_id}",
            "content": chunk_text,
            "start_line": -1, # Line numbers are not easily tracked here
            "end_line": -1
        })
        start += max_tokens - overlap
        chunk_id += 1
    return chunks