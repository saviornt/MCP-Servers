from pymongo.asynchronous.mongo_client import AsyncMongoClient
from pymongo.operations import SearchIndexModel
import asyncio
from config import MongoSettings
from models import CommandResultModel, ConfigErrorModel

config = MongoSettings()


# ===================== KNOWLEDGE (Long-term / RAG Memory) =====================
async def knowledge_add(
    content: str, memory_type: str = "general", metadata: dict | None = None
):
    """Add a new piece of knowledge to the agent's long-term memory."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        doc = {
            "content": content,
            "memory_type": memory_type,
            "metadata": metadata or {},
            "timestamp": asyncio.get_event_loop().time(),
        }
        result = await client[config.mongo_database]["memories"].insert_one(doc)
        return CommandResultModel(
            success=True,
            message="Knowledge added",
            data={"id": str(result.inserted_id)},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def knowledge_get(memory_id: str):
    """Retrieve a specific knowledge item by ID."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[config.mongo_database]["memories"].find_one(
            {"_id": memory_id}
        )
        return CommandResultModel(
            success=True, message="Knowledge retrieved", data=result
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def knowledge_search(query: str, limit: int = 10):
    """Semantic vector search (always enabled in this server)."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "content",
                    "queryVector": query,
                    "limit": limit,
                    "numCandidates": limit * 10,
                }
            },
            {"$project": {"_id": 0, "score": {"$meta": "vectorSearchScore"}}},
        ]
        cursor = await client[config.mongo_database]["memories"].aggregate(pipeline)
        results = await cursor.to_list(length=limit)
        return CommandResultModel(
            success=True, message="Knowledge search complete", data=results
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def knowledge_delete(memory_id: str):
    """Delete a knowledge item."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[config.mongo_database]["memories"].delete_one(
            {"_id": memory_id}
        )
        return CommandResultModel(
            success=True,
            message="Knowledge deleted",
            data={"deleted_count": result.deleted_count},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def knowledge_reindex(
    collection: str = "memories", path: str = "content", model: str = "voyage-4"
):
    """Create / update the Auto-Embedding vector index (always enabled)."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        coll = client[config.mongo_database][collection]
        index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "autoEmbed",
                        "modality": "text",
                        "path": path,
                        "model": model,
                    },
                    {"type": "filter", "path": "memory_type"},
                ]
            },
            name="vector_index",
            type="vectorSearch",
        )
        await coll.create_search_index(model=index_model)
        cursor = await coll.list_search_indexes("vector_index")
        indexes = await cursor.to_list(length=10)
        if indexes and indexes[0].get("queryable") is True:
            return CommandResultModel(
                success=True,
                message="Knowledge reindexed (vector index ready)",
                data={"index": "vector_index"},
            )
        return CommandResultModel(
            success=True, message="Index created (still warming up)"
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


# ===================== TASKS =====================
async def tasks_create(title: str, description: str, status: str = "pending"):
    """Create a new actionable task."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        doc = {
            "title": title,
            "description": description,
            "status": status,
            "timestamp": asyncio.get_event_loop().time(),
        }
        result = await client[config.mongo_database]["tasks"].insert_one(doc)
        return CommandResultModel(
            success=True, message="Task created", data={"id": str(result.inserted_id)}
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def tasks_list(status: str | None = None):
    """List tasks, optionally filtered by status."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        query = {"status": status} if status else {}
        cursor = client[config.mongo_database]["tasks"].find(query)
        results = await cursor.to_list(length=100)
        return CommandResultModel(success=True, message="Tasks listed", data=results)
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def tasks_complete(task_id: str):
    """Mark a task as completed."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[config.mongo_database]["tasks"].update_one(
            {"_id": task_id}, {"$set": {"status": "completed"}}
        )
        return CommandResultModel(
            success=True,
            message="Task completed",
            data={"modified_count": result.modified_count},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def tasks_delete(task_id: str):
    """Delete a task."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[config.mongo_database]["tasks"].delete_one(
            {"_id": task_id}
        )
        return CommandResultModel(
            success=True,
            message="Task deleted",
            data={"deleted_count": result.deleted_count},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


# ===================== JOURNAL =====================
async def journal_add_entry(entry: str):
    """Add a new journal / reflection entry."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        doc = {"entry": entry, "timestamp": asyncio.get_event_loop().time()}
        result = await client[config.mongo_database]["journals"].insert_one(doc)
        return CommandResultModel(
            success=True,
            message="Journal entry added",
            data={"id": str(result.inserted_id)},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def journal_list_entries(limit: int = 50):
    """List recent journal entries."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        cursor = (
            client[config.mongo_database]["journals"]
            .find()
            .sort("timestamp", -1)
            .limit(limit)
        )
        results = await cursor.to_list(length=limit)
        return CommandResultModel(
            success=True, message="Journal entries listed", data=results
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))

# ===================== IDENTITY / PERSONALITY =====================
async def identity_get():
    """Retrieve the agent's full identity and personality profile."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        profile = await client[config.mongo_database]["identity"].find_one(
            {"_id": "agent_profile"}
        )
        if profile is None:
            return CommandResultModel(
                success=True,
                message="No identity profile exists yet – create one with identity_update",
                data=None,
            )
        return CommandResultModel(
            success=True, message="Identity profile retrieved", data=profile
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def identity_update(profile_updates: dict):
    """Update or create the agent's identity/personality profile. Supports partial updates."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        # Add timestamped history entry for self-reflection
        history_entry = {
            "timestamp": asyncio.get_event_loop().time(),
            "changes": profile_updates,
            "reason": profile_updates.get("reason", "Agent-initiated update"),
        }
        result = await client[config.mongo_database]["identity"].update_one(
            {"_id": "agent_profile"},
            {"$set": profile_updates, "$push": {"history": history_entry}},
            upsert=True,
        )
        return CommandResultModel(
            success=True,
            message="Identity profile updated",
            data={"upserted": bool(result.upserted_id)},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def identity_reflect():
    """Agent reflects on its own identity and suggests improvements (meta-cognition)."""
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    try:
        client = AsyncMongoClient(config.mongo_uri)
        profile = await client[config.mongo_database]["identity"].find_one(
            {"_id": "agent_profile"}
        )
        if not profile:
            return CommandResultModel(
                success=True,
                message="No profile yet – start with identity_update",
                data=None,
            )
        # Simple reflection logic (can be expanded with LLM call later)
        reflection = {
            "current_big_five": profile.get("personality", {}).get("big_five", {}),
            "suggested_improvements": "Consider increasing Openness if the agent is too rigid.",
            "timestamp": asyncio.get_event_loop().time(),
        }
        return CommandResultModel(
            success=True, message="Self-reflection complete", data=reflection
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))