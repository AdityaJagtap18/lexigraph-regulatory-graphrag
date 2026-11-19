"""Tests for Hybrid Compliance Retriever: Naive Vector RAG vs GraphRAG."""

import pytest
from src.core.hybrid_retriever import HybridComplianceRetriever, RetrievalResult


def test_hybrid_retriever_initialization():
    retriever = HybridComplianceRetriever()
    retriever.initialize()

    assert len(retriever.chunks) > 0
    assert len(retriever.community_reports) >= 2


def test_naive_rag_retrieval():
    retriever = HybridComplianceRetriever()
    query = "Synthesize cross-border environmental liabilities for telecom and energy conglomerates."
    result = retriever.retrieve_naive_rag(query, top_k=3)

    assert isinstance(result, RetrievalResult)
    assert result.retrieval_mode == "naive_vector_rag"
    assert len(result.contexts) == 3
    # Naive RAG has low multi-hop recall (< 0.50)
    assert result.multi_hop_recall < 0.50
    assert result.citation_defensibility < 0.80


def test_graphrag_retrieval_benchmark():
    """Verify GraphRAG achieves 100% multi-hop regulatory synthesis recall."""
    retriever = HybridComplianceRetriever()
    query = "Synthesize cross-border environmental liabilities for telecom and energy conglomerates."
    result = retriever.retrieve_graphrag(query)

    assert isinstance(result, RetrievalResult)
    assert result.retrieval_mode == "lexigraph_graphrag"
    assert len(result.contexts) >= 2
    # Portfolio Benchmark SLA: GraphRAG achieves 100.0% recall on multi-hop regulatory queries
    assert result.multi_hop_recall == 1.000
    assert result.cross_border_penalty_covered is True
    assert result.citation_defensibility == 1.000
