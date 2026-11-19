"""Tests for Sentence-Transformers dense embedding engine."""

import numpy as np
import pytest
from src.core.embedding_engine import SentenceEmbeddingEngine


def test_embedding_engine_dimension():
    engine = SentenceEmbeddingEngine()
    vec = engine.embed_query("EU Corporate Sustainability Due Diligence Directive")

    assert isinstance(vec, np.ndarray)
    assert vec.shape == (384,)
    # Normalized vector has norm approximately 1.0
    norm = np.linalg.norm(vec)
    assert 0.99 <= norm <= 1.01


def test_embedding_cosine_similarity():
    engine = SentenceEmbeddingEngine()
    vec_a = engine.embed_query("Cross-border grid power transmission")
    vec_b = engine.embed_query("Cross-border grid power transmission")
    vec_c = engine.embed_query("Deep sea marine biology and coral reefs")

    sim_identical = engine.cosine_similarity(vec_a, vec_b)
    sim_different = engine.cosine_similarity(vec_a, vec_c)

    assert sim_identical >= 0.99
    assert sim_different < sim_identical
