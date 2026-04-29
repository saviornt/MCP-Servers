# cargo-server

An MCP server providing tools for Cargo (Rust package manager and build tool). Enables agents to create, build, test, run, and manage Rust projects with structured Pydantic outputs.

## Features

- Full Rust toolchain (rustup + cargo) pre-installed in container
- Safe command execution with policy enforcement
- Volume-mounted workspace for your Rust projects
- Structured Pydantic responses for all tools
- Publishable to GHCR

## Installation

### Quick Start with MCP (recommended)

Add to your client's `mcp.json`:

```json
{
  "mcpServers": {
    "cargo-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-v",
        "/path/to/your/rust/project:/workspace",
        "ghcr.io/saviornt/MCP-Servers/cargo-server:latest"
      ]
    }
  }
}
```

(Replace `/path/to/your/rust/project` with your actual project directory.)

### Install from Source

1. `cd cargo-server`
2. `python -m venv .venv`
3. Activate venv
4. `pip install -e .`

## Tool Safety

This MCP server enforces a **strict allowlist** of permitted `cargo` subcommands for security reasons. All tools that execute cargo commands (including the general `execute_cargo_command` tool) are subject to this policy.

**Allowed Cargo Commands:**

- `build`
- `check`
- `test`
- `run`
- `add`
- `new`
- `metadata`
- `clippy`
- `clean`
- `update`
- `remove`

Any attempt to run a command outside this list will be blocked by the policy.

## Usage

`python -m server`

## Available Tools

(See `server.py` for full signatures – all default to `/workspace`.)

## License

Apache 2.0
