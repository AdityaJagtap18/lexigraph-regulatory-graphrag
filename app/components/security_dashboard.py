"""Cloud Security and Governance dashboard component."""

import streamlit as st
from src.security.access_control import IAMAccessControl
from src.security.encryption_service import KMSEnvelopeEncryptionService
from src.security.guardrails import ComplianceGuardrails
from src.security.audit_logger import CryptographicAuditLogger


def render_security_dashboard(
    rbac: IAMAccessControl,
    kms: KMSEnvelopeEncryptionService,
    guardrails: ComplianceGuardrails,
    logger: CryptographicAuditLogger
):
    """Renders the enterprise Cloud Security & IAM Governance console."""
    st.subheader("4. Enterprise Cloud Security & Compliance Governance Console")

    tab_rbac, tab_kms, tab_guard, tab_audit = st.tabs([
        "🛡️ IAM RBAC Policies",
        "🔐 AWS KMS Envelope Encryption",
        "🛑 Redaction Guardrails",
        "📜 Cryptographic Audit Log"
    ])

    with tab_rbac:
        st.markdown("### IAM Least-Privilege Role-Based Access Control")
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_role = st.selectbox("Active Query Identity Role", list(rbac.ROLES.keys()))
            requested_action = st.selectbox("Requested API Action", [
                "graph:read",
                "graph:query_global",
                "graph:write",
                "security:configure",
                "audit:view",
                "public:view"
            ])
            authorized = rbac.is_authorized(selected_role, requested_action)
            if authorized:
                st.success(f"✅ ACTION ALLOWED: `{selected_role}` is authorized for `{requested_action}`.")
            else:
                st.error(f"❌ ACCESS DENIED: `{selected_role}` is NOT authorized for `{requested_action}`.")

        with col2:
            st.markdown("#### Registered IAM Role Policies")
            for r in rbac.list_roles():
                st.markdown(f"**{r['role_name']}:** {r['description']}")
                st.caption(f"Allowed Permissions: `{', '.join(r['permissions'])}`")

    with tab_kms:
        st.markdown("### AWS KMS Envelope Encryption (AES-256-GCM)")
        st.caption(f"Configured CMK Key ARN: `{kms.kms_key_arn}`")

        sample_secret = st.text_area(
            "Regulatory Corpus Artifact to Encrypt:",
            value="EU Subsea Cellular Cable Backhaul Route & Critical Substation Transformer Specifications v4.2"
        )
        if st.button("🔒 Encrypt with KMS Envelope (AES-256-GCM)"):
            envelope = kms.encrypt_payload(sample_secret)
            st.session_state["encrypted_envelope"] = envelope
            st.success("Envelope encryption completed! DEK generated and wrapped with KMS CMK.")

        if "encrypted_envelope" in st.session_state:
            env = st.session_state["encrypted_envelope"]
            st.json(env)
            if st.button("🔓 Decrypt Envelope with CMK"):
                decrypted = kms.decrypt_payload(env)
                st.info(f"Decrypted Plaintext: **{decrypted}**")

    with tab_guard:
        st.markdown("### Automated PII & Sensitive Infrastructure Key Guardrails")
        guard_input = st.text_area(
            "Audit Inquiry or Log Text to Sanitize:",
            value="Auditor contact: legal-audit@telecom-energy.eu, Tax ID: 345-67-8901, Gateway IP: 10.0.4.155, Auth: GRID-KEY-ZX881234."
        )
        if st.button("🛡️ Execute Redaction Filter"):
            redacted, detections = guardrails.redact_sensitive_data(guard_input)
            st.markdown("#### Redacted Text Stream:")
            st.code(redacted, language="text")
            st.markdown(f"**Detected Sensitive Patterns ({sum(detections.values())} total):**")
            for k, v in detections.items():
                st.caption(f"- `{k}`: {v} instance(s) redacted")

    with tab_audit:
        st.markdown("### Immutable Cryptographic Audit Log (SHA-256 Chained)")
        valid, count = logger.verify_integrity()
        if valid:
            st.success(f"Audit Trail Integrity Verified: **{count} records** validly chained with zero tampering.")
        else:
            st.error(f"Audit Trail Compromised at record index {count}!")

        if st.button("➕ Log Sample Compliance Event"):
            record = logger.log_event(
                event_type="COMPLIANCE_SYNTHESIS_REQUEST",
                identity_role=selected_role if 'selected_role' in locals() else "ComplianceAuditor",
                action="graph:query_global",
                details={"statute": "EU_CSDDD_Article_20", "query_hash": "sha256:4a8b..."}
            )
            st.success("Event appended to hash-chained log!")
            st.json(record)
