from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class GcpCostAnalysisSkill(GcpSkillBase):
    """GCP cost analysis skill for explain, optimization and architectural review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Cost Analysis", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how costs are generated and measured in a GCP setup."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how costs are generated and measured in this GCP setup.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest optimizations to reduce costs across GCP services."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Suggest optimizations to reduce costs across GCP services involved.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review an architecture from a cost perspective."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review the architecture from a cost perspective and suggest improvements.",
            description=description,
            context=context,
        )