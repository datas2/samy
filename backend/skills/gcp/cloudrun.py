from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class CloudRunSkill(GcpSkillBase):
    """GCP Cloud Run skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Cloud Run", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to deploy and operate services on Cloud Run."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design, deploy and operate this on Cloud Run.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Cloud Run services for performance and scalability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Cloud Run services for performance and scalability.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost optimizations for Cloud Run."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Cloud Run costs via autoscaling, CPU/memory tuning and concurrency.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Cloud Run (revisions, traffic, IAM, env vars)."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Cloud Run for this scenario.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that use Cloud Run as a compute layer."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review Cloud Run-based architectures for best practices and reliability.",
            description=description,
            context=context,
        )