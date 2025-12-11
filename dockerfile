FROM python:3.13-slim

# Install system dependencies (netcat for health checks)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install dependencies
# --frozen: assert that the lockfile is up-to-date
# --no-install-project: legitimate application code is not yet copied
# We install into the system python or a virtual env.
# Here we use the default venv at .venv and add it to path.
RUN uv sync --frozen --no-install-project --no-dev

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of the application
COPY . .

# Install the project itself (if needed, or just relying on code present)
# Since the app layout is simple, we might not need to install the project as a package.
# But running sync again ensures everything is consistent.
RUN uv sync --frozen --no-dev

EXPOSE 8000

# Copy entrypoint script
COPY scripts/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
