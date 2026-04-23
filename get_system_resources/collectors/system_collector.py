import os
import platform
from models import SystemModel
from utils import get_cpu_model_name, get_host_os


def collect_system() -> SystemModel:
    """Minimal system collector.

    Uses HOST_* environment variables (from --env or entrypoint.sh) when available.
    """
    host_os = get_host_os()
    host_release = os.getenv("HOST_RELEASE")

    # Main path: use host info passed from Docker (this should be active now)
    if host_os:
        return SystemModel(
            os=host_os,
            release=host_release or "",
            machine=platform.machine(),
            processor=get_cpu_model_name(),
        )

    # Fallback for native Linux, macOS, etc. (no env vars set)
    return SystemModel(
        os=platform.system(),
        release=platform.release() or "",
        machine=platform.machine(),
        processor=get_cpu_model_name(),
    )
