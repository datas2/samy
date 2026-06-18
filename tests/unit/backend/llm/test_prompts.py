from __future__ import annotations

from backend.llm.prompts import (
    build_explain_messages,
    build_optimize_messages,
    build_review_messages,
)


def test_build_explain_messages_includes_prompt_code_context_and_rag() -> None:
    messages = build_explain_messages(
        prompt="Explain this function",
        code="def foo(): return 1",
        context={
            "language": "python",
            "framework": "fastapi",
            "cloud_provider": "gcp",
            "file_path": "backend/main.py",
        },
        retrieved_context=[
            {"content": "snippet1", "source": "doc1.md", "offset": 0},
            {"content": "snippet2", "source": "doc2.md", "offset": 10},
        ],
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "Samy" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    user_content = messages[1]["content"]
    assert "Explain this function" in user_content
    assert "def foo(): return 1" in user_content
    assert "Language: python" in user_content
    assert "Framework: fastapi" in user_content
    assert "Cloud: gcp" in user_content
    assert "File: backend/main.py" in user_content
    assert "Relevant knowledge snippets:" in user_content
    assert "snippet1" in user_content
    assert "snippet2" in user_content


def test_build_review_messages_uses_goal_context_and_rag() -> None:
    messages = build_review_messages(
        code="SELECT * FROM users;",
        goal="performance",
        context={"language": "sql"},
        retrieved_context=[
            {"content": "review_snippet", "source": "review_doc.md", "offset": 5},
        ],
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "code reviewer" in messages[0]["content"].lower()
    user_content = messages[1]["content"]
    assert "Review goal: performance" in user_content
    assert "Code to review" in user_content
    assert "SELECT * FROM users;" in user_content
    assert "Language: sql" in user_content
    assert "Relevant knowledge snippets:" in user_content
    assert "review_snippet" in user_content


def test_build_optimize_messages_defaults_objective_and_includes_rag() -> None:
    messages = build_optimize_messages(
        code="SELECT * FROM big_table;",
        objective=None,
        context=None,
        retrieved_context=[
            {"content": "opt_snippet", "source": "opt_doc.md", "offset": 0},
        ],
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "optimization assistant" in messages[0]["content"].lower()
    user_content = messages[1]["content"]
    # default objective should be "performance"
    assert "Optimization objective: performance" in user_content
    assert "SELECT * FROM big_table;" in user_content
    assert "Relevant knowledge snippets:" in user_content
    assert "opt_snippet" in user_content