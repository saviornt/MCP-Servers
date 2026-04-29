from mcp.server.fastmcp import FastMCP
import subprocess
from policy.npm_policy import validate_script

mcp = FastMCP("npm")


def run_npm(args):
    result = subprocess.run(["npm"] + args, capture_output=True, text=True)
    return result.stdout + result.stderr


@mcp.tool()
def npm_run(script: str) -> str:
    if not validate_script("run"):
        return "Blocked by policy"
    return run_npm(["run", script])


@mcp.tool()
def npm_install(package: str = "") -> str:
    if not validate_script("install"):
        return "Blocked by policy"
    return run_npm(["install", package] if package else ["install"])


@mcp.tool()
def npm_test() -> str:
    if not validate_script("test"):
        return "Blocked by policy"
    return run_npm(["test"])


if __name__ == "__main__":
    mcp.run()
