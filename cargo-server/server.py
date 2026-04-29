__version__ = "1.0.0"

from fastmcp import FastMCP
from cargo_collector import (
    get_cargo_version,
    cargo_metadata,
    execute_cargo_command,
    cargo_build,
    cargo_check,
    cargo_test,
    cargo_run,
    cargo_add,
    cargo_new,
)
from capabilities import collect_capabilities


mcp = FastMCP(
    name="cargo-server",
    instructions="Cargo (Rust) package manager and build tool for creating, building, testing, and managing Rust projects. All operations run inside the container with the full Rust toolchain. Use /workspace as the default project path (mount your project there).",
)


@mcp.tool()
async def get_cargo_version_tool():
    return await get_cargo_version()


@mcp.tool()
async def get_cargo_metadata(project_path: str = "/workspace"):
    return await cargo_metadata(project_path)


@mcp.tool()
async def execute_cargo_command_tool(
    subcommand: str, project_path: str = "/workspace", args: list[str] | None = None
):
    """General-purpose cargo subcommand executor (subject to policy allowlist)."""
    return await execute_cargo_command(subcommand, project_path, args)


@mcp.tool()
async def cargo_build_tool(project_path: str = "/workspace", release: bool = False):
    return await cargo_build(project_path, release)


@mcp.tool()
async def cargo_check_tool(project_path: str = "/workspace"):
    return await cargo_check(project_path)


@mcp.tool()
async def cargo_test_tool(project_path: str = "/workspace", release: bool = False):
    return await cargo_test(project_path, release)


@mcp.tool()
async def cargo_run_tool(
    project_path: str = "/workspace",
    release: bool = False,
    args: list[str] | None = None,
):
    return await cargo_run(project_path, release, args)


@mcp.tool()
async def cargo_add_tool(
    crate: str, project_path: str = "/workspace", dev: bool = False
):
    return await cargo_add(crate, project_path, dev)


@mcp.tool()
async def cargo_new_tool(
    name: str, base_path: str = "/workspace", library: bool = False
):
    return await cargo_new(name, base_path, library)


@mcp.tool()
async def get_capabilities():
    return collect_capabilities()  # still sync (fast)


@mcp.tool()
def get_version():
    return {"version": __version__}


if __name__ == "__main__":
    mcp.run()
