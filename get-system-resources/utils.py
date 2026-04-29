import shutil
import platform
import subprocess
import os

from models import ByteValueModel


def has_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def get_host_os() -> str:
    """Return the real host OS name (Windows 11 Pro, Ubuntu 24.04, macOS, etc.)
    Uses the HOST_OS environment variable set by entrypoint.sh / --env flags.
    """
    return os.getenv("HOST_OS") or platform.system()


def get_host_os_family() -> str:
    """Return normalized OS family for topology ('windows', 'darwin', 'linux')"""
    host_os = os.getenv("HOST_OS", "").lower()
    if "windows" in host_os:
        return "windows"
    if any(x in host_os for x in ["darwin", "macos", "mac"]):
        return "darwin"
    if "linux" in host_os:
        return "linux"
    # fallback
    return platform.system().lower()


def get_system_info():
    return {
        "os": get_host_os(),
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


def get_cpu_model_name() -> str:
    """Cross-platform CPU model name (Intel Core i9-9900K, Apple M3, etc.)"""
    # Linux / WSL2
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass

    # macOS
    try:
        return subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"], text=True, timeout=2
        ).strip()
    except Exception:
        pass

    # FreeBSD / other Unix
    try:
        return subprocess.check_output(
            ["sysctl", "-n", "hw.model"], text=True, timeout=2
        ).strip()
    except Exception:
        pass

    # Final fallback
    return platform.processor() or "Unknown CPU"
