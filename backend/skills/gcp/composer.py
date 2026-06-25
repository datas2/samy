from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class ComposerSkill(GcpSkillBase):
    """GCP Cloud Composer skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Cloud Composer", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to orchestrate pipelines with Cloud Composer."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design and operate pipelines with Cloud Composer.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Composer environments and DAGs."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Cloud Composer DAGs and environments for reliability and performance.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost reductions for Cloud Composer."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Cloud Composer costs via environment sizing and scheduling strategies.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Composer environments."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Cloud Composer for this scenario.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that use Composer as orchestration."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review architectures orchestrated by Cloud Composer for best practices.",
            description=description,
            context=context,
        )