from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class IAMSkill(GcpSkillBase):
    """GCP IAM skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="IAM", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design IAM policies and roles."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design IAM roles and policies for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize IAM for least privilege and maintainability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize IAM policies for least privilege and maintainability.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """IAM is not directly costed, but can influence usage; still provide guidance."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Explain how IAM design can indirectly reduce costs via better isolation and control.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure IAM (roles, bindings, service accounts)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure IAM roles, bindings and service accounts.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review IAM-related aspects of architectures."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review IAM architecture for security and best practices.",
            description=description,
            context=context,
        )