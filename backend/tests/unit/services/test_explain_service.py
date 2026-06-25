from __future__ import annotations

from typing import Any, Dict, List, Optional

from backend.schemas.api import ExplainRequest, CodeContext
from backend.services.explain_service import ExplainService


class DummyRetriever:
    def __init__(self) -> None:
        self.last_query: Optional[str] = None
        self.last_k: Optional[int] = None

    def retrieve(self, *, query: str, k: int = 5) -> List[Dict[str, Any]]:
        self.last_query = query
        self.last_k = k
        return [
            {"content": "rag snippet", "source": "doc.md", "offset": 0},
        ]


class DummyLLMClient:
    def __init__(self) -> None:
        self.last_messages: Optional[List[Dict[str, str]]] = None

    def chat(self, messages: List[Dict[str, str]]) -> str:
        self.last_messages = messages
        return "Dummy explanation"


class DummyTelemetry:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    @staticmethod
    def estimate_tokens_from_text(text: str) -> int:
        # Simple deterministic function for tests
        return len(text.split())

    def record_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        self.events.append({"event_type": event_type, "payload": payload})


def test_explain_service_generates_explanation_and_telemetry() -> None:
    retriever = DummyRetriever()
    llm_client = DummyLLMClient()
    telemetry = DummyTelemetry()

    service = ExplainService(
        retriever=retriever,
        llm_client=llm_client,
        telemetry=telemetry,
    )

    request = ExplainRequest(
        prompt="Explain this code",
        code="print('hello')",
        context=CodeContext(language="python"),
    )

    response = service.explain(request)

    assert response.explanation == "Dummy explanation"
    assert retriever.last_query is not None
    assert "Explain this code" in retriever.last_query
    assert "print('hello')" in retriever.last_query

    assert llm_client.last_messages is not None
    # Telemetry
    assert len(telemetry.events) == 1
    event = telemetry.events[0]
    assert event["event_type"] == "explain"
    payload = event["payload"]
    assert payload["prompt"] == "Explain this code"
    assert payload["has_code"] is True
    assert payload["knowledge_hits"] == 1
    assert "prompt_tokens_estimate" in payload
    assert "response_tokens_estimate" in payload