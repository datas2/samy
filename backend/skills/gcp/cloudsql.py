from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class CloudSQLSkill(GcpSkillBase):
    """GCP Cloud SQL skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Cloud SQL", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design and operate Cloud SQL instances."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design, provision and operate Cloud SQL for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Cloud SQL for performance (indexes, connections, configs)."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Cloud SQL for performance and reliability.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost reductions for Cloud SQL (instance sizing, storage)."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Cloud SQL costs by adjusting instance size, storage and usage patterns.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Cloud SQL (HA, backups, flags)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Cloud SQL (HA, backups, flags, connectivity).",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures involving Cloud SQL."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review architectures using Cloud SQL for best practices and resilience.",
            description=description,
            context=context,
        )