from backend.skills.sql.explain import SQLExplainSkill
from backend.skills.sql.optimize import SQLOptimizeSkill
from backend.skills.sql.review import SQLReviewSkill


def test_sql_explain_skill_explain_basic():
    skill = SQLExplainSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.explain_sql(
        description="SELECT * FROM orders WHERE amount > 100;",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_sql_optimize_skill_optimize_basic():
    skill = SQLOptimizeSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.optimize_sql(
        description="SELECT * FROM orders WHERE amount > 100 ORDER BY created_at DESC;",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_sql_review_skill_review_basic():
    skill = SQLReviewSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.review_sql(
        description="SELECT * FROM orders WHERE status = 'PENDING';",
        context={"db": "postgres"},
    )

    assert isinstance(result, str)
    assert len(result) > 0