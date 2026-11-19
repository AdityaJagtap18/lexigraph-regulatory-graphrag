"""Tests for regulatory corpus loader and document chunker."""

import os
import pytest
from src.core.corpus_loader import RegulatoryCorpusLoader, DocumentChunk


def test_corpus_loader_reads_documents():
    loader = RegulatoryCorpusLoader(corpus_dir="data/regulatory_corpus")
    docs = loader.load_documents()

    assert len(docs) >= 3
    assert "eu_csddd_directive.txt" in docs
    assert "sec_climate_esg.txt" in docs
    assert "telecom_energy_grid_resilience.txt" in docs

    for name, content in docs.items():
        assert len(content) > 200
        c_lower = content.lower()
        assert "directive" in c_lower or "securities" in c_lower or "reliability" in c_lower


def test_corpus_loader_chunking():
    loader = RegulatoryCorpusLoader(corpus_dir="data/regulatory_corpus")
    chunks = loader.chunk_corpus(chunk_size=500, overlap=50)

    assert len(chunks) >= 5
    first = chunks[0]
    assert isinstance(first, DocumentChunk)
    assert first.chunk_id.startswith("chk_")
    assert first.document_name.endswith(".txt")
    assert len(first.text) > 0
    assert first.token_count > 0
