from mcp.server.fastmcp import FastMCP
from pymongo import AsyncMongoClient
from datetime import datetime, timezone

mcp = FastMCP("mongo-memory")

client = AsyncMongoClient("mongodb://localhost:27017")
db = client.agentos


@mcp.tool()
async def store_knowledge(topic: str, data: str):
    await db.knowledge.update_one(
        {"topic": topic},
        {"$set": {"data": data, "updated": datetime.now(timezone.utc)}},
        upsert=True,
    )
    return "stored"


@mcp.tool()
async def get_knowledge(topic: str):
    return await db.knowledge.find_one({"topic": topic}, {"_id": 0})


@mcp.tool()
async def search_knowledge(query: str):
    return await db.knowledge.find(
        {"topic": {"$regex": query, "$options": "i"}}, {"_id": 0}
    ).to_list(length=50)


if __name__ == "__main__":
    mcp.run()
