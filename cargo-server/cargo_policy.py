# TODO Review the below comments and implement them.
# Instead of having a strict, hardcoded allowed list,
# we should give the user the ability to turn on/off
# the various cargo commands that they want their agent
# to be able to run.

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
