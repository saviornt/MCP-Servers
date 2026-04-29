import platform

from linux import collect_cpu_linux
from windows import collect_cpu_windows
from darwin import collect_cpu_darwin


def collect_cpu():
    system = platform.system()

    if system == "Linux":
        return collect_cpu_linux()

    if system == "Windows":
        return collect_cpu_windows()

    if system == "Darwin":
        return collect_cpu_darwin()

    raise NotImplementedError(f"Unsupported OS: {system}")
