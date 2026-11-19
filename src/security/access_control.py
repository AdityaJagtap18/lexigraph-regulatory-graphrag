"""Cloud Security: Role-Based Access Control (RBAC) and IAM Policy Evaluator."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


@dataclass
class IAMRole:
    role_name: str
    description: str
    permissions: Set[str]


class IAMAccessControl:
    """Enforces least-privilege IAM and RBAC access policies for regulatory knowledge graph."""

    ROLES: Dict[str, IAMRole] = {
        "ComplianceAuditor": IAMRole(
            role_name="ComplianceAuditor",
            description="Read-only access to regulatory graph and community reports.",
            permissions={"graph:read", "graph:query_global", "audit:view"}
        ),
        "PlatformEngineer": IAMRole(
            role_name="PlatformEngineer",
            description="Manage indexing, graph extraction, and system maintenance.",
            permissions={"graph:read", "graph:write", "graph:index", "security:configure", "audit:view"}
        ),
        "ExecutiveOfficer": IAMRole(
            role_name="ExecutiveOfficer",
            description="Access executive multi-hop synthesis briefings and risk summaries.",
            permissions={"graph:query_global", "graph:query_local"}
        ),
        "PublicViewer": IAMRole(
            role_name="PublicViewer",
            description="Restricted public role with no access to internal community reports.",
            permissions={"public:view"}
        ),
    }

    def __init__(self, default_role: str = "ComplianceAuditor"):
        self.default_role = default_role

    def is_authorized(self, role_name: str, action: str) -> bool:
        """Evaluates whether the given IAM role is granted the requested action."""
        role = self.ROLES.get(role_name)
        if not role:
            return False
        return action in role.permissions

    def list_roles(self) -> List[Dict[str, Any]]:
        """Returns metadata for all available enterprise IAM roles."""
        return [
            {
                "role_name": r.role_name,
                "description": r.description,
                "permissions": sorted(list(r.permissions))
            }
            for r in self.ROLES.values()
        ]
