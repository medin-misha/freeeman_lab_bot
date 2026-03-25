FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.7.22 /uv /uvx /bin/

COPY pyproject.toml README.md ./
RUN uv sync --no-dev --no-install-project

COPY . .

CMD ["uv", "run", "python", "main.py"]
