from mcp.server.fastmcp import FastMCP
import redis.asyncio as redis
import json
import time
from typing import Any

mcp = FastMCP("redis-memory")

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def normalize(value: Any):
    """Ensure MCP always returns JSON-safe primitives"""
    if value is None:
        return None
    if isinstance(value, (dict, list, str, int, float, bool)):
        return value
    return str(value)


@mcp.tool()
async def set_state(key: str, value: str):
    payload = {"value": value, "timestamp": time.time()}
    await r.set(key, json.dumps(payload))
    return "OK"


@mcp.tool()
async def get_state(key: str):
    data = await r.get(key)
    if not data:
        return None
    return normalize(json.loads(data))


@mcp.tool()
async def append_log(key: str, event: str):
    r.lpush(f"log:{key}", event)
    return "logged"


if __name__ == "__main__":
    mcp.run()
