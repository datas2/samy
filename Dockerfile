FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install uv (Python package/dependency manager)
RUN pip install --upgrade pip && pip install uv

# Copy project files
COPY pyproject.toml README.md ./
COPY backend backend
COPY knowledge knowledge
COPY extension extension

# Install dependencies and project in editable mode
RUN uv sync

# Expose FastAPI default port
EXPOSE 8000

# Default command: run FastAPI with uvicorn
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]