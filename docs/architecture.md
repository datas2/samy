# Samy Architecture

Samy is a modular AI Engineering Assistant built around a clear separation of concerns: API layer, service layer, retrieval layer, knowledge layer, and LLM layer. The goal is to keep the system simple enough for individual engineers to operate, while being extensible for future capabilities.

## High-level components

- **API layer (FastAPI)**  
  Exposes HTTP endpoints such as `/health`, `/explain`, `/review`, and `/optimize`.  
  This layer is responsible only for request/response handling and delegates all business logic to services.

- **Service layer**  
  - `ExplainService`: orchestrates retrieval + prompt building + LLM calls for explanations.  
  - `ReviewService`: orchestrates code review flows.  
  - `OptimizeService`: orchestrates optimization suggestions.  
  - `TelemetryService`: records telemetry events (logs + optional SQLite persistence).
  
  Services are pure Python classes that encapsulate application logic and depend on:
  - `OllamaClient` for LLM calls,
  - `KnowledgeRetriever` for RAG,
  - `TelemetryService` for observability.

- **Retrieval layer (RAG)**  
  - `chunker.py`: splits knowledge documents into chunks with metadata.  
  - `vector_store.py`: wraps ChromaDB for storing and querying chunk embeddings.  
  - `ingest.py`: ingests files from `knowledge/` into the vector store.  
  - `retriever.py`: provides a high-level `KnowledgeRetriever` to fetch relevant chunks given a query.

- **Knowledge layer**  
  - `knowledge/`: directory containing documentation, playbooks, and technical notes.  
  - `scripts/import_playbooks.py`: imports external playbooks into `knowledge/playbooks`.  
  - `scripts/sync_knowledge.py`: re-ingests the `knowledge/` directory into the vector store.

- **LLM layer (Ollama)**  
  - `OllamaClient`: thin HTTP client for `/api/chat` and `/api/embeddings`, reading configuration from `OLLAMA_BASE_URL` and `OLLAMA_MODEL`.  
  - Prompts: `build_explain_messages`, `build_review_messages`, `build_optimize_messages` create structured prompts for the LLM.  
  - Models: configured via environment; typical defaults are `qwen2.5-coder:3b` or `codegemma:7b`.

- **Persistence layer (SQLite)**  
  - `backend/database/models.py`: defines ORM models (e.g., `TelemetryEventModel`).  
  - `backend/database/repositories.py`: provides a simple `TelemetryRepository` for saving/querying events.  
  - SQLite is used as a lightweight, file-based store suitable for both local and small-scale deployments.

## Data flow for a typical request

1. The client (e.g. VS Code extension) sends a POST request to `/explain`, `/review` or `/optimize`.
2. The API layer (FastAPI router) calls the corresponding service (`ExplainService`, `ReviewService`, or `OptimizeService`).
3. The service:
   - builds a context dict from the request,
   - calls `KnowledgeRetriever.retrieve(...)` to get relevant knowledge chunks (best-effort; falls back if RAG fails),
   - builds messages via the appropriate prompt function,
   - calls `OllamaClient.chat(...)` to obtain the LLM response (best-effort; falls back with a clear message if the LLM is unavailable or times out).
4. The service computes simple token estimates for prompt and response, and records an event via `TelemetryService`.
5. The service constructs the Pydantic response (`ExplainResponse`, `ReviewResponse`, `OptimizeResponse`) and returns it to the API layer.
6. The API layer serializes the response as JSON for the client.

## Design principles

- **Modularity**: Each concern (API, services, retrieval, LLM, persistence) is isolated in its own module.
- **Best-effort RAG**: Retrieval failures do not crash the request; the system logs `rag_error` and continues with LLM-only responses.
- **Best-effort LLM**: LLM timeouts or connection issues do not cause 500 errors; services log `llm_error` and return a user-friendly fallback.
- **Portability**: The system is designed to run:
  - locally with UV + Ollama,
  - in Docker,
  - in Cloud Run with minimal configuration.
- **Extensibility**: New services, prompts, and knowledge domains can be added without changing the existing API contract.