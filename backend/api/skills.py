from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.skills.registry import SkillRegistry

router = APIRouter(prefix="/skills", tags=["skills"])

_skill_registry = SkillRegistry()


class SkillRequest(BaseModel):
    """Generic payload for calling a skill operation."""
    description: str = Field(
        ...,
        description="Natural language description of the problem, scenario or code.",
    )
    context: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional contextual information (e.g., tool='powerbi', db='postgres').",
    )


class SkillResponse(BaseModel):
    """Generic response for a skill operation."""
    result: str


@router.post(
    "/{domain}/{skill}/{operation}",
    response_model=SkillResponse,
    summary="Invoke a specific skill operation",
)
def call_skill(
    domain: str,
    skill: str,
    operation: str,
    payload: SkillRequest,
) -> SkillResponse:
    """
    Invoke a specific skill operation for a given domain and skill.

    Examples:
      - POST /skills/sql/explain/explain
      - POST /skills/python/refactor/refactor
      - POST /skills/gcp/bigquery/optimize
      - POST /skills/dba/indexes/review_architecture
      - POST /skills/analytics/dashboard/design

    The payload `description` describes the scenario or code, and `context`
    provides additional structured hints (such as tool, database, or environment).
    """
    try:
        skill_instance = _skill_registry.get_skill(domain, skill)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    op_name = operation.lower()

    if not hasattr(skill_instance, op_name):
        raise HTTPException(
            status_code=400,
            detail=f"Operation '{operation}' not supported by skill '{domain}/{skill}'.",
        )

    op = getattr(skill_instance, op_name)
    if not callable(op):
        raise HTTPException(
            status_code=400,
            detail=f"Operation '{operation}' on skill '{domain}/{skill}' is not callable.",
        )

    # Skills follow a common signature: (description, context) or (query, context)
    # We standardize on description/context here.
    try:
        result: str = op(description=payload.description, context=payload.context)  # type: ignore[arg-type]
    except TypeError as exc_type_error:
        if domain.lower() not in {"sql", "gcp", "dba", "analytics"}:
            # For domains like python/go, a TypeError is a real error in the skill
            raise HTTPException(
                status_code=500,
                detail=f"Error invoking skill operation: {exc_type_error}",
            ) from exc_type_error
        try:
            result = op(query=payload.description, context=payload.context)  # type: ignore[arg-type]
        except Exception as exc:  # real error in the skill
            raise HTTPException(
                status_code=500,
                detail=f"Error invoking skill operation: {exc}",
            ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error invoking skill operation: {exc}",
        ) from exc

    return SkillResponse(result=result)