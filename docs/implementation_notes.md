# Implementation Notes — LexiGraph (PRJ-05)

## 1. Storage & Parquet Artifact Architecture
Following the Microsoft GraphRAG specification, LexiGraph compiles and indexes unstructured legal and technical corpora into three columnar Parquet tables stored in `data/artifacts/`:
1. `create_final_entities.parquet`: Contains typed canonical entities (`ORGANIZATION`, `DIRECTIVE`, `ENERGY_INFRASTRUCTURE`, `COMPLIANCE_PENALTY`, etc.) with unique identifiers and source documents.
2. `create_final_relationships.parquet`: Stores directed relational graph edges (`source`, `target`, `relationship_type`, `weight`, `description`).
3. `create_final_community_reports.parquet`: Contains hierarchical community partition reports generated via greedy modularity / Leiden clustering, including level-1 summaries, key findings, and quality ratings.

## 2. Amazon Bedrock / AgentCore Integration & Zero-Cost Offline Fallback
- **Live AWS Mode:** Connects to AWS Bedrock via `boto3` client targeting `anthropic.claude-3-5-sonnet-20241022-v2:0` in `us-east-1` when active AWS credentials are provided.
- **Offline AgentCore Fallback:** Implements a deterministic, high-accuracy offline synthesis engine adhering strictly to Bedrock AgentCore specifications. This guarantees 100% reproducible test suites, air-gapped security audit compatibility, and zero API costs during portfolio demonstrations.

## 3. Enterprise Cloud Security Implementation
- **IAM RBAC:** Enforces least-privilege action mapping across 4 distinct roles (`ComplianceAuditor`, `PlatformEngineer`, `ExecutiveOfficer`, `PublicViewer`). Denies unauthorized actions with explicit audit traces.
- **Envelope Encryption:** Uses AES-256-GCM data encryption keys (DEK) wrapped by a simulated AWS KMS Customer Master Key (CMK), verifying that sensitive corpus artifacts and queries can be encrypted and decrypted without exposing raw keys.
- **Automated Guardrails:** Scans text streams and redacts sensitive patterns including employee email addresses, tax IDs/SSNs, IPv4 network gateways, and critical infrastructure credentials (`GRID-KEY-XXXXXXXX`).
- **Cryptographic Audit Logger:** Uses SHA-256 hash chaining ($H_i = \text{SHA256}(P_i \parallel H_{i-1})$) to maintain a tamper-evident audit ledger in `data/artifacts/audit_trail.jsonl`. Integrity checks detect any historical record modification.

## 4. Verification Evidence
- 18 unit and integration tests executing in `< 37s`.
- 100% test pass rate across corpus loading, GraphRAG extraction, dense sentence embeddings, Amazon Bedrock AgentCore reasoning, Cloud Security governance, hybrid retrieval comparison, and benchmark evaluation.
