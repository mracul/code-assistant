import json
import os
import tiktoken
import numpy as np
from typing import List, Dict, Optional

try:
    from openai import OpenAI
except ImportError:
    # If openai client not installed, embedding-related methods will raise errors.
    OpenAI = None


class ConversationHistory:
    def __init__(self, 
                 max_tokens: int = 3500, 
                 embedding_model: str = "text-embedding-3-small",
                 persist_path: Optional[str] = None):
        self.history: List[Dict[str, str]] = []
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.persist_path = persist_path
        
        # For embeddings
        self.embedding_model = embedding_model
        self.embeddings: List[np.ndarray] = []
        self.client = OpenAI() if OpenAI else None

        if self.persist_path:
            self.load()

    def add_message(self, role: str, content: str, embed: bool = False):
        """Add a message to history; optionally embed content."""
        self.history.append({"role": role, "content": content})
        if embed and self.client:
            try:
                emb = self._get_embedding(content)
                self.embeddings.append(emb)
            except Exception:
                self.embeddings.append(None) # Fail gracefully
        else:
            self.embeddings.append(None)

        self._truncate_to_fit()

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def _truncate_to_fit(self):
        """Truncate oldest messages until token limit is met."""
        total_tokens = sum(self._count_tokens(m["content"]) for m in self.history)
        while total_tokens > self.max_tokens and len(self.history) > 1:
            removed = self.history.pop(0)
            self.embeddings.pop(0)
            total_tokens -= self._count_tokens(removed["content"])

    def get_history(self) -> List[Dict[str, str]]:
        """Return messages list ready for GPT API call."""
        self._truncate_to_fit()
        return self.history

    def _get_embedding(self, text: str):
        if not self.client:
            raise RuntimeError("OpenAI client not initialized for embedding generation.")
        resp = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return np.array(resp.data[0].embedding)

    def get_relevant_messages(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Return top_k relevant past messages by semantic similarity to query."""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized for semantic retrieval.")
        
        valid_embeddings = [(i, e) for i, e in enumerate(self.embeddings) if e is not None]
        if not valid_embeddings:
            return [] # No messages were embedded

        query_emb = self._get_embedding(query)
        
        indices, embeddings = zip(*valid_embeddings)
        similarities = [self._cosine_similarity(query_emb, e) for e in embeddings]
        
        ranked = sorted(zip(indices, similarities), key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, sim in ranked[:top_k]]
        
        return [self.history[i] for i in top_indices]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def save(self):
        if not self.persist_path:
            return
        try:
            with open(self.persist_path, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            # Fail silently if save fails
            pass

    def load(self):
        if not self.persist_path or not os.path.exists(self.persist_path):
            return
        try:
            with open(self.persist_path, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            # Reset embeddings, must re-embed manually if needed
            self.embeddings = [None] * len(self.history)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            self.embeddings = []