ALLOWED_CARGO_COMMANDS = {
    "build",
    "check",
    "test",
    "run",
    "add",
    "new",
    "metadata",
    "clippy",
    "clean",
    "update",
    "remove",
}


def validate_cargo(cmd: str) -> bool:
    return cmd in ALLOWED_CARGO_COMMANDS
