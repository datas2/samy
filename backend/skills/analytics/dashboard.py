from __future__ import annotations

from typing import Dict, Optional

from backend.skills.analytics.base import AnalyticsSkillBase


class DashboardSkill(AnalyticsSkillBase):
    """Analytics dashboard skill for explain, design, optimization and review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="dashboards", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design dashboards in Power BI, Tableau or Metabase."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design effective dashboards for this use case.",
            description=description,
            context=context,
        )

    def design(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Design a dashboard layout, including pages, visuals and interactions."""
        return self._rag_and_llm(
            operation="design",
            objective="Design a dashboard layout (pages, visuals, interactions) for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize dashboards for performance and usability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize dashboards for performance, usability and maintainability.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review dashboard architecture and data flows (models, refresh, permissions)."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review dashboard architecture, data flows and refresh strategies for best practices.",
            description=description,
            context=context,
        )