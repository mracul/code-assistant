import json
import os
import tiktoken
import numpy as np
from typing import List, Dict, Optional

# Lazy loading for sentence_transformers
SentenceTransformer = None

def _lazy_load_transformer():
    global SentenceTransformer
    if SentenceTransformer is None:
        try:
            from sentence_transformers import SentenceTransformer as STransformer
            SentenceTransformer = STransformer
        except ImportError:
            raise RuntimeError("SentenceTransformer is not installed. Please `pip install sentence-transformers`.")
    return SentenceTransformer

class ConversationHistory:
    def __init__(self, 
                 max_tokens: int = 3500, 
                 embedding_model_name: str = "all-MiniLM-L6-v2",
                 persist_path: Optional[str] = None):
        self.history: List[Dict[str, str]] = []
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.persist_path = persist_path
        
        # For embeddings
        self.embedding_model_name = embedding_model_name
        self._embedding_model = None  # Lazy-loaded
        self.embeddings: List[np.ndarray] = []

        if self.persist_path:
            self.load()

    @property
    def embedding_model(self):
        """Lazy-loads the embedding model on first access."""
        if self._embedding_model is None:
            print("Lazy loading embedding model...")
            TransformerClass = _lazy_load_transformer()
            self._embedding_model = TransformerClass(self.embedding_model_name)
            print("Embedding model loaded.")
        return self._embedding_model

    def add_message(self, role: str, content: str, embed: bool = False):
        """Add a message to history; optionally embed content."""
        self.history.append({"role": role, "content": content})
        if embed:
            try:
                emb = self._get_embedding(content)
                self.embeddings.append(emb)
            except Exception as e:
                print(f"Error embedding message: {e}")
                self.embeddings.append(None)
        else:
            self.embeddings.append(None)

        self._truncate_to_fit()

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def _truncate_to_fit(self):
        """Truncate oldest messages until token limit is met."""
        total_tokens = sum(self._count_tokens(m["content"]) for m in self.history)
        while total_tokens > self.max_tokens and len(self.history) > 1:
            self.history.pop(0)
            self.embeddings.pop(0)
            total_tokens -= self._count_tokens(m["content"])

    def get_history(self) -> List[Dict[str, str]]:
        """Return messages list ready for GPT API call."""
        self._truncate_to_fit()
        return self.history

    def _get_embedding(self, text: str) -> np.ndarray:
        """Generates an embedding for the given text."""
        return self.embedding_model.encode(text)

    def get_relevant_messages(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Return top_k relevant past messages by semantic similarity to query."""
        valid_embeddings = [(i, e) for i, e in enumerate(self.embeddings) if e is not None]
        if not valid_embeddings:
            return []

        query_emb = self._get_embedding(query)
        
        indices, embeddings = zip(*valid_embeddings)
        similarities = [self._cosine_similarity(query_emb, e) for e in embeddings]
        
        ranked = sorted(zip(indices, similarities), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, sim in ranked[:top_k]]
        
        return [self.history[i] for i in top_indices]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0.0

    def save(self):
        if not self.persist_path:
            return
        try:
            with open(self.persist_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load(self):
        if not self.persist_path or not os.path.exists(self.persist_path):
            return
        try:
            with open(self.persist_path, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            self.embeddings = [None] * len(self.history)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            self.embeddings = []
