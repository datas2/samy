from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class PartitioningSkill(DbaSkillBase):
    """DBA partitioning skill for explaining, optimizing and reviewing partitioning strategies."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="partitioning", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain partitioning strategies (range, hash, list, etc.)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain partitioning strategies and when to apply them.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize partitioning for performance and manageability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize partitioning schemes for query performance and maintenance.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that depend on partitioning."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review partitioning-related architectural patterns for best practices.",
            description=description,
            context=context,
        )