import subprocess
import asyncio


def run_cargo_command(cwd: str, cmd: list[str]) -> dict:
    """Synchronous Cargo runner (kept for reuse)."""
    try:
        result = subprocess.run(
            ["cargo"] + cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"success": False, "returncode": -1, "stdout": "", "stderr": str(e)}


async def run_cargo_command_async(cwd: str, cmd: list[str]) -> dict:
    """Async wrapper used by all collectors (non-blocking)."""

    def _sync_wrapper():
        return run_cargo_command(cwd, cmd)

    return await asyncio.to_thread(_sync_wrapper)
