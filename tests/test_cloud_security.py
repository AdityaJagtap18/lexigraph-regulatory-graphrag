"""Tests for Cloud Security: IAM RBAC, KMS Envelope Encryption, Guardrails, and Audit Logging."""

import os
import tempfile
import pytest

from src.security.access_control import IAMAccessControl
from src.security.encryption_service import KMSEnvelopeEncryptionService
from src.security.guardrails import ComplianceGuardrails
from src.security.audit_logger import CryptographicAuditLogger


def test_iam_rbac_authorization():
    rbac = IAMAccessControl()

    # ComplianceAuditor has read & query access
    assert rbac.is_authorized("ComplianceAuditor", "graph:read") is True
    assert rbac.is_authorized("ComplianceAuditor", "graph:query_global") is True
    # ComplianceAuditor cannot configure security
    assert rbac.is_authorized("ComplianceAuditor", "security:configure") is False

    # PlatformEngineer has full configuration access
    assert rbac.is_authorized("PlatformEngineer", "security:configure") is True

    # PublicViewer has only public:view
    assert rbac.is_authorized("PublicViewer", "graph:read") is False
    assert rbac.is_authorized("PublicViewer", "public:view") is True

    # Unknown role
    assert rbac.is_authorized("HackerRole", "graph:read") is False


def test_kms_envelope_encryption_roundtrip():
    kms = KMSEnvelopeEncryptionService()
    plaintext = "CONFIDENTIAL: European Subsea Fiber Backbone Cable Specification v4"

    # Encrypt
    envelope = kms.encrypt_payload(plaintext)
    assert envelope["algorithm"] == "AES-256-GCM"
    assert "ciphertext" in envelope
    assert "encrypted_data_key" in envelope
    assert envelope["ciphertext"] != plaintext

    # Decrypt
    decrypted = kms.decrypt_payload(envelope)
    assert decrypted == plaintext


def test_compliance_guardrails_redaction():
    guardrails = ComplianceGuardrails()
    sensitive_input = (
        "Auditor contact: john.doe@telecom-grid.eu, Tax ID: 123-45-6789, "
        "Substation gateway IP: 192.168.1.105 with active key GRID-KEY-AB991200."
    )

    assert guardrails.is_clean(sensitive_input) is False

    redacted, counts = guardrails.redact_sensitive_data(sensitive_input)

    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_TAX_ID]" in redacted
    assert "[REDACTED_IP]" in redacted
    assert "[CONFIDENTIAL_GRID_CREDENTIAL]" in redacted

    assert "john.doe@telecom-grid.eu" not in redacted
    assert "123-45-6789" not in redacted
    assert "192.168.1.105" not in redacted
    assert "GRID-KEY-AB991200" not in redacted

    assert counts["EMAIL_ADDRESS"] == 1
    assert counts["TAX_SSN_ID"] == 1
    assert counts["IPV4_ADDRESS"] == 1
    assert counts["GRID_CREDENTIAL"] == 1


def test_cryptographic_audit_logger_hash_chain():
    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file = os.path.join(tmp_dir, "test_audit.jsonl")
        logger = CryptographicAuditLogger(log_path=log_file)

        # Log 3 events
        logger.log_event("QUERY_SUBMITTED", "ComplianceAuditor", "graph:query_global", {"query": "Test query 1"})
        logger.log_event("ENCRYPTION_EXECUTED", "PlatformEngineer", "security:encrypt", {"status": "success"})
        logger.log_event("REPORT_DOWNLOADED", "ExecutiveOfficer", "graph:view", {"format": "pdf"})

        # Verify integrity
        valid, count = logger.verify_integrity()
        assert valid is True
        assert count == 3
