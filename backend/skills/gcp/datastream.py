from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class DatastreamSkill(GcpSkillBase):
    """GCP Datastream skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Datastream", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to set up and operate Datastream pipelines."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to configure and operate Datastream for this scenario.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Datastream configurations and pipelines."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Datastream configurations for performance and reliability.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost reductions for Datastream usage."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Datastream costs via efficient replication strategies.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Datastream sources, routes and destinations."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Datastream sources, routes and destinations.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that use Datastream for change data capture."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review Datastream-based CDC architectures for best practices.",
            description=description,
            context=context,
        )