# Base Image
# ------------------------------------------------
# Using official lightweight Python image
# "-slim" reduces image size by removing unnecessary OS tools
FROM python:3.11-slim


# Environment Configuration
# ------------------------------------------------
# Prevents Python from creating .pyc files
# Keeps container filesystem clean and avoids unnecessary writes
ENV PYTHONDONTWRITEBYTECODE=1
# Forces Python to print logs immediately
# This is important so Docker logs show output in real-time
ENV PYTHONUNBUFFERED=1


# Install uv
# ------------------------------------------------
# Copy uv binary from official uv image
# This avoids installing curl, cargo, or build tools
# Cleaner, faster, and more production-safe approach
COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /usr/local/bin/uv


# Create Non-Root User (Security Best Practice)
# ------------------------------------------------
# Containers run as root by default
# Running applications as root is a security risk
# So we create a normal user to follow best practices
RUN useradd -m appuser


# Set Working Directory
# ------------------------------------------------
# Sets the working directory inside container
# All future commands will run inside /app
WORKDIR /app


# Copy Dependency Files First (Docker Cache Optimization)
# ------------------------------------------------
# Copy only dependency-related files first
# This allows Docker to cache dependency installation
# If application code changes but dependencies don't,
# Docker will reuse this layer and build faster
COPY pyproject.toml uv.lock README.md ./
# Copy src folder separately because project uses src layout
# It is required so that uv can properly install the packages
COPY src ./src


# Install production dependencies only
# ------------------------------------------------
# --frozen ensures exact versions from uv.lock are used
# --no-dev excludes development dependencies from pyproject.toml file
# uv will automatically create and manage .venv
RUN uv sync --frozen --no-dev


# Copy Application Code
# ------------------------------------------------
# Copy remaining necessary project files
# Done after dependency installation to preserve Docker caching
COPY api ./api
COPY config ./config


# Change Ownership to Non-Root User
# ------------------------------------------------
# Ensures appuser owns application files
# Prevents permission errors at runtime
RUN chown -R appuser:appuser /app


# Using the Non-Root User
# ------------------------------------------------
# From this point forward, container runs as appuser
# Improves security posture of the container
USER appuser


# Expose Application Port
# ------------------------------------------------
# Documents that the container listens on port 8000
# Required for proper port mapping in Docker
EXPOSE 8000


# Start FastAPI Application
# ------------------------------------------------
# Use uv run to:
# - Automatically activate .venv
# - Use correct Python interpreter
# - Respect uv.lock dependencies
#
# ${PORT:-8000} means:
# - Use environment variable PORT if provided
# - Otherwise default to 8000
#
# Using "sh -c" allows shell variable expansion
CMD ["sh", "-c", "uv run uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]