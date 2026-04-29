from pydantic import BaseModel
from typing import Optional, List, Literal


class CommandResultModel(BaseModel):
    success: bool
    returncode: int
    stdout: str
    stderr: str


class CargoVersionModel(BaseModel):
    rust_version: str
    cargo_version: str
    rustup_version: str
    host: str


class CargoPackageModel(BaseModel):
    name: str
    version: str
    authors: Optional[List[str]] = None
    edition: Optional[str] = None


class CargoDependencyModel(BaseModel):
    name: str
    version: str
    kind: Literal["normal", "dev", "build"] = "normal"


class CargoMetadataModel(BaseModel):
    name: str
    version: str
    edition: Optional[str]
    packages: List[CargoPackageModel]
    dependencies: List[CargoDependencyModel]
    workspace_members: Optional[List[str]] = None

class CargoCapabilitiesModel(BaseModel):
    """Structured capabilities report for the cargo-server."""

    platform: str
    cargo_available: bool
    rustc_available: bool
    rustup_available: bool
    supported_commands: list[str]