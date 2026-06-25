from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class GcpObservabilitySkill(GcpSkillBase):
    """GCP observability skill for explain, optimize and architectural review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Observability", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design observability (logs, metrics, traces) on GCP."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design observability (logs, metrics, traces) for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize observability pipelines and configurations."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize observability pipelines and configurations for cost and usefulness.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest ways to reduce observability costs (logs, metrics storage)."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce observability costs via sampling, retention policies and aggregation.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review observability aspects of an architecture."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review observability architecture for coverage, cost and effectiveness.",
            description=description,
            context=context,
        )