#FROM docker.io/python:3.11-slim
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app
COPY . ./
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 5000
CMD ["gunicorn", "--log-level", "debug", "--reload", "-b", "0.0.0.0:5000", "dep:app"]
