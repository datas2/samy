from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class ClusteringSkill(DbaSkillBase):
    """DBA clustering skill for explaining, optimizing and reviewing clustering strategies."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="clustering", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain clustering strategies (table clustering, sharding, etc.)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain clustering strategies and when to apply them.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize clustering configurations for performance."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize clustering for query performance and maintenance.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that rely on clustering for scalability."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review clustering-related architectural patterns for best practices.",
            description=description,
            context=context,
        )