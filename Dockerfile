# syntax=docker/dockerfile:1.6
FROM python:3.13-slim AS builder

# OCI Labels for image metadata
LABEL org.opencontainers.image.source="https://github.com/Brevex/PaintMatch-AI"
LABEL org.opencontainers.image.title="PaintMatch-AI"
LABEL org.opencontainers.image.description="AI-powered paint color matching system"
LABEL org.opencontainers.image.version="1.0.0"
LABEL maintainer="Brevex"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.13-slim

# Install runtime dependencies and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

# Copy application files
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser Base_de_Dados_de_Tintas_Suvinil.csv ./
COPY pyproject.toml uv.lock ./

# Copy and set up entrypoint
COPY --chown=appuser:appuser scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create required directories with proper ownership
RUN mkdir -p /app/app/static/images && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Healthcheck for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
