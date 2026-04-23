import platform
from typing import List

from get_system_resources.models import GPUDeviceModel, GPUModel
from get_system_resources.utils import human_readable_size


def _to_int_bytes(value) -> int:
    if isinstance(value, int):
        return value

    if isinstance(value, bytes):
        return int(value.decode(errors="ignore"))

    if isinstance(value, str):
        return int(value)

    # ctypes / unknown NVML types
    try:
        return int(value)
    except Exception:
        return 0


# =========================
# NVIDIA (NVML)
# =========================
def _collect_nvidia() -> List[GPUDeviceModel]:
    try:
        import pynvml  # NVML bindings

        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()

        devices = []

        cuda_version = None
        try:
            cuda_version = pynvml.nvmlSystemGetCudaDriverVersion()
            cuda_version = f"{cuda_version}"
        except Exception:
            pass

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)

            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode()
            driver_version = pynvml.nvmlSystemGetDriverVersion()
            if isinstance(driver_version, bytes):
                driver_version = driver_version.decode()

            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            mem_total = _to_int_bytes(mem.total)
            mem_used = _to_int_bytes(mem.used)
            mem_free = _to_int_bytes(mem.free)

            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            utilization_int = int(util.gpu) if hasattr(util, "gpu") else None
            utilization_float = (
                float(utilization_int / 100) if utilization_int is not None else None
            )

            temp = None
            try:
                temp = pynvml.nvmlDeviceGetTemperature(
                    handle, pynvml.NVML_TEMPERATURE_GPU
                )
            except Exception:
                pass

            # c_nvmlMemory_t(total: 10737418240 B, free: 327372800 B, used: 10410045440 B)

            devices.append(
                GPUDeviceModel(
                    vendor="NVIDIA",
                    name=name,
                    driver_version=driver_version,
                    cuda_version=cuda_version,
                    vram_total_mb=human_readable_size(mem_total),
                    vram_used_mb=human_readable_size(mem_used),
                    vram_free_mb=human_readable_size(mem_free),
                    utilization_percent=utilization_float,
                    temperature_c=temp,
                )
            )

        pynvml.nvmlShutdown()
        return devices

    except Exception:
        return []


# =========================
# AMD (ROCm via pyrsmi)
# =========================
def _collect_amd() -> list[GPUDeviceModel]:
    try:
        from pyrsmi import rocml

        rocml.smi_initialize()

        devices: list[GPUDeviceModel] = []

        count = rocml.smi_get_device_count()

        for i in range(count):
            name = rocml.smi_get_device_name(i)

            mem_total = _to_int_bytes(rocml.smi_get_device_memory_total(i))
            mem_used = _to_int_bytes(rocml.smi_get_device_memory_used(i))
            mem_free = max(mem_total - mem_used, 0)

            util = None
            try:
                util = rocml.smi_get_device_utilization(i)
            except Exception:
                pass

            devices.append(
                GPUDeviceModel(
                    vendor="AMD",
                    name=name,
                    driver_version=f"Kernel Version: {rocml.smi_get_kernel_version()}",
                    rocm_version="Unsupported",
                    vram_total_mb=human_readable_size(mem_total),
                    vram_used_mb=human_readable_size(mem_used),
                    vram_free_mb=human_readable_size(mem_free),
                    utilization_percent=util,
                    temperature_c=None,
                )
            )

        rocml.smi_shutdown()
        return devices

    except Exception:
        return []


# =========================
# Apple (Darwin fallback only)
# =========================
def _collect_apple() -> List[GPUDeviceModel]:
    if platform.system() != "Darwin":
        return []

    import subprocess
    import re

    out = subprocess.check_output(
        ["system_profiler", "SPDisplaysDataType"],
        text=True,
        stderr=subprocess.DEVNULL,
    )

    name_match = re.search(r"Chipset Model:\s*(.+)", out)

    return [
        GPUDeviceModel(
            vendor="Apple",
            name=name_match.group(1).strip() if name_match else "Apple GPU",
            driver_version=None,
            metal_version="Supported",
            vram_total_mb=None,
            vram_used_mb=None,
            vram_free_mb=None,
            utilization_percent=None,
            temperature_c=None,
        )
    ]


# =========================
# Dispatcher
# =========================
def collect_gpu() -> GPUModel:
    nvidia_devices = _collect_nvidia()
    if nvidia_devices:
        return GPUModel(devices=nvidia_devices)

    amd_devices = _collect_amd()
    if amd_devices:
        return GPUModel(devices=amd_devices)

    apple_devices: List[GPUDeviceModel] = []
    if platform.system() == "Darwin":
        apple_devices = _collect_apple()

    return GPUModel(devices=apple_devices)
