# uv - https://uv.io/
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

run-tests:
	uv sync
	@if [ -d tests/unit ]; then uv run pytest tests/unit; else echo "No unit tests found in tests/unit, skipping."; fi
	@if [ -d tests/integration ]; then uv run pytest tests/integration; else echo "No integration tests found in tests/integration, skipping."; fi
	@if [ -d tests/e2e ]; then uv run pytest tests/e2e; else echo "No e2e tests found in tests/e2e, skipping."; fi

# ollama
# Default model used by Samy via OLLAMA_MODEL (can be overridden).
OLLAMA_MODEL ?= qwen3.1:latest
run-ollama:
	ollama run $(OLLAMA_MODEL)

# docker
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