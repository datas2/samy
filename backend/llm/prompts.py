from __future__ import annotations

from typing import Dict, List


def build_explain_messages(
    *,
    prompt: str,
    code: str,
    context: Dict[str, str] | None = None,
    retrieved_context: List[Dict[str, str]] | None = None,
) -> List[Dict[str, str]]:
    """
    Build chat messages for the explain endpoint.

    Focus on clear, technical explanations for data/cloud/engineering scenarios.
    """
    system = (
        "You are Samy, a specialized AI engineering assistant for data, cloud and "
        "analytics. Explain code, SQL or architectures in clear, concise technical "
        "language. Prefer step-by-step reasoning and highlight trade-offs when relevant."
    )

    ctx_lines: list[str] = []
    if context:
        if lang := context.get("language"):
            ctx_lines.append(f"Language: {lang}")
        if fw := context.get("framework"):
            ctx_lines.append(f"Framework: {fw}")
        if cloud := context.get("cloud_provider"):
            ctx_lines.append(f"Cloud: {cloud}")
        if path := context.get("file_path"):
            ctx_lines.append(f"File: {path}")

    context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

    # Build RAG context block if provided
    rag_block_lines: list[str] = []
    if retrieved_context:
        rag_block_lines.append("Relevant knowledge snippets:")
        rag_block_lines.extend(
            f"[{idx}] Source: {item.get('source')} | Offset: {item.get('offset')}\n{item.get('content')}"
            for idx, item in enumerate(retrieved_context, start=1)
        )
    rag_block = "\n\n".join(rag_block_lines) if rag_block_lines else "No retrieved knowledge."

    user_content = (
        f"User question:\n{prompt.strip()}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Retrieved knowledge:\n{rag_block}\n\n"
        f"Code snippet (if any):\n{code.strip() or '[no code provided]'}\n\n"
        "Please explain what this does and any important considerations "
        "(performance, readability, correctness, security)."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]


def build_review_messages(
    *,
    code: str,
    goal: str | None,
    context: Dict[str, str] | None = None,
    retrieved_context: List[Dict[str, str]] | None = None,
) -> List[Dict[str, str]]:
    """
    Build chat messages for the review endpoint.

    Ask the model to return a structured, multi-point review.
    """
    system = (
        "You are Samy, an AI code reviewer specialized in data engineering, analytics "
        "and cloud-native systems. Review code focusing on correctness, clarity, "
        "performance and security, with short, actionable comments."
    )

    goal_str = goal or "general review"
    ctx_lines: list[str] = []
    if context:
        if lang := context.get("language"):
            ctx_lines.append(f"Language: {lang}")
        if fw := context.get("framework"):
            ctx_lines.append(f"Framework: {fw}")
        if cloud := context.get("cloud_provider"):
            ctx_lines.append(f"Cloud: {cloud}")

    context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

    rag_block_lines: list[str] = []
    if retrieved_context:
        rag_block_lines.append("Relevant knowledge snippets:")
        rag_block_lines.extend(
            f"[{idx}] Source: {item.get('source')} | Offset: {item.get('offset')}\n{item.get('content')}"
            for idx, item in enumerate(retrieved_context, start=1)
        )
    rag_block = "\n\n".join(rag_block_lines) if rag_block_lines else "No retrieved knowledge."

    user_content = (
        f"Review goal: {goal_str}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Retrieved knowledge:\n{rag_block}\n\n"
        f"Code to review:\n{code}\n\n"
        "Provide a short summary of the main issues and list concrete suggestions. "
        "Respond in plain text; bullet lists are welcome."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]


def build_optimize_messages(
    *,
    code: str,
    objective: str | None,
    context: Dict[str, str] | None = None,
    retrieved_context: List[Dict[str, str]] | None = None,
) -> List[Dict[str, str]]:
    """
    Build chat messages for the optimize endpoint.

    Focus on performance/cost optimizations for data and cloud workloads.
    """
    system = (
        "You are Samy, an optimization assistant for SQL, ETL pipelines and backend "
        "services. Suggest improvements that reduce latency, cost or complexity, "
        "while keeping correctness."
    )

    obj_str = objective or "performance"
    ctx_lines: list[str] = []
    if context:
        if lang := context.get("language"):
            ctx_lines.append(f"Language: {lang}")
        if fw := context.get("framework"):
            ctx_lines.append(f"Framework: {fw}")
        if cloud := context.get("cloud_provider"):
            ctx_lines.append(f"Cloud: {cloud}")

    context_block = "\n".join(ctx_lines) if ctx_lines else "No extra context."

    rag_block_lines: list[str] = []
    if retrieved_context:
        rag_block_lines.append("Relevant knowledge snippets:")
        rag_block_lines.extend(
            f"[{idx}] Source: {item.get('source')} | Offset: {item.get('offset')}\n{item.get('content')}"
            for idx, item in enumerate(retrieved_context, start=1)
        )
    rag_block = "\n\n".join(rag_block_lines) if rag_block_lines else "No retrieved knowledge."

    user_content = (
        f"Optimization objective: {obj_str}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Retrieved knowledge:\n{rag_block}\n\n"
        f"Code or SQL to optimize:\n{code}\n\n"
        "List specific optimization suggestions and, when possible, show before/after "
        "examples. Focus on realistic improvements for production workloads."
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]