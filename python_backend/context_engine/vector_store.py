# python_backend/context_engine/vector_store.py
import os
import openai
import numpy as np
import chromadb
from .tokenization import get_tokenizer

EMBEDDING_DIM = 1536 # text-embedding-3-small

def generate_embeddings(text_chunks: list[str]) -> list[list[float]]:
    """Generates embeddings for a list of text chunks."""
    if not text_chunks:
        return []
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not found. Skipping embedding generation.")
        return []

    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[chunk.replace("\n", " ") for chunk in text_chunks]
        )
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return []

class ChromaVectorStore:
    def __init__(self, path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="code_assistant_v2")
        self.tokenizer = get_tokenizer()

    def add_chunks(self, file_path: str, chunks: list[dict]):
        """
        Generates embeddings for text chunks and adds them to the store
        with rich metadata.
        """
        if not chunks:
            return

        contents = [chunk["content"] for chunk in chunks]
        embeddings = generate_embeddings(contents)
        if not embeddings:
            return

        metadatas = []
        ids = []
        for i, chunk in enumerate(chunks):
            metadatas.append({
                "file_path": file_path,
                "type": chunk["type"],
                "name": chunk["name"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "token_count": len(self.tokenizer.encode(chunk["content"])),
                "content_preview": chunk["content"][:200] # For quick inspection
            })
            ids.append(f"{file_path}:{chunk['name']}:{chunk['start_line']}")

        self.collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)

    def search(self, query: str, k: int = 10) -> list[dict]:
        """
        Searches for the k most similar vectors to the query.
        """
        if self.collection.count() == 0:
            return []
            
        query_embedding = generate_embeddings([query])
        if not query_embedding:
            return []

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k
        )
        # The result is a dict with 'ids', 'distances', 'metadatas', etc.
        # We return the list of metadatas for the first query.
        return results.get('metadatas', [[]])[0]
