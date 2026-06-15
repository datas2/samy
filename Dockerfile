FROM python:3.12-slim

COPY . .

RUN pip install uv

RUN uv sync

CMD ["uv", "run", "uvicorn", "src.samy.main:app", "--host", "0.0.0.0", "--port", "8080"]