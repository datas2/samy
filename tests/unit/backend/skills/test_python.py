from backend.skills.python.code import PythonCodeGenerationSkill
from backend.skills.python.docstring import PythonDocstringSkill
from backend.skills.python.fastapi import PythonFastAPISkill
from backend.skills.python.refactor import PythonRefactorSkill
from backend.skills.python.review import PythonReviewSkill
from backend.skills.python.tests import PythonTestsSkill


def test_python_code_generation_skill_generate_code_basic(monkeypatch):
    # mock llm_client.chat para não chamar LLM de verdade
    def fake_chat(messages):
        return "def soma(a, b):\n    return a + b\n"

    skill = PythonCodeGenerationSkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.generate_code(
        description="Função que soma dois números.",
        context={"framework": "none"},
    )

    assert isinstance(result, str)
    assert "def" in result
    assert "soma" in result


def test_python_docstring_skill_generate_docstring_basic(monkeypatch):
    def fake_chat(messages):
        return "Função que soma dois números.\n\nArgs:\n  a: Primeiro número.\n  b: Segundo número.\n\nReturns:\n  A soma de a e b."

    skill = PythonDocstringSkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.generate_docstring(
        description="def soma(a, b):\n    return a + b",
        context={"style": "google"},
    )

    assert isinstance(result, str)
    assert "Função que soma dois números" in result


def test_python_fastapi_skill_generate_endpoint_basic(monkeypatch):
    def fake_chat(messages):
        return (
            "from fastapi import APIRouter\n\n"
            "router = APIRouter()\n\n"
            "@router.get('/health')\n"
            "async def health():\n"
            "    return {'status': 'ok'}\n"
        )

    skill = PythonFastAPISkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.generate_endpoint(
        description="Endpoint GET /health que retorna status=ok.",
        context={"path": "/health", "method": "GET"},
    )

    assert isinstance(result, str)
    assert "router.get" in result
    assert "/health" in result


def test_python_fastapi_skill_review_fastapi_code_basic(monkeypatch):
    def fake_chat(messages):
        return "O endpoint está correto, mas você pode adicionar tipagem explícita no retorno."

    skill = PythonFastAPISkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.review_fastapi_code(
        description="from fastapi import FastAPI\napp = FastAPI()",
        context={"notes": "API simples"},
    )

    assert isinstance(result, str)
    assert "endpoint" in result.lower() or len(result) > 0


def test_python_refactor_skill_refactor_basic(monkeypatch):
    def fake_chat(messages):
        return "def foo(x: int) -> int:\n    return x + 1\n"

    skill = PythonRefactorSkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    code = "def foo(x):\n    return x+1"
    result = skill.refactor(
        description=code,
        context={"framework": "none"},
    )

    assert isinstance(result, str)
    assert "def foo" in result
    assert "+ 1" in result or "x + 1" in result


def test_python_review_skill_review_basic(monkeypatch):
    def fake_chat(messages):
        return "O código poderia usar f-strings e adicionar tipagem."

    skill = PythonReviewSkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.review(
        description="def hello(name):\n    return 'Hello, ' + name",
        context={"framework": "none"},
    )

    assert isinstance(result, str)
    assert "f-string" in result.lower() or len(result) > 0


def test_python_tests_skill_generate_tests_basic(monkeypatch):
    def fake_chat(messages):
        return (
            "import pytest\n\n"
            "from mymodule import soma\n\n"
            "def test_soma():\n"
            "    assert soma(1, 2) == 3\n"
        )

    skill = PythonTestsSkill(llm_client=None, telemetry=None)
    monkeypatch.setattr(skill._llm_client, "chat", fake_chat)

    result = skill.generate_tests(
        description="def soma(a, b):\n    return a + b",
        context={"framework": "pytest"},
    )

    assert isinstance(result, str)
    assert "test_soma" in result