import asyncio


async def run_async(func, *args, **kwargs):
    """Async wrapper for any blocking call (non-blocking MCP event loop)."""

    def _sync_wrapper():
        return func(*args, **kwargs)

    return await asyncio.to_thread(_sync_wrapper)
