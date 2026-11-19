"""Dual query comparison component: Naive Vector RAG vs. LexiGraph GraphRAG."""

from typing import Any, Dict
import streamlit as st
from src.core.hybrid_retriever import HybridComplianceRetriever
from src.core.bedrock_agent import BedrockAgentCore


def render_query_comparison(retriever: HybridComplianceRetriever, agent: BedrockAgentCore):
    """Renders side-by-side retrieval and Bedrock AgentCore synthesis comparison."""
    st.subheader("3. Dual Retrieval Comparison: Naive Vector RAG vs. LexiGraph GraphRAG")

    sample_queries = [
        "Synthesize cross-border environmental liabilities for telecom and energy conglomerates under EU CSDDD and SEC Regulation S-K.",
        "How does a 5% turnover civil sanction in the EU trigger mandatory disclosure obligations under US SEC Item 1508?",
        "What are the physical resilience, 72-hour battery backup, and power requirements for critical substations under NERC CIP-014 and EU NIS2?",
        "Explain supply chain tier-1 contractual assurances and Scope 3 emissions reporting obligations."
    ]

    query = st.selectbox("Select Compliance Audit Query", sample_queries)
    custom_q = st.text_input("Or enter custom compliance query:", value="")
    final_query = custom_q.strip() if custom_q.strip() else query

    if st.button("🚀 Execute Dual Comparative Retrieval", type="primary", use_container_width=True):
        with st.spinner("Executing Naive Vector RAG & LexiGraph GraphRAG queries..."):
            naive_res = retriever.retrieve_naive_rag(final_query, top_k=3)
            graph_res = retriever.retrieve_graphrag(final_query)

            naive_synth = agent.synthesize_compliance_brief(final_query, naive_res.contexts, retrieval_mode="naive_rag")
            graph_synth = agent.synthesize_compliance_brief(final_query, graph_res.contexts, retrieval_mode="graphrag")

        col1, col2 = st.columns(2)

        with col1:
            st.error("### ❌ Naive Vector RAG (Chunk Top-K)")
            st.markdown(f"- **Multi-Hop Recall:** `{naive_res.multi_hop_recall * 100:.1f}%` (Misses 2nd-degree cross-border link)")
            st.markdown(f"- **Penalty Linkage Covered:** `{'YES' if naive_res.cross_border_penalty_covered else 'NO'}`")
            st.markdown(f"- **Citation Defensibility:** `{naive_res.citation_defensibility * 100:.0f}%`")
            st.markdown(f"- **Retrieval Latency:** `{naive_res.retrieval_time_ms:.1f} ms`")

            st.markdown("#### Retrieved Top-3 Document Chunks:")
            for idx, c in enumerate(naive_res.contexts):
                st.caption(f"**Chunk #{idx + 1} ({c['source']}) — Score: {c['score']:.4f}**")
                st.text(c["text"][:220] + "...")

            st.markdown("#### AgentCore Response (Naive Context):")
            st.markdown(naive_synth["answer"])

        with col2:
            st.success("### ✅ LexiGraph GraphRAG (Microsoft GraphRAG)")
            st.markdown(f"- **Multi-Hop Recall:** `{graph_res.multi_hop_recall * 100:.1f}%` (Complete Cross-Border Synthesis)")
            st.markdown(f"- **Penalty Linkage Covered:** `{'YES' if graph_res.cross_border_penalty_covered else 'NO'}`")
            st.markdown(f"- **Citation Defensibility:** `{graph_res.citation_defensibility * 100:.0f}%`")
            st.markdown(f"- **Retrieval Latency:** `{graph_res.retrieval_time_ms:.1f} ms`")

            st.markdown("#### Retrieved Hierarchical Community Syntheses:")
            for c in graph_res.contexts:
                st.caption(f"**{c['source']} — {c['section']} (Rating: {c['rating'] * 100:.0f}%)**")
                st.caption(c["summary"][:180] + "...")

            st.markdown("#### AgentCore Response (GraphRAG Context):")
            st.markdown(graph_synth["answer"])
