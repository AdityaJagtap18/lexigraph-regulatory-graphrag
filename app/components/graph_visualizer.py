"""Graph visualizer and community report inspector component."""

from typing import List
import pandas as pd
import streamlit as st
from src.core.graph_extractor import GraphEntity, GraphRelationship, GraphCommunityReport


def render_graph_visualizer(
    entities: List[GraphEntity],
    relationships: List[GraphRelationship],
    communities: List[GraphCommunityReport]
):
    """Renders hierarchical community reports and knowledge graph relational tables."""
    st.subheader("2. Microsoft GraphRAG Hierarchical Knowledge Graph & Communities")

    tab1, tab2, tab3 = st.tabs(["🏛️ Community Reports (Leiden)", "🏷️ Entities (13)", "🔗 Relationships (12)"])

    with tab1:
        st.markdown("### Hierarchical Community Summaries")
        st.caption("Greedy modularity clustering partitions cross-border statutory provisions into coherent regulatory themes.")

        for comm in communities:
            with st.expander(f"**{comm.community_id}: {comm.title}** (Rating: {comm.rating * 100:.0f}%)", expanded=True):
                st.markdown(f"**Community Summary:** {comm.summary}")
                st.markdown("**Key Regulatory Findings:**")
                for f in comm.findings:
                    st.markdown(f"- {f}")
                col_e, col_r = st.columns(2)
                with col_e:
                    st.markdown(f"**Member Entities ({len(comm.entities)}):**")
                    st.code("\n".join(comm.entities), language="text")
                with col_r:
                    st.markdown(f"**Relational Subgraph ({len(comm.relationships)}):**")
                    st.code("\n".join(comm.relationships), language="text")

    with tab2:
        st.markdown("### Canonical Regulatory Entities")
        df_ent = pd.DataFrame([
            {
                "ID": e.entity_id,
                "Entity Name": e.name,
                "Type": e.type,
                "Description": e.description,
                "Sources": ", ".join(e.source_documents)
            }
            for e in entities
        ])
        st.dataframe(df_ent, use_container_width=True)

    with tab3:
        st.markdown("### Relational Graph Edges (Multi-Hop Links)")
        df_rel = pd.DataFrame([
            {
                "ID": r.relationship_id,
                "Source": r.source,
                "Relationship": f"--[{r.relationship_type}]-->",
                "Target": r.target,
                "Weight": r.weight,
                "Legal Description": r.description
            }
            for r in relationships
        ])
        st.dataframe(df_rel, use_container_width=True)
