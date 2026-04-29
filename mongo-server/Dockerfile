# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

LABEL io.modelcontextprotocol.server.name="io.github.saviornt/mongo-server" \
      io.modelcontextprotocol.server.description="Safe general MongoDB CRUD operations (strict policy - no destructive commands)." \
      io.modelcontextprotocol.server.version="1.0.0" \
      io.modelcontextprotocol.server.repository.url="https://github.com/saviornt/MCP-Servers/mongo-server"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

CMD ["python", "-m", "server"]