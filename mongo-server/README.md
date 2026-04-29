# mongo-server

Safe general MongoDB CRUD operations with strict policy enforcement.  
Agent can pass `database` at call time. Supports optional Auto-Embedding vector indexing via `MONGO_VECTOR_SEARCH=true`.

## Features

- Safe CRUD only (insert, find, update, delete) – no destructive operations
- Strict allowlist policy on collections
- Smart config detection: environment variables → workspace `.env` / `mongo.env` / `mongo.yaml` etc.
- Optional `MONGO_VECTOR_SEARCH=true` for Auto-Embedding + semantic vector search
- Agent-friendly: optional `database` parameter on every tool
- Fully async, Pydantic-structured outputs
- GHCR published

## Installation

### Quick Start with MCP (recommended)

Add to your client's `mcp.json`:

```json
{
  "mcpServers": {
    "mongo-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/path/to/your/project:/workspace",
        "-e",
        "MONGO_URI=mongodb://your-host:27017",
        "-e",
        "MONGO_VECTOR_SEARCH=true",
        "ghcr.io/saviornt/MCP-Servers/mongo-server:latest"
      ]
    }
  }
}
```

Replace `/path/to/your/project` with your actual workspace and update the URI as needed.

### Install from Source

```powershell
cd mongo-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Tool Safety

This server enforces a **strict allowlist** of operations and collections for security:

**Allowed Operations:** `insert_one`, `find_one`, `find`, `update_one`, `delete_one`, `list_collections`

**Allowed Collections (by default):** `memories`, `tasks`, `journals`, `logs`, `knowledge` (or any collection prefixed with `custom_`)

Any attempt to run disallowed operations will be rejected with a clear error.

For long-term agent memory (memories/tasks/journals + vector search), use the dedicated **`mongo-memories`** server instead.

## Usage

```powershell
python -m server
```

## Available Tools

All tools are prefixed with `mongo_` for easy grouping in the client UI:

### Core CRUD

- `mongo_get_status_tool(database: str | None = None)`
- `mongo_list_collections_tool(database: str | None = None)`
- `mongo_insert_one_tool(collection: str, document: dict, database: str | None = None)`
- `mongo_find_one_tool(collection: str, query: dict, database: str | None = None)`
- `mongo_find_tool(collection: str, query: dict, limit: int = 50, database: str | None = None)`
- `mongo_update_one_tool(collection: str, query: dict, update: dict, database: str | None = None)`
- `mongo_delete_one_tool(collection: str, query: dict, database: str | None = None)`

### Vector / Auto-Embedding (requires `MONGO_VECTOR_SEARCH=true`)

- `mongo_ensure_vector_index_tool(collection: str = "memories", path: str = "content", model: str = "voyage-4")`
- `mongo_semantic_search_tool(collection: str, query: str, limit: int = 10, path: str = "content")`

### Utilities

- `get_capabilities()`
- `get_version()`

## Configuration Options

| Variable                | Description                              | Default                     |
|-------------------------|------------------------------------------|-----------------------------|
| `MONGO_URI`             | MongoDB connection string                | `mongodb://localhost:27017` |
| `MONGO_DATABASE`        | Default database name                    | `default_db`                |
| `MONGO_AGENT_NAME`      | Auto-creates `agent_<name>` database     | (none)                      |
| `MONGO_VECTOR_SEARCH`   | Enable Auto-Embedding vector search      | `false`                     |

## License

Apache 2.0
