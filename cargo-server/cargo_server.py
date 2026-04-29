from mcp.server.fastmcp import FastMCP
import subprocess
from policy.cargo_policy import validate_cargo

mcp = FastMCP("cargo")


def run_cargo(args):
    result = subprocess.run(["cargo"] + args, capture_output=True, text=True)
    return result.stdout + result.stderr


@mcp.tool()
def cargo_build():
    if not validate_cargo("build"):
        return "Blocked"
    return run_cargo(["build"])


@mcp.tool()
def cargo_test():
    if not validate_cargo("test"):
        return "Blocked"
    return run_cargo(["test"])


@mcp.tool()
def cargo_check():
    return run_cargo(["check"])


if __name__ == "__main__":
    mcp.run()
