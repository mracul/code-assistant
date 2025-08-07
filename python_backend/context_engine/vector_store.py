import os
import openai
import numpy as np
import faiss

# The dimension of the text-embedding-3-small model
EMBEDDING_DIM = 1536

def generate_embeddings(chunks: list[str]) -> list[np.ndarray]:
    """
    Generates embeddings for a list of text chunks.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY environment variable not found. Skipping embedding generation.")
        return []

    client = openai.OpenAI(api_key=api_key)

    if not chunks:
        return []

    try:
        chunks = [chunk.replace("\n", " ") for chunk in chunks]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )
        return [np.array(embedding.embedding, dtype=np.float32) for embedding in response.data]
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return []

class InMemoryVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.metadata_store = []

    def clear(self):
        """Clears the store."""
        self.index.reset()
        self.metadata_store = []

    def add(self, embeddings: list[np.ndarray], metadata: list[dict]):
        """
        Adds embeddings and their corresponding metadata to the store.
        """
        if not embeddings:
            return

        embeddings_np = np.array(embeddings).astype('float32')
        self.index.add(embeddings_np)
        self.metadata_store.extend(metadata)

    def search(self, query_embedding: np.ndarray, k: int = 10) -> list[dict]:
        """
        Searches for the k most similar vectors to the query vector.
        """
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, k)

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i != -1: # faiss returns -1 for no result
                result_metadata = self.metadata_store[i]
                result_metadata['distance'] = float(dist)
                results.append(result_metadata)

        return results
