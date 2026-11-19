"""Cloud Security: Automated Guardrails and Sensitive Data Redaction Engine."""

import re
from typing import Dict, List, Tuple


class ComplianceGuardrails:
    """Detects and redacts sensitive corporate credentials, PII, and infrastructure keys."""

    PATTERNS = [
        ("EMAIL_ADDRESS", r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]"),
        ("TAX_SSN_ID", r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_TAX_ID]"),
        ("IPV4_ADDRESS", r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", "[REDACTED_IP]"),
        ("GRID_CREDENTIAL", r"\bGRID-KEY-[A-Z0-9]{8}\b", "[CONFIDENTIAL_GRID_CREDENTIAL]"),
    ]

    def redact_sensitive_data(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Scans input text, replaces sensitive matches, and reports detection counts."""
        redacted_text = text
        detections = {}

        for name, pattern, replacement in self.PATTERNS:
            matches = re.findall(pattern, redacted_text)
            if matches:
                detections[name] = len(matches)
                redacted_text = re.sub(pattern, replacement, redacted_text)

        return redacted_text, detections

    def is_clean(self, text: str) -> bool:
        """Returns True if no sensitive patterns are found."""
        _, detections = self.redact_sensitive_data(text)
        return len(detections) == 0
