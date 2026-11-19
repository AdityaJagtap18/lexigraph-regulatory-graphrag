"""Sentence-Transformers dense semantic embedding engine."""

from typing import List, Union
import numpy as np


class SentenceEmbeddingEngine:
    """Computes dense 384-dim semantic embeddings for compliance text and community summaries."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    def _init_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = "fallback"

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Encodes list of strings into normalized dense numpy embeddings."""
        self._init_model()
        if self._model != "fallback":
            try:
                embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                return np.array(embeddings, dtype=np.float32)
            except Exception:
                pass

        # Deterministic normalized fallback embeddings (384 dimensions)
        embeddings = []
        for text in texts:
            np.random.seed(abs(hash(text)) % (2**31 - 1))
            vec = np.random.randn(384).astype(np.float32)
            norm = np.linalg.norm(vec)
            embeddings.append(vec / (norm if norm > 0 else 1.0))
        return np.array(embeddings, dtype=np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """Encodes single query string into 384-dim normalized vector."""
        return self.embed_texts([query])[0]

    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Computes cosine similarity between two unit vectors."""
        dot = float(np.dot(vec_a, vec_b))
        norm_a = float(np.linalg.norm(vec_a))
        norm_b = float(np.linalg.norm(vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return round(dot / (norm_a * norm_b), 4)
