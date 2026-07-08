# 1. High-Level Goals
Samy’s Python architecture guidance should focus on:
- **Separation of concerns**: domain logic, application services, infrastructure, interfaces.
- **Modularity and testability**: small, composable components, easy to test in isolation.
- **Explicit dependencies**: dependency injection instead of globals.
- **Consistency**: predictable project layout and patterns.
- **Observability**: telemetry, logging, and metrics integrated from the start.

---
# 2. Recommended Project Structure
Use a layered, modular structure for Python backends:

```text
project/
  backend/
    api/                # HTTP, CLI, gRPC, etc. – I/O layer
    skills/             # domain-specific skills (Samy-style)
    services/           # application services, orchestration
    core/               # shared utilities (logging, config)
    database/           # models, repositories, DB setup
    rag/                # retrievers, ingestion, embeddings
    llm/                # LLM clients, prompt builders
    schemas/            # used to store data validation, serialization, and structure definitions
    services/           # isolates business logic away from the routing, database, and presentation layers
    tests/              # unit/integration tests
```

Guidelines:
- **api**: only request/response handling, routing, validation; no business logic.
- **skills**: encapsulate domain-specific LLM/RAG behavior (SQL, Python, GCP, etc.).
- **services**: coordinate skills, DB, external APIs; implement use cases.
- **database**: ORM models and repositories; no business rules.
- **core**: logging, config, error types, cross-cutting concerns.
- **llm** / **rag**: separate LLM and retrieval concerns from business logic.

Samy itself follows this pattern; use it as a template for other Python projects.

---
# 3. Layered Architecture
Think in terms of layers:
- **Domain & Skills Layer**
    - Core skills and business logic.
    - Independent from frameworks (FastAPI, SQLAlchemy, etc.) whenever possible.
- **Application Services Layer**
    - Orchestrates use cases:
        - “Explain this SQL query”
        - “Refactor this Python function”
        - “Generate tests for this module”
    - Uses skills, repositories, and external clients.
- **Infrastructure Layer**
    - DB connections, repositories, LLM clients, HTTP clients.
- **Interface Layer**
    - HTTP endpoints (FastAPI), CLI, background jobs, MCP servers.

Principles:
- Domain/skills should not import from API or infrastructure directly.
-   Services depend on domain/skills and repositories, but not on HTTP specifics.
-   API layer depends on services and domain/skills, never the other way around.

---
# 4. Dependency Injection & Configuration
## 4.1 Explicit Dependencies
Avoid hidden global dependencies; inject them:

```python
class TelemetryService:
    def __init__(self, logger: Logger, repository: TelemetryRepository):
        self._logger = logger
        self._repository = repository
```

Services & skills should accept dependencies via constructors or factories rather than importing singletons.

## 4.2 Configuration
Use environment-based configuration with a small config module:

```python
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    ollama_base_url: str
    ollama_model: str = "qwen2.5-coder:3b"

    class Config:
        env_file = ".env"


settings = Settings()
```

Pass `settings` (or its values) into DB, LLM clients, etc. Avoid reading environment variables deep inside business logic.

---
# 5. Error Handling & Domain Errors
Define clear error types:
- Domain errors (e.g., `InvalidQueryError`, `RefactorError`).
- Infrastructure errors (DB, network, LLM timeouts).

Patterns:
- In domain/skills: raise domain-specific exceptions with meaningful messages.
- In services: catch domain errors to compose responses or logs.
- In API: map exceptions to HTTP responses (`HTTPException` with proper status and detail).

Example:
```python
class InvalidSqlError(Exception):
    """Raised when SQL is syntactically invalid or unsupported."""


def explain_sql(query: str) -> str:
    if not query.strip():
        raise InvalidSqlError("Query is empty")
    ...
```

In FastAPI:
```python
from fastapi import HTTPException

try:
    explanation = sql_explain_service.explain(payload.description)
except InvalidSqlError as exc:
    raise HTTPException(status_code=400, detail=str(exc))
```

---
# 6. Testing Strategy (Architecture-Level)
Align tests with architecture:
- **Unit tests** for domain logic, skills, and services:
    - Use dummy repositories and clients.
    - Avoid real DB/LLM calls.
- **Integration tests** for API, DB, and selected end-to-end flows.
- **Contract tests** for external APIs if needed.

Guidelines:
- Test domain/skills without FastAPI or SQLAlchemy.
- Test API endpoints using `TestClient` and real wiring.
- Ensure that each layer has dedicated tests.

Example:
- `tests/unit/backend/skills/test_python_refactor.py` – tests PythonRefactorSkill.
- `tests/unit/backend/services/test_sql_explain_service.py` – tests the orchestration.
- `tests/integration/backend/api/test_skills_sql.py` – tests HTTP endpoints.

---
# 7. Observability & Telemetry
Architecture should include:
- Logging
- Telemetry events (Samy’s `TelemetryService`)
- Optional metrics (OpenTelemetry, Prometheus)

Guidelines:
- Emit telemetry from services, not from API layer only.
- Keep telemetry calls lightweight (buffered or best-effort).
- Use structured payloads: event_type, schema_version, context.

