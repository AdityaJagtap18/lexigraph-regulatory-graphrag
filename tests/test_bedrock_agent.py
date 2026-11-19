"""Tests for Amazon Bedrock / AgentCore regulatory synthesis engine."""

import pytest
from src.core.bedrock_agent import BedrockAgentCore


def test_bedrock_agent_initialization():
    agent = BedrockAgentCore(offline_mode=True)
    assert agent.model_id == BedrockAgentCore.DEFAULT_MODEL_ID
    assert agent.offline_mode is True


def test_bedrock_agent_synthesis_graphrag():
    agent = BedrockAgentCore(offline_mode=True)
    mock_contexts = [
        {"source": "Graph Community COMM-00", "summary": "EU CSDDD requires supply chain due diligence."},
        {"source": "Graph Community COMM-01", "summary": "SEC Item 1508 requires disclosure of foreign fines."}
    ]
    query = "Synthesize cross-border environmental liabilities for telecom conglomerates."
    resp = agent.synthesize_compliance_brief(query, mock_contexts, retrieval_mode="graphrag")

    assert "answer" in resp
    assert "CSDDD" in resp["answer"]
    assert "SEC" in resp["answer"]
    assert "NERC" in resp["answer"]
    assert "Statutory Citations:" in resp["answer"]
    assert resp["retrieval_mode"] == "graphrag"


def test_bedrock_agent_synthesis_naive_rag():
    agent = BedrockAgentCore(offline_mode=True)
    mock_contexts = [
        {"source": "eu_csddd_directive.txt", "text": "Article 6 due diligence."}
    ]
    query = "What are the Scope disclosures?"
    resp = agent.synthesize_compliance_brief(query, mock_contexts, retrieval_mode="naive_rag")

    assert "answer" in resp
    assert "Naive Vector RAG" in resp["answer"]
    assert "Limitation" in resp["answer"]
