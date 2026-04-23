import platform
from get_system_resources.models import SystemModel


def collect_system() -> SystemModel:
    return SystemModel(
        os=platform.system(),
        release=platform.release(),
        machine=platform.machine(),
        processor=platform.processor() or "Unknown",
    )
