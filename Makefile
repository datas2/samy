# ---------------------------------------------------------------------------
# UV / local development
# ---------------------------------------------------------------------------

install-uv:
	pip install uv

init-uv:
	uv init
	uv sync

add-dependencies-uv:
	uv sync

run-uv:
	uv run uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

build-uv:
	uv build

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

run-tests:
	uv sync
	@if [ -d tests/unit ]; then uv run pytest tests/unit; else echo "No unit tests found in tests/unit, skipping."; fi
	@if [ -d tests/integration ]; then uv run pytest tests/integration; else echo "No integration tests found in tests/integration, skipping."; fi
	@if [ -d tests/e2e ]; then uv run pytest tests/e2e; else echo "No e2e tests found in tests/e2e, skipping."; fi

# ---------------------------------------------------------------------------
# RAG ingestion
# ---------------------------------------------------------------------------

ingest-knowledge:
	uv run python -c "from backend.rag.ingest import ingest_knowledge_directory; ingest_knowledge_directory('knowledge')"

# ---------------------------------------------------------------------------
# Ollama (local)
# ---------------------------------------------------------------------------

# Default model used by Samy via OLLAMA_MODEL (can be overridden).
# Certify that this model exists in your Ollama (use `ollama list`).
OLLAMA_MODEL ?= qwen2.5-coder:3b

run-pull-ollama:
	@echo "Pulling model $(OLLAMA_MODEL) from Ollama registry..."
	ollama pull $(OLLAMA_MODEL)

run-ollama:
	@echo "Starting Ollama server (ensure the model $(OLLAMA_MODEL) exists)..."
	@echo "In another terminal, you can test the model with: 'ollama run $(OLLAMA_MODEL)'."
	ollama serve

run-samy-with-ollama:
	@echo "Running Samy with Ollama at http://127.0.0.1:11434 using model $(OLLAMA_MODEL)"
	@export OLLAMA_BASE_URL=http://127.0.0.1:11434; export OLLAMA_MODEL=$(OLLAMA_MODEL); \
	make run-uv

# ---------------------------------------------------------------------------
# Docker (single container, no Ollama)
# ---------------------------------------------------------------------------

build-docker:
	docker build -t samy:latest .

docker-up:
	docker run -p 8000:8000 samy:latest

docker-down:
	@CONTAINER_IDS=$$(docker ps -q --filter ancestor=samy:latest); \
	if [ -n "$$CONTAINER_IDS" ]; then \
		echo "Stopping containers: $$CONTAINER_IDS"; \
		docker stop $$CONTAINER_IDS; \
	else \
		echo "No running containers for image samy:latest"; \
	fi

docker-logs:
	@CONTAINER_IDS=$$(docker ps -q --filter ancestor=samy:latest); \
	if [ -n "$$CONTAINER_IDS" ]; then \
		echo "Tailing logs for container $$CONTAINER_IDS"; \
		docker logs -f $$CONTAINER_IDS; \
	else \
		echo "No running containers for image samy:latest"; \
	fi

docker-clean:
	@CONTAINER_IDS=$$(docker ps -aq --filter ancestor=samy:latest); \
	if [ -n "$$CONTAINER_IDS" ]; then \
		echo "Removing containers: $$CONTAINER_IDS"; \
		docker rm -f $$CONTAINER_IDS; \
	else \
		echo "No containers found for image samy:latest"; \
	fi

docker-all: build-docker docker-up

# ---------------------------------------------------------------------------
# Docker Compose (Samy + Ollama)
# ---------------------------------------------------------------------------

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down

# Helper to open a shell in the Ollama container (for manual pulls)
docker-ollama-shell:
	docker exec -it samy-ollama bash