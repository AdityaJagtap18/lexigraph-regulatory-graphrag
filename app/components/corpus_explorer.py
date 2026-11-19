"""Corpus explorer component for browsing regulatory directives."""

from typing import Dict, List
import streamlit as st
from src.core.corpus_loader import DocumentChunk


def render_corpus_explorer(documents: Dict[str, str], chunks: List[DocumentChunk]):
    """Renders regulatory directives browser and document chunk inspector."""
    st.subheader("1. Cross-Border Regulatory Corpus Explorer")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Regulatory Directives")
        selected_doc = st.selectbox("Select Statute", list(documents.keys()))
        if selected_doc:
            doc_text = documents[selected_doc]
            st.caption(f"Document Size: {len(doc_text):,} characters | Chunks: {len([c for c in chunks if c.document_name == selected_doc])}")

            # Highlight specific statutes
            if "csddd" in selected_doc.lower():
                st.info("🇪🇺 **EU CSDDD (2024/1760):** Mandatory supply-chain due diligence, tier-1 contractual assurances, and 5% global turnover sanctions.")
            elif "sec" in selected_doc.lower():
                st.info("🇺🇸 **US SEC Climate Disclosures:** Regulation S-K Scope 1-3 GHG reporting and Item 1508 cross-border foreign penalty trigger.")
            elif "resilience" in selected_doc.lower():
                st.info("⚡ **NERC CIP-014 & NIS2:** Critical substation physical protection, High-Impact Critical Infrastructure (HICI), and 72-hr battery buffers.")

    with col2:
        if selected_doc:
            st.markdown(f"### Full Statute Content: `{selected_doc}`")
            with st.container(height=260):
                st.text(documents[selected_doc])

    with st.expander("Inspect Processed Document Chunks", expanded=False):
        doc_chunks = [c for c in chunks if c.document_name == selected_doc]
        st.markdown(f"Showing **{len(doc_chunks)}** chunks for `{selected_doc}`:")
        for chk in doc_chunks:
            st.markdown(f"**[{chk.chunk_id}] {chk.section_title}** ({chk.token_count} tokens)")
            st.caption(chk.text[:250] + "...")
