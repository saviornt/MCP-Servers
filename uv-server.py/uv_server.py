from mcp.server.fastmcp import FastMCP
import subprocess
from policy.uv_policy import validate_uv

mcp = FastMCP("uv")


def run_uv(args):
    result = subprocess.run(["uv"] + args, capture_output=True, text=True)
    return result.stdout + result.stderr


@mcp.tool()
def uv_install(package: str) -> str:
    if not validate_uv("pip_install"):
        return "Blocked by policy"
    return run_uv(["pip", "install", package])


@mcp.tool()
def uv_sync() -> str:
    if not validate_uv("sync"):
        return "Blocked by policy"
    return run_uv(["sync"])


@mcp.tool()
def uv_run(script: str) -> str:
    if not validate_uv("run"):
        return "Blocked by policy"
    return run_uv(["run", script])


if __name__ == "__main__":
    mcp.run()
