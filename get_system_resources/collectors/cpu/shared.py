from typing import Sequence
import psutil
import platform
import subprocess
from models import CPUCoreModel, CPUTopologyModel, SystemTopologyModel, CacheInfo


def build_per_core(utilization: Sequence[float], freq=None):
    return [
        CPUCoreModel(
            core_id=i,
            utilization_percent=float(u),
            frequency_ghz=(freq.current / 1000 if freq else None),
        )
        for i, u in enumerate(utilization)
    ]


def normalize_arch(arch: str) -> str:
    arch = arch.lower()
    if arch in ("amd64", "x86_64"):
        return "x86_64"
    if arch in ("arm64", "aarch64"):
        return "arm64"
    return arch


def _get_windows_sockets() -> int:
    try:
        out = subprocess.check_output(
            ["wmic", "cpu", "get", "SocketDesignation"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        sockets = set()
        for line in out.splitlines():
            line = line.strip()
            if line and "Socket" not in line:
                sockets.add(line)
        return len(sockets) if sockets else 1
    except Exception:
        return 1


def _get_linux_sockets() -> int:
    try:
        sockets = set()
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("physical id"):
                    sockets.add(line.split(":")[1].strip())
        return len(sockets) if sockets else 1
    except Exception:
        return 1


def _get_macos_sockets() -> int:
    return 1  # macOS abstracts this away, usually 1 socket even on multi-chip systems


def get_sockets(os_name: str) -> int:
    os_name = os_name.lower()
    match os_name:
        case "windows":
            return _get_windows_sockets()
        case "linux":
            return _get_linux_sockets()
        case "darwin":
            return _get_macos_sockets()
        case _:
            return 1


def build_memory_model():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024**3), 2),
        "used_gb": round(mem.used / (1024**3), 2),
        "available_gb": round(mem.available / (1024**3), 2),
        "usage_percent": mem.percent,
    }


def unsupported_cache(unit: str) -> CacheInfo:
    return CacheInfo(
        value=None,
        status="not_supported",
        unit=unit,
        source="os_abstracted",
    )


def build_topology(os_name: str) -> SystemTopologyModel:
    return SystemTopologyModel(
        os=os_name,
        cpu=CPUTopologyModel(
            architecture=normalize_arch(platform.machine()),
            sockets=get_sockets(os_name),
            physical_cores=psutil.cpu_count(logical=False) or 0,
            logical_cores=psutil.cpu_count(logical=True) or 0,
            threads=sum(p.num_threads() for p in psutil.process_iter()),
        ),
        memory_model=build_memory_model(),
    )
