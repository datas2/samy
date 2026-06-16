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
	uv run pytest tests/