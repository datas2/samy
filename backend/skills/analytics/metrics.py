from __future__ import annotations

from typing import Dict, Optional

from backend.skills.analytics.base import AnalyticsSkillBase


class MetricsSkill(AnalyticsSkillBase):
    """Analytics metrics skill for defining, optimizing and reviewing analytical metrics."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="metrics", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to define metrics (dimensions, aggregations, grain)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to define analytical metrics (grain, dimensions, aggregations).",
            description=description,
            context=context,
        )

    def design(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Design metric definitions for reporting and analysis."""
        return self._rag_and_llm(
            operation="design",
            objective="Design metric definitions for reporting and analysis, including naming and semantics.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize metric definitions for correctness and performance."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize metric definitions for correctness, reuse and performance.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review metric layer architecture (semantic models, metric stores)."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review metric layer architecture (semantic models, metric stores) for best practices.",
            description=description,
            context=context,
        )