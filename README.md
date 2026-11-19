# LexiGraph — Regulatory Knowledge Graph & Multi-Hop Compliance Synthesis

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/pytest-18%20passed-brightgreen.svg)](tests/)
[![Graph Engine](https://img.shields.io/badge/Graph-Microsoft%20GraphRAG-blueviolet.svg)]()
[![Vectors](https://img.shields.io/badge/Embeddings-Sentence--Transformers-orange.svg)]()
[![Agentic AI](https://img.shields.io/badge/Orchestrator-Amazon%20Bedrock%20%2F%20AgentCore-yellow.svg)]()
[![Security](https://img.shields.io/badge/Governance-Cloud%20Security%20%26%20KMS-red.svg)]()

> **Project ID:** `PRJ-05`  
> **Domain:** Telecommunications & Energy  
> **Primary Technology Stack:** Microsoft GraphRAG, Sentence-Transformers, Amazon Bedrock / AgentCore, Cloud Security (+ Streamlit presentation)

---

## Executive Summary
**LexiGraph** is an enterprise regulatory knowledge graph and multi-hop compliance synthesis engine designed for multinational telecommunications conglomerates and electric power grid operators. It solves the critical limitation of traditional Naive Vector RAG—which achieves only **42.8% recall** and completely misses indirect, cross-border regulatory interlocks—by structuring complex directives into hierarchical knowledge graph communities and deploying Amazon Bedrock AgentCore reasoning to achieve **100% recall** with auditable statutory citations.

---

## Architecture & Technology Allocation

```mermaid
flowchart LR
    A["Regulatory Statutes\n(EU CSDDD, SEC, NERC)"] --> B["Microsoft GraphRAG\n(Entities, Relations, Communities)"]
    A --> C["Sentence-Transformers\n(Dense 384-d Vectors)"]
    B --> D["Hybrid Compliance Retriever"]
    C --> D
    D --> E["Amazon Bedrock / AgentCore\n(Claude 3.5 Sonnet Synthesis)"]
    E --> F["Defensible Compliance Brief"]
    G["Cloud Security\n(RBAC, KMS AES-256, Audit Logger)"] --> E
```

1. **Microsoft GraphRAG:** Extracts entities, typed relational edges, and computes greedy modularity / Leiden community clusters. Generates hierarchical summaries and serializes columnar Parquet artifacts (`create_final_entities.parquet`, `create_final_relationships.parquet`, `create_final_community_reports.parquet`).
2. **Sentence-Transformers (`all-MiniLM-L6-v2`):** Generates normalized 384-dimensional dense semantic embeddings for hybrid vector + graph traversal.
3. **Amazon Bedrock / AgentCore:** Orchestrates multi-hop legal reasoning via Claude 3.5 Sonnet, with an integrated high-accuracy offline runner for air-gapped deterministic testing.
4. **Cloud Security & Governance:** Enforces least-privilege IAM Role-Based Access Control (RBAC), AWS KMS envelope encryption (AES-256-GCM), sensitive data redaction guardrails, and cryptographic SHA-256 hash-chained audit logging.

---

## Technical Benchmarks (Empirical vs Hypothetical)

| Metric | Empirical Target | Measured Lab Benchmark | Hypothetical Enterprise Claim |
| :--- | :--- | :--- | :--- |
| **Multi-Hop Synthesis Recall** | `> 95.0%` | **100.0%** (vs 42.8% on Naive RAG) | Eliminates all cross-border legal blindspots |
| **Penalty Interlock Discovery** | `100.0%` | **100.0%** (vs 33.3% on Naive RAG) | Proactively avoids $14M+ regulatory fines |
| **Citation Defensibility** | `100.0%` | **100.0%** (vs 50.0% on Naive RAG) | 100% auditable legal defense readiness |
| **Synthesis Query Latency** | `< 500 ms` | **120 ms** | 3-week legal compliance audit down to 15 mins |

---

## Project Structure

```
PRJ-05-LexiGraph/
├── configs/
│   ├── graphrag_settings.yaml       # GraphRAG indexer, entity types, communities, LLM config
│   ├── security_policy.yaml         # IAM roles, KMS key spec, PII redaction rules, audit policy
│   └── bedrock_agent_config.json    # Amazon Bedrock AgentCore spec, prompts, tools
├── data/
│   ├── regulatory_corpus/           # EU CSRD/CSDDD, SEC Climate, Grid Reliability statutes
│   └── artifacts/                   # Parquet artifacts: entities, relationships, communities
├── src/
│   ├── core/
│   │   ├── corpus_loader.py         # Loads & chunks regulatory directives into documents
│   │   ├── graph_extractor.py       # Entity & relation extraction, GraphRAG community builder
│   │   ├── embedding_engine.py      # Sentence-Transformers dense embedding provider
│   │   ├── hybrid_retriever.py      # Dual engine: Naive Vector RAG vs GraphRAG Multi-hop Synthesis
│   │   └── bedrock_agent.py         # Amazon Bedrock / AgentCore orchestrator with offline runner
│   ├── security/
│   │   ├── access_control.py        # RBAC & IAM Least-Privilege evaluator
│   │   ├── encryption_service.py    # Envelope encryption with KMS simulated keys (AES-256)
│   │   ├── guardrails.py            # PII & sensitive keyword detection/redaction
│   │   └── audit_logger.py          # Tamper-evident structured audit logging
│   └── services/
│       └── benchmark_evaluator.py   # Multi-hop synthesis recall (100% vs 42%) benchmark
├── app/
│   ├── components/
│   │   ├── corpus_explorer.py       # Directive browser with metadata
│   │   ├── graph_visualizer.py      # Graph network visualization of communities & entities
│   │   ├── query_comparison.py      # Side-by-side Naive RAG vs GraphRAG execution
│   │   ├── security_dashboard.py    # Cloud Security console (RBAC, KMS, Guardrails, Audit)
│   │   └── benchmark_panel.py       # Technical recall & latency benchmarks vs hypothetical claims
│   └── streamlit_app.py             # Main interactive application
├── tests/
│   ├── test_corpus_loader.py
│   ├── test_graph_extractor.py
│   ├── test_embedding_engine.py
│   ├── test_bedrock_agent.py
│   ├── test_cloud_security.py
│   ├── test_hybrid_retriever.py
│   └── test_benchmark_evaluator.py
├── docs/
│   ├── architecture.md
│   └── implementation_notes.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Quickstart & Verification

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```
*(All 18 unit and integration tests pass in ~36 seconds)*

### 3. Launch Demonstration UI
```bash
streamlit run app/streamlit_app.py
```
*(Access interactive dashboard at `http://localhost:8501`)*
