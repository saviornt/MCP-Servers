# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

LABEL io.modelcontextprotocol.server.name="io.github.saviornt/cargo-server" \
      io.modelcontextprotocol.server.description="An MCP server that provides tools for Cargo (Rust package manager) to create, build, test, and manage Rust projects." \
      io.modelcontextprotocol.server.version="1.0.0" \
      io.modelcontextprotocol.server.repository.url="https://github.com/saviornt/MCP-Servers/cargo-server"

# Install system dependencies + Rust via rustup
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && rm -rf /root/.cargo/registry /root/.cargo/git

# Add Rust to PATH
ENV PATH="/root/.cargo/bin:${PATH}"
ENV RUSTUP_HOME=/root/.cargo
ENV CARGO_HOME=/root/.cargo

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire MCP server source
COPY . .

# Install the package in editable mode
RUN pip install -e .

# The MCP server runs via stdio by default
CMD ["python", "-m", "server"]