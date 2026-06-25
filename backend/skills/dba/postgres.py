from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class PostgresSkill(DbaSkillBase):
    """DBA Postgres skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="postgres", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design and operate Postgres instances."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design, configure and operate Postgres for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Postgres for performance (indexes, configs, queries)."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Postgres performance (indexes, configs, query tuning).",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest ways to reduce operational costs for Postgres."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Postgres costs via sizing, storage tuning and maintenance.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Postgres (parameters, replication, backups)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Postgres parameters, replication and backups.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that use Postgres as a primary database."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review architectures using Postgres for best practices and resilience.",
            description=description,
            context=context,
        )