install-uv:
	pip install uv

init-uv:
	uv init
	uv sync

add-dependencies-uv:
	uv pip install -r pyproject.toml

run-uv:
	uv run backend/main.py

build-uv:
	uv build