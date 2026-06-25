from __future__ import annotations

from typing import Dict, Optional

from backend.skills.analytics.base import AnalyticsSkillBase


class KpiSkill(AnalyticsSkillBase):
    """Analytics KPI skill for defining, optimizing and reviewing key performance indicators."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="kpi", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to define KPIs for a given business context."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to define meaningful KPIs for this business context.",
            description=description,
            context=context,
        )

    def design(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Design KPI definitions (formula, segmentation, thresholds)."""
        return self._rag_and_llm(
            operation="design",
            objective="Design KPI definitions (formulas, segments, thresholds) for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize existing KPIs for clarity, actionability and alignment."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize existing KPIs for clarity, actionability and business alignment.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review how KPIs are organized across dashboards and data models."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review KPI architecture across dashboards and models for consistency and governance.",
            description=description,
            context=context,
        )