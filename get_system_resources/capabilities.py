import platform
import shutil
import psutil

from get_system_resources.models import (
    SystemCapabilitiesModel,
    CPUCapabilitiesModel,
    MemoryCapabilitiesModel,
    DiskCapabilitiesModel,
    NetworkCapabilitiesModel,
    GPUCapabilitiesModel,
    ReliabilityModel,
)


def _has_cmd(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def collect_capabilities() -> SystemCapabilitiesModel:
    system = platform.system()

    return SystemCapabilitiesModel(
        platform=system,
        cpu=CPUCapabilitiesModel(
            per_core_usage=True,
            topology_detection=True,
            socket_detection=system in ["Windows", "Linux"],
            cache_detection=False,
        ),
        memory=MemoryCapabilitiesModel(
            virtual_memory=True,
            swap_memory=True,
            detailed_breakdown=True,
        ),
        disk=DiskCapabilitiesModel(
            partition_usage=True,
            io_counters=hasattr(psutil, "disk_io_counters"),
        ),
        network=NetworkCapabilitiesModel(
            interface_detection=True,
            link_speed=True,
            latency_probe=True,
            external_ping=True,
        ),
        gpu=GPUCapabilitiesModel(
            nvidia_smi=_has_cmd("nvidia-smi"),
            rocm_smi=_has_cmd("rocm-smi") or _has_cmd("amd-smi"),
            directx=system == "Windows",
            metal=system == "Darwin",
            driver_version=True,
            compute_stack_version=True,
        ),
        reliability=ReliabilityModel(
            cpu_topology="estimated",
            gpu_detection="vendor_dependent",
            network_latency="active_probe",
        ),
    )
