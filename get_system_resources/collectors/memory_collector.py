import psutil
from ..models import MemoryModel
from ..utils import gb


def collect_memory() -> MemoryModel:
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()

    return MemoryModel(
        total_virtual_memory_gb=gb(virtual_mem.total),
        used_virtual_memory_gb=gb(virtual_mem.used),
        available_virtual_memory_gb=gb(virtual_mem.available),
        virtual_memory_usage_percent=virtual_mem.percent,
        total_swap_memory_gb=gb(swap_mem.total),
        used_swap_memory_gb=gb(swap_mem.used),
        available_swap_memory_gb=gb(swap_mem.free),
        swap_memory_usage_percent=swap_mem.percent,
    )
