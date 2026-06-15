install-uv:
	pip install uv

init-uv:
	uv init
	uv sync

add-dependencies-uv:
	uv sync

run-uv:
	uv run backend/main.py

build-uv:
	uv build