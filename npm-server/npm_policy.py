ALLOWED_SCRIPTS = {"install", "run", "test", "build", "list"}


def validate_script(script: str) -> bool:
    return script in ALLOWED_SCRIPTS
