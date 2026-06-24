# Deployment Guide

Samy can be deployed both locally and in cloud environments. This document focuses on container-based deployments using Docker and Docker Compose, with Ollama as the LLM runtime.

The deployment architecture was intentionally designed to remain simple, allowing individual developers and small teams to operate the platform without requiring complex infrastructure.

## Docker-only deployment (Samy only, no Ollama)

This mode is useful for running the API skeleton, running tests, or integrating with a remote LLM provider in the future.

1. Build the Docker image:

```bash
make build-docker
# or
docker build -t samy:latest .
```

2. Run the container:
```bash
make docker-up
# or
docker run -p 8000:8000 samy:latest
```

3. Test the API:
```bash
curl http://localhost:8000/health
```

In this mode, `/explain`, `/review`, and `/optimize` will use the configured LLM (if available) or fall back to a friendly error message when the LLM is unavailable.

## Docker Compose deployment (Samy + Ollama)
The recommended way to run Samy with a local LLM is via `docker-compose.yml`, which defines two services:
- `ollama`: runs the Ollama server.
- `samy`: runs the FastAPI backend and connects to Ollama.

1. Pull a model in Ollama (inside the container)

```bash
docker-compose up -d ollama
docker exec -it samy-ollama bash
ollama pull qwen2.5-coder:3b
# or any other model you configured via OLLAMA_MODEL
```

2. Start the full stack
```bash
make docker-compose-up
# or
docker-compose up --build
```

By default, the samy service is configured with:
```yaml
environment:
  OLLAMA_BASE_URL: http://ollama:11434
  OLLAMA_MODEL: qwen2.5-coder:3b
```

3. Test the stack

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain this code","code":"print(\"hello\")","context":{"language":"python"}}'
```

If Ollama or the model is not available, Samy will:
- log a `rag_error` when embeddings are not available, and
- log a `llm_error` when the LLM chat call fails or times out,
- while still returning a best-effort response (fallback message) instead of a 500 error.

## Cloud Run deployment (high-level)
Samy can be deployed to Google Cloud Run using the Docker image built from the Dockerfile. The typical flow:

- Build and push the image:
```bash
gcloud builds submit --tag gcr.io/<PROJECT_ID>/samy
```

- Deploy to Cloud Run:
```bash
gcloud run deploy samy \
  --image gcr.io/<PROJECT_ID>/samy \
  --platform managed \
  --region <REGION> \
  --allow-unauthenticated \
  --set-env-vars OLLAMA_BASE_URL=<LLM_URL>,OLLAMA_MODEL=<MODEL_NAME>
```

- Configure Ollama:
    - Option 1: run Ollama in a VM or another managed environment, expose it over HTTPS, and set    `OLLAMA_BASE_URL` accordingly.
    - Option 2: run Ollama in a separate Cloud Run service (requires careful tuning and potentially more resources).
In both cases:
- the `OLLAMA_MODEL` must match a model installed in the Ollama instance;
- latency and cost will depend heavily on model size (3B/7B/13B models are more Cloud Run-friendly than 30B models).

## Database and knowledge management
- Samy uses a local SQLite database (`backend/database/sqlite.db`) for telemetry and other lightweight persistence needs.
- Knowledge is stored as files under `knowledge/` and ingested into a Chroma-based vector store.

For production:
- consider periodic backups using `scripts/backup_db.py`,
- use `scripts/sync_knowledge.py` or `scripts/build_embeddings.py` to refresh the vector store when knowledge changes,
- consider externalizing the database if you need durability beyond the lifecycle of a single container instance.