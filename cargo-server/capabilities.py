import shutil
import platform
from models import CargoCapabilitiesModel


def collect_capabilities() -> CargoCapabilitiesModel:
    """Return structured Cargo environment capabilities (Pydantic model)."""
    return CargoCapabilitiesModel(
        platform=platform.system(),
        cargo_available=shutil.which("cargo") is not None,
        rustc_available=shutil.which("rustc") is not None,
        rustup_available=shutil.which("rustup") is not None,
        supported_commands=[
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
        ],
    )
