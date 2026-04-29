__version__ = "1.0.0"

from fastmcp import FastMCP
from collectors import (
    knowledge_add,
    knowledge_get,
    knowledge_search,
    knowledge_delete,
    knowledge_reindex,
    tasks_create,
    tasks_list,
    tasks_complete,
    tasks_delete,
    journal_add_entry,
    journal_list_entries,
    identity_get,
    identity_update,
    identity_reflect
)
from capabilities import collect_capabilities
from config import MongoSettings

config = MongoSettings()

mcp = FastMCP(
    name="mongo-memories",
    instructions=(
        "Dedicated long-term agent memory system. "
        "Use knowledge_* tools for RAG-style long-term memory, "
        "tasks_* for actionable planning, and journal_* for reflections/logs. "
        "Vector search (Auto-Embedding) is always enabled."
    ),
)


# ===================== KNOWLEDGE (Long-term / RAG Memory) =====================
@mcp.tool()
async def knowledge_add_tool(
    content: str, memory_type: str = "general", metadata: dict | None = None
):
    """Add a new piece of knowledge to the agent's long-term memory."""
    return await knowledge_add(content, memory_type, metadata)


@mcp.tool()
async def knowledge_get_tool(memory_id: str):
    """Retrieve a specific knowledge item by ID."""
    return await knowledge_get(memory_id)


@mcp.tool()
async def knowledge_search_tool(query: str, limit: int = 10):
    """Semantic vector search over the agent's knowledge base."""
    return await knowledge_search(query, limit)


@mcp.tool()
async def knowledge_delete_tool(memory_id: str):
    """Delete a knowledge item."""
    return await knowledge_delete(memory_id)


@mcp.tool()
async def knowledge_reindex_tool(
    collection: str = "memories", path: str = "content", model: str = "voyage-4"
):
    """Rebuild the Auto-Embedding vector index (always available)."""
    return await knowledge_reindex(collection, path, model)


# ===================== TASKS =====================
@mcp.tool()
async def tasks_create_tool(title: str, description: str, status: str = "pending"):
    """Create a new actionable task for the agent."""
    return await tasks_create(title, description, status)


@mcp.tool()
async def tasks_list_tool(status: str | None = None):
    """List tasks, optionally filtered by status."""
    return await tasks_list(status)


@mcp.tool()
async def tasks_complete_tool(task_id: str):
    """Mark a task as completed."""
    return await tasks_complete(task_id)


@mcp.tool()
async def tasks_delete_tool(task_id: str):
    """Delete a task."""
    return await tasks_delete(task_id)


# ===================== JOURNAL =====================
@mcp.tool()
async def journal_add_entry_tool(entry: str):
    """Add a new journal / reflection entry."""
    return await journal_add_entry(entry)


@mcp.tool()
async def journal_list_entries_tool(limit: int = 50):
    """List recent journal entries (newest first)."""
    return await journal_list_entries(limit)

# ===================== IDENTITY / PERSONALITY =====================
@mcp.tool()
async def identity_get_tool():
    """Retrieve the agent's full identity and personality profile."""
    return await identity_get()


@mcp.tool()
async def identity_update_tool(profile_updates: dict):
    """Update or create the agent's identity/personality profile (Big Five, values, goals, etc.)."""
    return await identity_update(profile_updates)


@mcp.tool()
async def identity_reflect_tool():
    """Agent reflects on its own identity and suggests improvements."""
    return await identity_reflect()


# ===================== UTILITIES =====================
@mcp.tool()
async def get_capabilities():
    """Report server capabilities."""
    return collect_capabilities()


@mcp.tool()
def get_version():
    """Return the current server version."""
    return {"version": __version__}


if __name__ == "__main__":
    mcp.run()
