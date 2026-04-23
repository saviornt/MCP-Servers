import platform
from models import SystemModel


def collect_system() -> SystemModel:
    return SystemModel(
        os=platform.system(),
        release=platform.release(),
        machine=platform.machine(),
        processor=platform.processor() or "Unknown",
    )
