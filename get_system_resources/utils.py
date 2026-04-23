import shutil
import platform
import subprocess

from .models import ByteValueModel


def has_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def get_system_info():
    return {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Unknown",
    }


def human_readable_size(bytes_val: int) -> ByteValueModel:
    if bytes_val >= 1024**3:
        return ByteValueModel(
            value=round(bytes_val / (1024**3), 2),
            unit="GB",
            raw_bytes=bytes_val,
        )
    elif bytes_val >= 1024**2:
        return ByteValueModel(
            value=round(bytes_val / (1024**2), 2),
            unit="MB",
            raw_bytes=bytes_val,
        )
    elif bytes_val >= 1024:
        return ByteValueModel(
            value=round(bytes_val / 1024, 2),
            unit="KB",
            raw_bytes=bytes_val,
        )
    else:
        return ByteValueModel(
            value=bytes_val,
            unit="B",
            raw_bytes=bytes_val,
        )


def gb(bytes_val: int) -> float:
    return round(bytes_val / (1024**3), 2)


def run_cmd(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return ""


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_linux() -> bool:
    return platform.system() == "Linux"


def is_macos() -> bool:
    return platform.system() == "Darwin"
