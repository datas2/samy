from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class GcpSecuritySkill(GcpSkillBase):
    """GCP security skill for explain, optimize, configuration and architectural review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="GCP Security", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to implement security controls on GCP."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to implement security controls on GCP for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize security posture for least privilege and compliance."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize GCP security posture for least privilege, compliance and manageability.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure security controls (policies, org policies, etc.)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure GCP security controls for this scenario.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures from a GCP security perspective."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review GCP architectures for security best practices and risks.",
            description=description,
            context=context,
        )