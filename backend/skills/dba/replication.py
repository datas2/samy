from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class ReplicationSkill(DbaSkillBase):
    """DBA replication skill for explaining, optimizing and reviewing replication strategies."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="replication", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain replication strategies (sync/async, logical/physical, multi-site)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain database replication strategies and when to apply them.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize replication configurations for performance and durability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize replication settings for performance, durability and failover.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that rely on replication for HA/DR."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review replication-based architectures for high availability and disaster recovery.",
            description=description,
            context=context,
        )