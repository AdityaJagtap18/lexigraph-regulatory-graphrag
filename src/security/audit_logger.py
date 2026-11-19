"""Cloud Security: Cryptographically Hashed Immutable Audit Logger."""

from datetime import datetime, timezone
import hashlib
import json
import os
from typing import Any, Dict, List, Optional, Tuple


class CryptographicAuditLogger:
    """Records regulatory compliance queries in a hash-chained, tamper-evident log."""

    def __init__(self, log_path: str = "data/artifacts/audit_trail.jsonl"):
        self.log_path = log_path
        self._last_hash = "0" * 64
        self._init_log()

    def _init_log(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.log_path)), exist_ok=True)
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f if l.strip()]
                    if lines:
                        last_record = json.loads(lines[-1])
                        self._last_hash = last_record.get("record_hash", self._last_hash)
            except Exception:
                self._last_hash = "0" * 64

    def log_event(
        self,
        event_type: str,
        identity_role: str,
        action: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Appends a new cryptographically chained audit record."""
        timestamp = datetime.now(timezone.utc).isoformat()

        record_payload = {
            "timestamp": timestamp,
            "event_type": event_type,
            "identity_role": identity_role,
            "action": action,
            "details": details,
            "prev_hash": self._last_hash
        }

        # Compute SHA-256 hash chaining over serialized payload
        serialized = json.dumps(record_payload, sort_keys=True)
        record_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        record_payload["record_hash"] = record_hash
        self._last_hash = record_hash

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_payload) + "\n")

        return record_payload

    def verify_integrity(self) -> Tuple[bool, int]:
        """Verifies mathematical SHA-256 hash chaining across the entire audit log."""
        if not os.path.exists(self.log_path):
            return True, 0

        prev = "0" * 64
        count = 0
        with open(self.log_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                stated_hash = record["record_hash"]

                # Reconstruct payload without record_hash
                check_payload = dict(record)
                check_payload.pop("record_hash")
                expected_hash = hashlib.sha256(
                    json.dumps(check_payload, sort_keys=True).encode("utf-8")
                ).hexdigest()

                if stated_hash != expected_hash or record["prev_hash"] != prev:
                    return False, idx

                prev = stated_hash
                count += 1

        return True, count
