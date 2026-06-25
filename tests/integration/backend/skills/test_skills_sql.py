import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_sql_explain_endpoint_smoke():
    payload = {
        "description": "SELECT * FROM users WHERE created_at > '2024-01-01';",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/sql/explain/explain", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_sql_optimize_endpoint_smoke():
    payload = {
        "description": "SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.amount > 100;",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/sql/optimize/optimize", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_sql_review_endpoint_smoke():
    payload = {
        "description": "SELECT * FROM payments WHERE status = 'PENDING' AND created_at < NOW() - INTERVAL '30 days';",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/sql/review/review", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_sql_code_generate_sql_endpoint_smoke():
    payload = {
        "description": "Liste todos os clientes ativos com id e nome.",
        "context": {"db": "postgres"},
    }

    response = client.post("/skills/sql/code/generate_sql", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)