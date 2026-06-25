from backend.skills.golang.tests import GoTestsSkill
from backend.skills.golang.review import GoReviewSkill
from backend.skills.golang.concurrency import GoConcurrencySkill


def test_go_tests_skill_generate_basic():
    skill = GoTestsSkill(llm_client=None, telemetry=None)

    result = skill.generate(
        description="Função que valida CPF.",
        context={"package": "cpfvalidator"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_go_review_skill_review_basic():
    skill = GoReviewSkill(llm_client=None, telemetry=None)

    result = skill.review(
        description="package main\n\nfunc Add(a, b int) int { return a + b }",
        context={"package": "main"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_go_concurrency_skill_analyze_basic():
    skill = GoConcurrencySkill(llm_client=None, telemetry=None)

    result = skill.analyze_concurrency(
        description="func worker(ch chan int) { go func() { ch <- 1 }(); <-ch }",
        context={"package": "main"},
    )

    assert isinstance(result, str)
    assert len(result) > 0