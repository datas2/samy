from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class GcpMonitoringSkill(GcpSkillBase):
    """GCP monitoring skill for explain, optimize and architectural review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Cloud Monitoring", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to set up monitoring for GCP workloads."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design and configure monitoring for GCP workloads.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize monitoring dashboards, alerts and metrics."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize monitoring dashboards, alerts and metrics for signal-to-noise ratio.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review monitoring strategies in an architecture."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review monitoring strategies for coverage and effectiveness.",
            description=description,
            context=context,
        )