import types

from backend.skills.registry import SkillRegistry
from backend.skills.sql.explain import SQLExplainSkill
from backend.skills.python.refactor import PythonRefactorSkill
from backend.skills.golang.tests import GoTestsSkill
from backend.skills.gcp.bigquery import BigQuerySkill
from backend.skills.dba.indexes import IndexesSkill
from backend.skills.analytics.dashboard import DashboardSkill


def _get_init_kwargs(instance, cls):
    """
    Helper to inspect the internal attributes set by the skill's __init__.
    This assumes the pattern used in current skills (_retriever, _llm_client, _telemetry).
    """
    attrs = {}
    for name in dir(instance):
        if name.startswith("_") and not name.startswith("__"):
            try:
                value = getattr(instance, name)
            except Exception:
                continue
            attrs[name] = value
    return attrs


def test_registry_returns_correct_sql_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("sql", "explain")

    assert isinstance(skill, SQLExplainSkill)


def test_registry_returns_correct_python_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("python", "refactor")

    assert isinstance(skill, PythonRefactorSkill)


def test_registry_returns_correct_go_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("go", "tests")

    assert isinstance(skill, GoTestsSkill)


def test_registry_returns_correct_gcp_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("gcp", "bigquery")

    assert isinstance(skill, BigQuerySkill)


def test_registry_returns_correct_dba_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("dba", "indexes")

    assert isinstance(skill, IndexesSkill)


def test_registry_returns_correct_analytics_skill_type():
    registry = SkillRegistry()

    skill = registry.get_skill("analytics", "dashboard")

    assert isinstance(skill, DashboardSkill)


def test_registry_injects_retriever_for_domains_with_retriever():
    registry = SkillRegistry()

    # domains that should receive retriever: sql, gcp, dba, analytics
    sql_skill = registry.get_skill("sql", "explain")
    gcp_skill = registry.get_skill("gcp", "bigquery")
    dba_skill = registry.get_skill("dba", "indexes")
    analytics_skill = registry.get_skill("analytics", "dashboard")

    # base skills of these domains store retriever in _retriever
    assert getattr(sql_skill, "_retriever", None) is not None
    assert getattr(gcp_skill, "_retriever", None) is not None
    assert getattr(dba_skill, "_retriever", None) is not None
    assert getattr(analytics_skill, "_retriever", None) is not None


def test_registry_does_not_inject_retriever_for_python_and_go():
    registry = SkillRegistry()

    python_skill = registry.get_skill("python", "refactor")
    go_skill = registry.get_skill("go", "tests")

    # these skills do not use retriever; the attribute should not exist
    assert not hasattr(python_skill, "_retriever")
    assert not hasattr(go_skill, "_retriever")


def test_registry_uses_same_llm_and_telemetry_instances_for_all_skills():
    registry = SkillRegistry()

    sql_skill = registry.get_skill("sql", "explain")
    python_skill = registry.get_skill("python", "refactor")
    go_skill = registry.get_skill("go", "tests")

    # in all skills, the LLM client and telemetry should be the same objects
    sql_llm = getattr(sql_skill, "_llm_client", None)
    py_llm = getattr(python_skill, "_llm_client", None)
    go_llm = getattr(go_skill, "_llm_client", None)

    sql_tel = getattr(sql_skill, "_telemetry", None)
    py_tel = getattr(python_skill, "_telemetry", None)
    go_tel = getattr(go_skill, "_telemetry", None)

    assert sql_llm is not None
    assert sql_llm is py_llm is go_llm

    assert sql_tel is not None
    assert sql_tel is py_tel is go_tel


def test_registry_raises_for_unknown_skill():
    registry = SkillRegistry()

    try:
        registry.get_skill("sql", "does_not_exist")
    except ValueError as exc:
        assert "Skill not found" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown skill, but none was raised.")