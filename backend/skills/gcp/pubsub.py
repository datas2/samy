from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class PubSubSkill(GcpSkillBase):
    """GCP Pub/Sub skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Pub/Sub", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design and operate Pub/Sub topics and subscriptions."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design topics, subscriptions and consumers with Pub/Sub.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Pub/Sub usage for performance and reliability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Pub/Sub usage for performance, reliability and ordering.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost reductions for Pub/Sub usage."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Pub/Sub costs via batching, filtering and efficient consumption.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Pub/Sub (topics, subscriptions, filters)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Pub/Sub topics, subscriptions and filters.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures using Pub/Sub as messaging backbone."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review Pub/Sub-based architectures for reliability and best practices.",
            description=description,
            context=context,
        )