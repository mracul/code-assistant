from . import vector_store, git_analyzer, sql_analyzer, ast_parser
import os

def get_context(prompt, conversation_history, repo_path, db_uri=None):
    """
    Get the context for the agent.
    """
    context = {
        "prompt": prompt,
        "conversation_history": conversation_history,
        "ast_analysis": {}
    }

    # RAG search
    vs = vector_store.ChromaVectorStore()
    query_embedding = vector_store.generate_embeddings([prompt])
    if query_embedding.any():
        context["rag_search_results"] = vs.search(query_embedding[0])

    # Git history
    ga = git_analyzer.GitAnalyzer(repo_path)
    context["recently_changed_files"] = ga.get_recently_changed_files()

    # AST Analysis of recently changed python files
    for file_path in context["recently_changed_files"]:
        if file_path.endswith(".py"):
            with open(os.path.join(repo_path, file_path), 'r') as f:
                content = f.read()
                parser = ast_parser.ASTParser(content)
                context["ast_analysis"][file_path] = parser.parse()

    # SQL schema
    if db_uri:
        sa = sql_analyzer.SQLAnalyzer(db_uri)
        context["sql_schema"] = sa.get_schema()

    return context
