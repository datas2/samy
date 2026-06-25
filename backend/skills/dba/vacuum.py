from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class VacuumSkill(DbaSkillBase):
    """DBA vacuum/autovacuum skill for explaining, optimizing and reviewing maintenance."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="vacuum", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain VACUUM/autovacuum behavior and configuration."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how VACUUM/autovacuum works and how to configure it.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize VACUUM/autovacuum settings for performance and bloat control."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize VACUUM/autovacuum settings for performance and bloat control.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review maintenance strategies involving VACUUM/autovacuum."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review maintenance strategies involving VACUUM/autovacuum for best practices.",
            description=description,
            context=context,
        )