install-uv:
	pip install uv

uv-init:
	uv init
	uv sync

uv-add-dependencies:
	uv pip install -r pyproject.toml