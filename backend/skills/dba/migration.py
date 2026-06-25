from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class MigrationSkill(DbaSkillBase):
    """DBA migration skill for explaining, planning and reviewing database migrations."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="migration", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain migration strategies (on-prem to cloud, engine changes, etc.)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain database migration strategies and their trade-offs.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize migration plans for risk, downtime and complexity."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize migration plans to minimize risk, downtime and complexity.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review migration architectures and strategies."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review migration architectures and strategies for best practices.",
            description=description,
            context=context,
        )