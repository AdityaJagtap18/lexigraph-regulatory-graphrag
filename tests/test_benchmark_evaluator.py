"""Tests for Compliance Benchmark Evaluator."""

import pytest
from src.core.hybrid_retriever import HybridComplianceRetriever
from src.services.benchmark_evaluator import ComplianceBenchmarkEvaluator


def test_benchmark_evaluator_execution():
    retriever = HybridComplianceRetriever()
    evaluator = ComplianceBenchmarkEvaluator(retriever=retriever)

    bench = evaluator.run_benchmark_suite()

    assert "summary_dataframe" in bench
    assert "metrics" in bench
    assert bench["queries_evaluated"] == 4

    metrics = bench["metrics"]
    assert metrics["naive_recall"] < 0.50
    assert metrics["graphrag_recall"] == 1.000
    assert metrics["recall_gain"] > 0.50
    assert metrics["graph_penalty_rate"] == 1.0
    assert metrics["graph_defensibility"] == 1.0
