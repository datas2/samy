from __future__ import annotations

from fastapi.testclient import TestClient

from backend.main import create_app


client = TestClient(create_app())


def test_full_flow_explain_review_optimize() -> None:
    # 1) Health
    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json() == {"status": "ok"}

    # 2) Explain
    explain_payload = {
        "prompt": "Explain this SQL query",
        "code": "SELECT * FROM users;",
        "context": {"language": "sql"},
    }
    explain_resp = client.post("/explain", json=explain_payload)
    assert explain_resp.status_code == 200
    assert "explanation" in explain_resp.json()

    # 3) Review
    review_payload = {
        "code": "SELECT * FROM users;",
        "goal": "performance",
    }
    review_resp = client.post("/review", json=review_payload)
    assert review_resp.status_code == 200
    review_body = review_resp.json()
    assert isinstance(review_body["issues"], list)

    # 4) Optimize
    optimize_payload = {
        "code": "SELECT * FROM users;",
        "objective": "performance",
    }
    optimize_resp = client.post("/optimize", json=optimize_payload)
    assert optimize_resp.status_code == 200
    optimize_body = optimize_resp.json()
    assert isinstance(optimize_body["suggestions"], list)