Example pattern:
```python
telemetry.record_event(
    event_type="sql_explain",
    payload={
        "query": query,
        "db": context.get("db"),
        "knowledge_hits": len(knowledge_hits),
        "prompt_tokens_estimate": prompt_tokens,
        "response_tokens_estimate": response_tokens,
    },
)
```

Telemetry is part of the architecture; design it so you can monitor behavior without modifying core logic heavily.

---
# 8. RAG & LLM Integration Patterns
When using RAG and LLM in architecture:
- Keep **retriever** and **LLM client** separate from business logic.
- Use helper functions or base classes (`AnalyticsSkillBase`, `DbaSkillBase`, etc.) for repeated patterns.

Patterns:
- Build prompts in a dedicated module (`llm/prompts.py`).
- Use a retriever in skills/services, not in API.
- Record telemetry for RAG (number of hits, sources) and LLM (tokens, errors).

Example:
```python
knowledge_hits = retriever.retrieve(query=query_text, k=5)
messages = build_explain_messages(query=query, context=context, retrieved_context=knowledge_hits)
answer = llm_client.chat(messages)
```

Design LLM calls as pure functions of inputs, to make them easier to test with fake clients.

---
# 9. Modularity & Extensibility
Architecture should make it easy to:
- Add new skills (new domains or operations).
- Plug in new LLMs or retrievers.
- Swap DBs (e.g., SQLite → Postgres) with minimal changes.

Guidelines:
- Use registries (`SkillRegistry`) to map names to classes.
- Keep skills small and independent.
- Make dependency injection the default.

Example:
```python
skill_registry.register("sql", "explain", SQLExplainSkill)
skill_registry.register("python", "refactor", PythonRefactorSkill)
```

The registry is an extension point; architecture should favor such extension points over hard-coded wiring.

---
# 10. Playbook Summary for Samy
When Samy’s Python skills advise on architecture or refactor a project structure, they should:

- Encourage a layered, modular layout:
    - api, skills, services, core, database, llm, rag, tests.
- Separate domain logic from infrastructure and interfaces.
- Promote explicit dependency injection and environment-based configuration.
- Define clear domain and infrastructure error types.
- Align tests with architecture layers (unit vs integration).
- Integrate logging and telemetry as first-class concerns.
- Encapsulate RAG and LLM logic in dedicated components.
- Use registries and factories to enable extension.
- Avoid God objects, global state, and tightly coupled modules.
- Aim for architectures that are:
    - Understandable
    - Testable
    - Observable
    - Extendable

---
# 11. External References & Further Reading

These resources provide deeper background and examples that align with the
architecture guidelines used by Samy’s Python skills.

## 11.1 Python Architecture & Design Patterns

- **“Architecture Patterns with Python” (Cosmic Python)**  
  https://www.cosmicpython.com/  
  Focuses on domain-driven design, layered architecture, and separation of
  concerns in Python applications. Highly relevant for designing services,
  repositories, and domain models.

- **Python Design Patterns on Refactoring.Guru**  
  https://refactoring.guru/design-patterns/python  
  Catalog of common patterns (Strategy, Adapter, Factory, etc.) with Python
  examples. Useful when choosing patterns for skills, services, and clients.

## 11.2 Web Backends & FastAPI

- **FastAPI Official Documentation**  
  https://fastapi.tiangolo.com/  
  Includes recommended project structures, dependency injection patterns,
  and testing strategies for FastAPI-based backends.

- **FastAPI “Big Applications” Pattern**  
  https://fastapi.tiangolo.com/tutorial/bigger-applications/  
  Example of organizing routers, dependencies, and settings in larger apps.

## 11.3 Clean Architecture & Hexagonal Architecture

- **Clean Architecture (Uncle Bob) – Concepts**  
  https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html  
  Explains the idea of keeping business rules independent from frameworks,
  mirroring the layers used by Samy (domain, application, infrastructure, interface).

- **Hexagonal Architecture (Ports and Adapters)**  
  https://alistair.cockburn.us/hexagonal-architecture/  
  Useful for thinking about skills, services, and external systems (DB, LLM, RAG)
  as ports/adapters.

## 11.4 RAG & LLM System Design

- **Retrieval-Augmented Generation (RAG) – LangChain Docs**  
  https://python.langchain.com/docs/use_cases/question_answering/  
  Shows how to structure retrievers, indexes, and prompts. Relevant for Samy’s
  `rag/` and `llm/` modules and skill bases (e.g., AnalyticsSkillBase).

- **OpenAI “Patterns for building LLM applications”**  
  https://platform.openai.com/docs/guides  
  General guidance on prompt design, tool usage, and multi-step workflows.

## 11.5 Observability & Telemetry

- **OpenTelemetry – Semantic Conventions**  
  https://opentelemetry.io/docs/specs/semconv/  
  Provides standard names and structures for traces, metrics, and logs. Useful
  when designing telemetry payloads and event types.

- **Prometheus & Grafana Docs**  
  https://prometheus.io/docs/introduction/overview/  
  Useful if you plan to expose metrics from Python services and visualize them.

---

When Samy’s architecture skills generate or review designs, they should prefer
patterns and structures that are consistent with these references, while still
adapting to the specifics of the project (size, team, domain).
