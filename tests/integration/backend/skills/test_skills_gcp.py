import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_gcp_bigquery_optimize_endpoint_smoke():
    payload = {
        "description": "Consulta BigQuery lenta que faz join de 3 tabelas de 1TB.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/bigquery/optimize", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_cloudrun_optimize_endpoint_smoke():
    payload = {
        "description": "Serviço HTTP com picos de tráfego imprevisíveis.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/cloudrun/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_cloudsql_optimize_endpoint_smoke():
    payload = {
        "description": "Instância Cloud SQL com problemas de conexão e latência.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/cloudsql/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_composer_optimize_endpoint_smoke():
    payload = {
        "description": "DAGs com falhas frequentes e longos tempos de execução.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/composer/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_cost_analysis_optimize_endpoint_smoke():
    payload = {
        "description": "Conta com gastos altos em BigQuery, Dataflow e GCS.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/cost_analysis/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_dataflow_optimize_endpoint_smoke():
    payload = {
        "description": "Pipeline em Dataflow com alto custo e janelas muito grandes.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/dataflow/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_datastream_optimize_endpoint_smoke():
    payload = {
        "description": "Replicação contínua de base transacional para BigQuery usando Datastream.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/datastream/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_iam_optimize_endpoint_smoke():
    payload = {
        "description": "Projeto com permissões excessivas concedidas a service accounts.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/iam/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_monitoring_optimize_endpoint_smoke():
    payload = {
        "description": "Alertas com muito ruído e dashboards pouco úteis.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/monitoring/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_observability_optimize_endpoint_smoke():
    payload = {
        "description": "Stack de observabilidade com muitos logs e custos altos.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/observability/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_pubsub_optimize_endpoint_smoke():
    payload = {
        "description": "Sistema event-driven com muitos consumidores lentos e fila acumulando.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/pubsub/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_gcp_security_optimize_endpoint_smoke():
    payload = {
        "description": "Ambiente com múltiplos projetos, VPC peering e necessidade de hardening.",
        "context": {"project": "meu-projeto"},
    }

    response = client.post("/skills/gcp/security/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)