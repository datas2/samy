from __future__ import annotations

import time
from contextlib import suppress

import httpx
import pytest


def _server_is_running() -> bool:
    """Quick check to see if the backend is already running on /health."""
    with suppress(Exception):
        r = httpx.get("http://127.0.0.1:8000/health", timeout=1.0)
        return r.status_code == 200
    return False


def _wait_for_server(timeout: float = 5.0) -> None:
    """
    Wait until the backend responds on /health or until timeout.

    This helper assumes the server is already running separately
    (e.g., via `make run-uv`) and avoids starting it inside the test.
    """
    start = time.time()
    while time.time() - start < timeout:
        if _server_is_running():
            return
        time.sleep(0.5)
    raise RuntimeError("Server did not become ready in time")


@pytest.mark.skipif(
    not _server_is_running(),
    reason="Backend is not running on http://127.0.0.1:8000; start it with `make run-uv` to run this e2e test.",
)
def test_e2e_health_and_explain_endpoint() -> None:
    """
    End-to-end test that assumes the Samy API server is already running.

    This test does not start the server; it only verifies that the deployed
    instance responds correctly to /health and /explain.
    """
    _wait_for_server()

    # 1) Health
    r_health = httpx.get("http://127.0.0.1:8000/health", timeout=5.0)
    assert r_health.status_code == 200
    assert r_health.json() == {"status": "ok"}

    # 2) Explain
    payload = {
        "prompt": "Explain this code",
        "code": "print('hello world')",
        "context": {"language": "python"},
    }
    r_explain = httpx.post(
        "http://127.0.0.1:8000/explain",
        json=payload,
        timeout=10.0,
    )
    assert r_explain.status_code == 200
    body = r_explain.json()
    assert "explanation" in body