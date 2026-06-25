import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_analytics_dashboard_design_endpoint_smoke():
    payload = {
        "description": "Crie um dashboard de vendas com métricas de receita e ticket médio.",
        "context": {"tool": "powerbi"},
    }

    response = client.post("/skills/analytics/dashboard/design", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


@pytest.mark.integration
def test_analytics_kpi_design_endpoint_smoke():
    payload = {
        "description": "Defina KPIs de receita recorrente mensal (MRR) e churn.",
        "context": {"domain": "saas"},
    }

    response = client.post("/skills/analytics/kpi/design", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


@pytest.mark.integration
def test_analytics_metrics_design_endpoint_smoke():
    payload = {
        "description": "Defina métricas de funil de conversão (visitas, leads, oportunidades, vendas).",
        "context": {"domain": "marketing"},
    }

    response = client.post("/skills/analytics/metrics/design", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0