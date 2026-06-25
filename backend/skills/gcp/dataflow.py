from __future__ import annotations

from typing import Dict, Optional

from backend.skills.gcp.base import GcpSkillBase


class DataflowSkill(GcpSkillBase):
    """GCP Dataflow skill for explain, optimize, cost reduction, config and architecture review."""

    def __init__(self, **kwargs) -> None:
        super().__init__(service_name="Dataflow", **kwargs)

    def explain(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to design and run pipelines on Dataflow."""
        return self._rag_and_llm(
            operation="explain",
            objective="Explain how to design and run pipelines on Dataflow.",
            description=description,
            context=context,
        )

    def optimize(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Optimize Dataflow jobs for performance and stability."""
        return self._rag_and_llm(
            operation="optimize",
            objective="Optimize Dataflow jobs for performance and robustness.",
            description=description,
            context=context,
        )

    def reduce_costs(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Suggest cost reductions for Dataflow."""
        return self._rag_and_llm(
            operation="reduce_costs",
            objective="Reduce Dataflow costs via autoscaling, worker tuning and efficient transforms.",
            description=description,
            context=context,
        )

    def configure(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Explain how to configure Dataflow jobs and templates."""
        return self._rag_and_llm(
            operation="configure",
            objective="Explain how to configure Dataflow for this scenario.",
            description=description,
            context=context,
        )

    def review_architecture(self, description: str, context: Optional[Dict[str, str]] = None) -> str:
        """Review architectures that use Dataflow as processing layer."""
        return self._rag_and_llm(
            operation="review_architecture",
            objective="Review Dataflow-based architectures for best practices and cost efficiency.",
            description=description,
            context=context,
        )