ALLOWED_UV_COMMANDS = {"pip_install", "sync", "run"}


def validate_uv(cmd: str) -> bool:
    return cmd in ALLOWED_UV_COMMANDS
