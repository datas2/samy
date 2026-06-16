from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class CodeContext(BaseModel):
    """
    Optional context about the code or environment.
    """
    language: Optional[str] = Field(
        default=None,
        description="Primary language of the code (python, sql, go, etc.).",
    )
    framework: Optional[str] = Field(
        default=None,
        description="Framework or stack (fastapi, flask, dbt, airflow, etc.).",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        description="Cloud provider (gcp, aws, azure, on-prem, etc.).",
    )
    file_path: Optional[str] = Field(
        default=None,
        description="Path to the file or resource, if applicable.",
    )


class ExplainRequest(BaseModel):
    """
    Request payload for explaining a piece of code or architecture.
    """
    prompt: str = Field(
        ...,
        description="Descriptive text of the problem or question.",
    )
    code: str = Field(
        "",
        description="Code snippet, SQL, or configuration to be explained.",
    )
    context: Optional[CodeContext] = None


class ExplainResponse(BaseModel):
    """
    Response payload for an explanation.
    """
    explanation: str


class ReviewRequest(BaseModel):
    """
    Request payload for reviewing code.
    """
    code: str = Field(
        ...,
        description="Code snippet or SQL to be reviewed.",
    )
    goal: Optional[str] = Field(
        default=None,
        description="Main goal of the review (e.g., 'bugs', 'clean code', 'security').",
    )
    context: Optional[CodeContext] = None


class ReviewIssue(BaseModel):
    """
    Single issue found during code review.
    """
    severity: Literal["info", "warning", "error"] = "info"
    message: str
    suggestion: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None


class ReviewResponse(BaseModel):
    """
    Response payload for code review.
    """
    summary: str
    issues: list[ReviewIssue]


class OptimizeRequest(BaseModel):
    """
    Request payload for optimization suggestions (performance/cost).
    """
    code: str = Field(
        ...,
        description="Code, SQL, or pipeline to be optimized.",
    )
    objective: Optional[str] = Field(
        default=None,
        description="Main objective (e.g., 'performance', 'cost', 'readability').",
    )
    context: Optional[CodeContext] = None


class OptimizeSuggestion(BaseModel):
    """
    Single optimization suggestion.
    """
    title: str
    description: str
    example_before: Optional[str] = None
    example_after: Optional[str] = None
    impact: Optional[str] = None  # e.g., 'reduces cost', 'improves latency'


class OptimizeResponse(BaseModel):
    """
    Response payload for optimization suggestions.
    """
    summary: str
    suggestions: list[OptimizeSuggestion]