from __future__ import annotations

from typing import Dict, Optional

from backend.skills.dba.base import DbaSkillBase


class BackupRestoreSkill(DbaSkillBase):
    """DBA backup/restore skill for explaining, optimizing and reviewing backup strategies."""

    def __init__(self, **kwargs) -> None:
        super().__init__(topic_name="backup_restore", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain backup and restore strategies (full, incremental, PITR)."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain backup and restore strategies including full, incremental and point-in-time recovery.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize backup/restore for RPO/RTO and operational overhead."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize backup and restore plans for RPO/RTO and operational efficiency.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review backup/restore aspects of an architecture."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review backup and restore architecture for resilience and compliance.",
            description=description,
            context=context,
        )