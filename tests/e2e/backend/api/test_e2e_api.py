from __future__ import annotations

import subprocess
import sys
import time
from contextlib import suppress

import httpx


def _start_server() -> subprocess.Popen:
    """
    Start the FastAPI server using uvicorn and return the Popen handle.

    Assumes that dependencies have already been installed (e.g., via `uv sync`)
    and that `backend.main:app` is the ASGI application.
    """
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _wait_for_server(proc: subprocess.Popen, timeout: float = 10.0) -> None:
    start = time.time()
    while time.time() - start < timeout and proc.poll() is None:
        with suppress(Exception):
            r = httpx.get("http://127.0.0.1:8000/health", timeout=1.0)
            if r.status_code == 200:
                return
        time.sleep(0.5)

    # If we reach here, either timeout or process died
    stderr = None
    with suppress(Exception):
        stderr = proc.stderr.read().decode("utf-8") if proc.stderr else None
    raise RuntimeError(
        f"Server did not become ready in time. "
        f"Exit code: {proc.poll()}, stderr: {stderr}"
    )

def test_e2e_health_and_explain_endpoint() -> None:
    proc = _start_server()
    try:
        _wait_for_server(proc)

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
    finally:
        with suppress(Exception):
            proc.terminate()
        with suppress(Exception):
            proc.kill()