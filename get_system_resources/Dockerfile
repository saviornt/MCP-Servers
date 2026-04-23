# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

LABEL io.modelcontextprotocol.server.name="io.github.davidwadsworth80/get-system-resources" \
      io.modelcontextprotocol.server.description="An MCP server that provides system resource information such as CPU, memory, disk usage, and network statistics." \
      io.modelcontextprotocol.server.version="1.0.0" \
      io.modelcontextprotocol.server.repository.url="https://github.com/davidwadsworth80/get-system-resources"

# Install system dependencies (very minimal for this MCP tool)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire MCP server source
COPY . .

# Install the package in editable mode
RUN pip install -e .

# The MCP server runs via stdio by default
CMD ["python", "-m", "get_system_resources.server"]