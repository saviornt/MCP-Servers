# mongo-memories-server

Dedicated long-term memory server for agents. Stores memories, tasks, journals, logs, and knowledge with built-in Auto-Embedding vector search (enabled by default).

## Features

- Isolated memory-only server (cannot touch general/production databases)
- Dedicated collections: `memories`, `tasks`, `journals`, `logs`
- Automatic vector indexing using MongoDB Auto-Embedding (Voyage AI models)
- Semantic (vector) search support out of the box
- Smart config detection: environment variables → workspace `.env` / `mongo.env` / `mongo.yaml` etc.
- Fully async with structured Pydantic outputs
- GHCR published

## Installation

### Quick Start with MCP (recommended)

Add to your client's `mcp.json`:

```json
{
  "mcpServers": {
    "mongo-memories": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/path/to/your/project:/workspace",
        "-e",
        "MONGO_URI=mongodb://your-host:27017",
        "ghcr.io/saviornt/MCP-Servers/mongo-memories:latest"
      ]
    }
  }
}
```

Replace `/path/to/your/project` with your actual workspace and update the URI as needed.

### Install from Source

```powershell
cd mongo-memories
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Tool Safety

This server is **dedicated to agent long-term memory only**. It is intentionally isolated from general database operations (use the separate `mongo-server` for general CRUD).

**Allowed Collections:** `memories`, `tasks`, `journals`, `logs`

**Vector Search:** Enabled by default (`MONGO_VECTOR_SEARCH=true`). You can disable it with an environment variable if desired.

All operations are safe and restricted to memory-related actions.

## Usage

```powershell
python -m server
```

## Available Tools

All tools are prefixed with `memories_` for clear grouping in the MCP client UI:

### Memory Tools

- `memories_store_memory_tool(content: str, memory_type: str = "memory", metadata: dict | None = None)`
- `memories_get_memory_tool(memory_id: str)`
- `memories_search_memories_tool(query: str, limit: int = 20)`
- `memories_delete_memory_tool(memory_id: str)`

### Task Tools

- `memories_store_task_tool(title: str, description: str, status: str = "pending")`
- `memories_list_tasks_tool(status: str | None = None)`

### Journal Tools

- `memories_store_journal_entry_tool(entry: str)`

### Vector / Auto-Embedding Tools

- `memories_ensure_auto_embed_index_tool(collection: str = "memories", path: str = "content", model: str = "voyage-4")`
- `memories_semantic_search_tool(collection: str = "memories", query: str, limit: int = 10, path: str = "content")`

### Utilities

- `get_capabilities()`
- `get_version()`

## Configuration Options

| Variable                | Description                              | Default                     |
|-------------------------|------------------------------------------|-----------------------------|
| `MONGO_URI`             | MongoDB connection string                | `mongodb://localhost:27017` |
| `MONGO_DATABASE`        | Database name for memories               | `agent_memory`              |
| `MONGO_AGENT_NAME`      | Auto-creates database `agent_<name>`     | (none)                      |
| `MONGO_VECTOR_SEARCH`   | Enable Auto-Embedding vector search      | `true`                      |

## License

Apache 2.0
