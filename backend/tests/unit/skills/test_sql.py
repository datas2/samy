from backend.skills.sql.explain import SQLExplainSkill
from backend.skills.sql.optimize import SQLOptimizeSkill
from backend.skills.sql.review import SQLReviewSkill
from backend.skills.sql.code import SQLCodeGenerationSkill


def test_sql_explain_skill_explain_basic():
    skill = SQLExplainSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.explain(
        description="SELECT * FROM orders WHERE amount > 100;",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_sql_optimize_skill_optimize_basic():
    skill = SQLOptimizeSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize(
        description="SELECT * FROM orders WHERE amount > 100 ORDER BY created_at DESC;",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_sql_review_skill_review_basic():
    skill = SQLReviewSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review(
        description="SELECT * FROM orders WHERE status = 'PENDING';",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_sql_code_generation_skill_generate_sql_basic(monkeypatch):
    def fake_chat(messages):
        return "SELECT id, name FROM customers WHERE active = true;"

    skill = SQLCodeGenerationSkill(llm_client=None, telemetry=None, retriever=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.generate_sql(
        description="Liste todos os clientes ativos com id e nome.",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert "SELECT" in result.upper()