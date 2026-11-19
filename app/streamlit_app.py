"""LexiGraph — Enterprise Regulatory & Multi-Hop Compliance Knowledge Graph.

Demonstration UI showcasing:
Microsoft GraphRAG -> Sentence-Transformers -> Amazon Bedrock / AgentCore -> Cloud Security.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from src.core.corpus_loader import RegulatoryCorpusLoader
from src.core.graph_extractor import GraphRAGExtractor
from src.core.embedding_engine import SentenceEmbeddingEngine
from src.core.bedrock_agent import BedrockAgentCore
from src.core.hybrid_retriever import HybridComplianceRetriever
from src.security.access_control import IAMAccessControl
from src.security.encryption_service import KMSEnvelopeEncryptionService
from src.security.guardrails import ComplianceGuardrails
from src.security.audit_logger import CryptographicAuditLogger
from src.services.benchmark_evaluator import ComplianceBenchmarkEvaluator

from app.components.corpus_explorer import render_corpus_explorer
from app.components.graph_visualizer import render_graph_visualizer
from app.components.query_comparison import render_query_comparison
from app.components.security_dashboard import render_security_dashboard
from app.components.benchmark_panel import render_benchmark_panel

st.set_page_config(
    page_title="LexiGraph — Regulatory Knowledge Graph",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%); padding: 22px 28px; border-radius: 12px; margin-bottom: 24px; color: white;">
    <h1 style="color: white; margin: 0 0 6px 0; font-size: 26px;">🕸️ LexiGraph: Regulatory Knowledge Graph & Compliance Synthesis</h1>
    <p style="color: #c7d2fe; margin: 0; font-size: 14px;">
        Multi-hop cross-border compliance reasoning for Telecommunications & Energy conglomerates powered by Microsoft GraphRAG, Sentence-Transformers, Amazon Bedrock / AgentCore, and Cloud Security.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize services in session state
if "retriever" not in st.session_state:
    retriever = HybridComplianceRetriever()
    retriever.initialize()
    st.session_state["retriever"] = retriever

retriever = st.session_state["retriever"]

if "agent" not in st.session_state:
    st.session_state["agent"] = BedrockAgentCore(offline_mode=True)

agent = st.session_state["agent"]

if "rbac" not in st.session_state:
    st.session_state["rbac"] = IAMAccessControl()
if "kms" not in st.session_state:
    st.session_state["kms"] = KMSEnvelopeEncryptionService()
if "guardrails" not in st.session_state:
    st.session_state["guardrails"] = ComplianceGuardrails()
if "audit_logger" not in st.session_state:
    st.session_state["audit_logger"] = CryptographicAuditLogger()
if "evaluator" not in st.session_state:
    st.session_state["evaluator"] = ComplianceBenchmarkEvaluator(retriever=retriever)

rbac = st.session_state["rbac"]
kms = st.session_state["kms"]
guardrails = st.session_state["guardrails"]
audit_logger = st.session_state["audit_logger"]
evaluator = st.session_state["evaluator"]

# Sidebar controls
st.sidebar.title("LexiGraph Controls")
st.sidebar.markdown("### Assigned Technology Stack")
st.sidebar.markdown("""
- **Graph Engine:** `Microsoft GraphRAG`
- **Dense Vectors:** `Sentence-Transformers`
- **Orchestration:** `Amazon Bedrock / AgentCore`
- **Governance:** `Cloud Security (IAM, KMS, Audit)`
- **Presentation:** `Streamlit`
""")

st.sidebar.divider()
offline_toggle = st.sidebar.checkbox("AgentCore Offline Mode", value=True)
agent.offline_mode = offline_toggle

if st.sidebar.button("Re-Index Graph & Parquet Tables", use_container_width=True):
    with st.spinner("Extracting entities, building communities, and writing Parquet tables..."):
        extractor = GraphRAGExtractor()
        extractor.build_graph()
        extractor.extract_communities()
        paths = extractor.save_parquet_artifacts()
        retriever.community_reports = extractor.community_reports
        retriever.graph_extractor = extractor
    st.sidebar.success("Parquet tables successfully regenerated in `data/artifacts/`!")

st.sidebar.divider()
st.sidebar.caption("Portfolio Project PRJ-05 | Enterprise AI & Data Portfolio")

# 1. Corpus Explorer
docs = retriever.corpus_loader.load_documents()
render_corpus_explorer(docs, retriever.chunks)

st.divider()

# 2. Graph Visualizer
render_graph_visualizer(
    retriever.graph_extractor.entities,
    retriever.graph_extractor.relationships,
    retriever.community_reports
)

st.divider()

# 3. Query Comparison
render_query_comparison(retriever, agent)

st.divider()

# 4. Security Console
render_security_dashboard(rbac, kms, guardrails, audit_logger)

st.divider()

# 5. Benchmarks Panel
render_benchmark_panel(evaluator)
