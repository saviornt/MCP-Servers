__version__ = "1.0.0"

from fastmcp import FastMCP
from collectors import (
    mongo_get_status,
    mongo_list_collections,
    mongo_insert_one,
    mongo_find_one,
    mongo_find,
    mongo_update_one,
    mongo_delete_one,
    mongo_ensure_vector_index,
    mongo_semantic_search,
)
from capabilities import collect_capabilities
from config import MongoSettings
from models import MongoStatusModel, CommandResultModel

config = MongoSettings()

mcp = FastMCP(
    name="mongo-server",
    instructions="Safe MongoDB CRUD. Use MONGO_URI and optional MONGO_VECTOR_SEARCH=true for Auto-Embedding + semantic search.",
)


# Core CRUD tools (agent can pass 'database' param)
@mcp.tool()
async def mongo_get_status_tool(database: str | None = None):
    return await mongo_get_status(database)


@mcp.tool()
async def mongo_list_collections_tool(database: str | None = None):
    return await mongo_list_collections(database)


@mcp.tool()
async def mongo_insert_one_tool(
    collection: str, document: dict, database: str | None = None
):
    return await mongo_insert_one(collection, document, database)


@mcp.tool()
async def mongo_find_one_tool(
    collection: str, query: dict, database: str | None = None
):
    return await mongo_find_one(collection, query, database)


@mcp.tool()
async def mongo_find_tool(
    collection: str, query: dict, limit: int = 50, database: str | None = None
):
    return await mongo_find(collection, query, limit, database)


@mcp.tool()
async def mongo_update_one_tool(
    collection: str, query: dict, update: dict, database: str | None = None
):
    return await mongo_update_one(collection, query, update, database)


@mcp.tool()
async def mongo_delete_one_tool(
    collection: str, query: dict, database: str | None = None
):
    return await mongo_delete_one(collection, query, database)


# Vector tools (only useful when MONGO_VECTOR_SEARCH=true)
@mcp.tool()
async def mongo_ensure_vector_index_tool(
    collection: str = "memories", path: str = "content", model: str = "voyage-4"
):
    return await mongo_ensure_vector_index(collection, path, model)


@mcp.tool()
async def mongo_semantic_search_tool(
    collection: str, query: str, limit: int = 10, path: str = "content"
):
    return await mongo_semantic_search(collection, query, limit, path)


@mcp.tool()
async def get_capabilities():
    return collect_capabilities()


@mcp.tool()
def get_version():
    return {"version": __version__}


if __name__ == "__main__":
    mcp.run()
