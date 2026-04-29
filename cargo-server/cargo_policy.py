ALLOWED_CARGO_COMMANDS = {"build", "test", "check", "run", "clippy"}


def validate_cargo(cmd: str) -> bool:
    return cmd in ALLOWED_CARGO_COMMANDS
