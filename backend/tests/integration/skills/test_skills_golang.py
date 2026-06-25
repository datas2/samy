import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_go_tests_generate_endpoint_smoke():
    payload = {
        "description": "Função Go que soma dois inteiros.",
        "context": {"framework": "testing"},
    }

    response = client.post("/skills/go/tests/generate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)


@pytest.mark.integration
def test_go_review_review_endpoint_smoke():
    payload = {
        "description": "package main\n\nfunc Add(a, b int) int { return a + b }",
        "context": {"package": "main"},
    }

    response = client.post("/skills/go/review/review", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_go_concurrency_analyze_concurrency_endpoint_smoke():
    payload = {
        "description": "go func() { ch <- 1 }()\n<-ch",
        "context": {"package": "main"},
    }

    response = client.post("/skills/go/concurrency/analyze_concurrency", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)