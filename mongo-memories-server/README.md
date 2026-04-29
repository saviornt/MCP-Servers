# mongo-memories-server

Dedicated long-term **cognitive memory system** for agents.  
Stores knowledge (RAG), tasks, journal entries, and a rich, evolving **identity/personality profile** with Big Five traits, core values, goals, cognitive style, and self-reflection capabilities. Vector search (Auto-Embedding) is **always enabled**.

## Features

- **Knowledge** – semantic RAG-style long-term memory with automatic vector indexing
- **Tasks** – actionable planning and tracking
- **Journal** – temporal reflections and logs
- **Identity** – rich personality/profile with Big Five traits, values, goals, cognitive style, and self-reflection (meta-cognition)
- Smart config detection: environment variables → workspace `.env` / `mongo.env` / YAML files
- Fully async, structured Pydantic outputs
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

Replace `/path/to/your/project` and the URI as needed.

### Install from Source

```powershell
cd mongo-memories
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Tool Safety

This server is **strictly isolated** to agent memory and identity operations only.  
It cannot access general/production databases (use the separate `mongo-server` for that).

All tools are safe, policy-enforced, and designed for cognitive use.

## Usage

```powershell
python -m server
```

## Available Tools

Tools are grouped by cognitive domain for clarity in the MCP client UI.

### Knowledge (RAG / Long-term Memory)

- `knowledge_add_tool(content: str, memory_type: str = "general", metadata: dict | None = None)`
- `knowledge_get_tool(memory_id: str)`
- `knowledge_search_tool(query: str, limit: int = 10)`
- `knowledge_delete_tool(memory_id: str)`
- `knowledge_reindex_tool(collection: str = "memories", path: str = "content", model: str = "voyage-4")`

### Tasks (Actionable Planning)

- `tasks_create_tool(title: str, description: str, status: str = "pending")`
- `tasks_list_tool(status: str | None = None)`
- `tasks_complete_tool(task_id: str)`
- `tasks_delete_tool(task_id: str)`

### Journal (Reflections / Logs)

- `journal_add_entry_tool(entry: str)`
- `journal_list_entries_tool(limit: int = 50)`

### Identity / Personality (Self-Concept)

- `identity_get_tool()` – Retrieve full personality profile
- `identity_update_tool(profile_updates: dict)` – Update Big Five traits, values, goals, cognitive style, etc.
- `identity_reflect_tool()` – Agent performs self-reflection and suggests improvements

### Utilities

- `get_capabilities()`
- `get_version()`

## Configuration Options

| Variable          | Description                              | Default                     |
|-------------------|------------------------------------------|-----------------------------|
| `MONGO_URI`       | MongoDB connection string                | `mongodb://localhost:27017` |
| `MONGO_DATABASE`  | Database name for memories               | `agent_memory`              |
| `MONGO_AGENT_NAME`| Auto-creates database `agent_<name>`     | (none)                      |

Vector search (Auto-Embedding) is **always enabled** in this server.

## License

Apache 2.0
