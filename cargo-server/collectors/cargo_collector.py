import json
import asyncio
import subprocess
from cargo_policy import validate_cargo
from utils import run_cargo_command_async
from models import CargoVersionModel, CargoMetadataModel, CommandResultModel


async def get_cargo_version():
    """Return structured Rust/Cargo/rustup versions (async)."""
    try:
        rust = await asyncio.to_thread(
            lambda: subprocess.run(
                ["rustc", "--version"], capture_output=True, text=True, timeout=10
            ).stdout.strip()
        )
        cargo = await asyncio.to_thread(
            lambda: subprocess.run(
                ["cargo", "--version"], capture_output=True, text=True, timeout=10
            ).stdout.strip()
        )
        rustup = await asyncio.to_thread(
            lambda: (
                subprocess.run(
                    ["rustup", "--version"], capture_output=True, text=True, timeout=10
                ).stdout.strip()
                or "unknown"
            )
        )
        host = await asyncio.to_thread(
            lambda: subprocess.run(
                ["rustc", "--print", "host"], capture_output=True, text=True, timeout=10
            ).stdout.strip()
        )

        return CargoVersionModel(
            rust_version=rust.split()[1] if rust else "unknown",
            cargo_version=cargo.split()[1] if cargo else "unknown",
            rustup_version=rustup.split()[1] if rustup != "unknown" else "unknown",
            host=host or "unknown",
        )
    except Exception as e:
        return {"error": f"Cargo/Rust not available: {e}"}


async def cargo_metadata(project_path: str = "/workspace"):
    result = await run_cargo_command_async(
        project_path, ["metadata", "--format-version", "1"]
    )
    if not result["success"]:
        return CommandResultModel(**result)
    try:
        data = json.loads(result["stdout"])
        pkg = data.get("packages", [{}])[0]
        return CargoMetadataModel(
            name=pkg.get("name", "unknown"),
            version=pkg.get("version", "unknown"),
            edition=pkg.get("edition"),
            packages=[],
            dependencies=[],
        )
    except Exception:
        return CommandResultModel(**result)


async def execute_cargo_command(
    subcommand: str, project_path: str = "/workspace", args: list[str] | None = None
):
    """Execute any allowed cargo subcommand (subcommand is required)."""
    if not validate_cargo(subcommand):
        return CommandResultModel(
            success=False, returncode=1, stdout="", stderr="Command blocked by policy"
        )
    cmd = [subcommand] + (args or [])
    result = await run_cargo_command_async(project_path, cmd)
    return CommandResultModel(**result)


async def cargo_build(project_path: str = "/workspace", release: bool = False):
    cmd = ["build"] + (["--release"] if release else [])
    result = await run_cargo_command_async(project_path, cmd)
    return CommandResultModel(**result)


async def cargo_check(project_path: str = "/workspace"):
    result = await run_cargo_command_async(project_path, ["check"])
    return CommandResultModel(**result)


async def cargo_test(project_path: str = "/workspace", release: bool = False):
    cmd = ["test"] + (["--release"] if release else [])
    result = await run_cargo_command_async(project_path, cmd)
    return CommandResultModel(**result)


async def cargo_run(
    project_path: str = "/workspace", release: bool = False, args: list | None = None
):
    cmd = ["run"] + (["--release"] if release else []) + (args or [])
    result = await run_cargo_command_async(project_path, cmd)
    return CommandResultModel(**result)


async def cargo_add(crate: str, project_path: str = "/workspace", dev: bool = False):
    cmd = ["add", crate] + (["--dev"] if dev else [])
    result = await run_cargo_command_async(project_path, cmd)
    return CommandResultModel(**result)


async def cargo_new(name: str, base_path: str = "/workspace", library: bool = False):
    cmd = ["new", name] + (["--lib"] if library else ["--bin"])
    result = await run_cargo_command_async(base_path, cmd)
    return CommandResultModel(**result)
