from backend.skills.analytics.dashboard import DashboardSkill
from backend.skills.analytics.kpi import KpiSkill
from backend.skills.analytics.metrics import MetricsSkill


def test_dashboard_skill_design_signature_and_basic_behavior():
    skill = DashboardSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.design(
        description="Dashboard de churn de clientes.",
        context={"tool": "looker"},
    )

    assert isinstance(result, str)
    assert "churn" in result.lower() or len(result) > 0


def test_kpi_skill_design_basic_behavior():
    skill = KpiSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.design(
        description="Definir KPIs de NPS, churn e lifetime value.",
        context={"domain": "customer_success"},
    )

    assert isinstance(result, str)
    assert len(result) > 0


def test_metrics_skill_design_basic_behavior():
    skill = MetricsSkill(llm_client=None, telemetry=None, retriever=None)

    result = skill.design(
        description="Definir métricas de engajamento (DAU, WAU, MAU).",
        context={"domain": "produto"},
    )

    assert isinstance(result, str)
    assert len(result) > 0