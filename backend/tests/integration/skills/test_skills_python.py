import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@pytest.mark.integration
def test_python_code_generate_endpoint_smoke():
    payload = {
        "description": "Crie uma função que soma dois números e retorna o resultado.",
        "context": {"framework": "none"},
    }

    response = client.post("/skills/python/code/generate_code", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_docstring_generate_endpoint_smoke():
    payload = {
        "description": "def soma(a, b):\n    return a + b",
        "context": {"style": "google"},
    }

    response = client.post("/skills/python/docstring/generate_docstring", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_fastapi_generate_endpoint_smoke():
    payload = {
        "description": "Endpoint GET /health que retorna status=ok.",
        "context": {"path": "/health", "method": "GET"},
    }

    response = client.post("/skills/python/fastapi/generate_endpoint", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_fastapi_review_endpoint_smoke():
    payload = {
        "description": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/health')\nasync def health():\n    return {'status': 'ok'}",
        "context": {"notes": "API pública"},
    }

    response = client.post("/skills/python/fastapi/review_fastapi_code", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_refactor_refactor_endpoint_smoke():
    payload = {
        "description": "def foo(x):\n    return x+1",
        "context": {"framework": "none"},
    }

    response = client.post("/skills/python/refactor/refactor", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_review_review_endpoint_smoke():
    payload = {
        "description": "def soma(a, b):\n    return a +  b",
        "context": {"framework": "none"},
    }

    response = client.post("/skills/python/review/review", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)


@pytest.mark.integration
def test_python_tests_generate_tests_endpoint_smoke():
    payload = {
        "description": "def soma(a, b):\n    return a + b",
        "context": {"framework": "pytest"},
    }

    response = client.post("/skills/python/tests/generate_tests", json=payload)

    assert response.status_code in {200, 400, 501}
    if response.status_code == 200:
        data = response.json()
        assert "result" in data
        assert isinstance(data["result"], str)