"""Tests for GraphRAG entity, relationship, and community extraction."""

import os
import tempfile
import pandas as pd
import pytest
from src.core.graph_extractor import GraphRAGExtractor, GraphCommunityReport


def test_graph_builder_creation():
    extractor = GraphRAGExtractor()
    g = extractor.build_graph()

    assert len(g.nodes) >= 10
    assert len(g.edges) >= 10
    assert "EU_CSDDD_Directive" in g.nodes
    assert "Telecommunications_Conglomerate" in g.nodes
    assert "Critical_Transformer_Substation" in g.nodes


def test_graph_community_extraction():
    extractor = GraphRAGExtractor()
    extractor.build_graph()
    reports = extractor.extract_communities()

    assert len(reports) >= 2
    for rep in reports:
        assert isinstance(rep, GraphCommunityReport)
        assert rep.community_id.startswith("COMM-")
        assert len(rep.entities) >= 1
        assert len(rep.findings) >= 1
        assert rep.rating > 0.80


def test_parquet_artifact_serialization():
    with tempfile.TemporaryDirectory() as tmp_dir:
        extractor = GraphRAGExtractor(artifacts_dir=tmp_dir)
        paths = extractor.save_parquet_artifacts()

        assert os.path.exists(paths["entities"])
        assert os.path.exists(paths["relationships"])
        assert os.path.exists(paths["communities"])

        # Validate Parquet contents via Pandas
        df_ent = pd.read_parquet(paths["entities"])
        df_rel = pd.read_parquet(paths["relationships"])
        df_comm = pd.read_parquet(paths["communities"])

        assert len(df_ent) >= 10
        assert len(df_rel) >= 10
        assert len(df_comm) >= 2
        assert "name" in df_ent.columns
        assert "source" in df_rel.columns
        assert "summary" in df_comm.columns
