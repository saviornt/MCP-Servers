__version__ = "0.1.0"
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from fastmcp import FastMCP  # noqa: E402
from collectors.cpu.dispatcher import collect_cpu  # noqa: E402
from collectors.memory_collector import collect_memory  # noqa: E402
from collectors.disk_collector import collect_disk  # noqa: E402
from collectors.network_collector import collect_network  # noqa: E402
from collectors.system_collector import collect_system  # noqa: E402
from collectors.gpu_collector import collect_gpu  # noqa: E402
from capabilities import collect_capabilities  # noqa: E402
from models import SystemResourcesModel  # noqa: E402


mcp = FastMCP(
    name="get-system-resources",
    instructions="Cross-platform system resource inspection tool for an on-demand snapshot of system resources. Provides detailed information about CPU, memory, disk, GPU, and network status. Ideal for diagnostics, monitoring, and troubleshooting.",
)


@mcp.tool()
async def get_cpu():
    return collect_cpu()


@mcp.tool()
async def get_memory():
    return collect_memory()


@mcp.tool()
async def get_disk():
    return collect_disk()


@mcp.tool()
async def get_network():
    return collect_network()


@mcp.tool()
async def get_system():
    return collect_system()


@mcp.tool()
async def get_gpu():
    return collect_gpu()


@mcp.tool()
async def get_all():
    gpu_devices = collect_gpu()
    return SystemResourcesModel(
        cpu=collect_cpu(),
        memory=collect_memory(),
        disk=collect_disk(),
        gpu=gpu_devices,
        network=collect_network(),
        system=collect_system(),
    )


@mcp.tool()
async def get_capabilities():
    return collect_capabilities()


@mcp.tool()
def get_version():
    return {"version": __version__}


if __name__ == "__main__":
    mcp.run()
