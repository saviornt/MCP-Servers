import psutil
import time
from typing import List
from ...models import CPUCoreModel, CPUModel, SystemTopologyModel
from .shared import build_per_core, build_topology, unsupported_cache


_boot = psutil.boot_time()


def collect_cpu_linux() -> CPUModel:
    per_core_usage = psutil.cpu_percent(interval=0.3, percpu=True)
    freq = psutil.cpu_freq()

    per_core: List[CPUCoreModel] = build_per_core(per_core_usage, freq)
    graph: SystemTopologyModel = build_topology("linux")

    return CPUModel(
        utilization_percent=psutil.cpu_percent(interval=0.3),
        base_speed_ghz=freq.current / 1000 if freq else None,
        logical_cores=psutil.cpu_count(logical=True) or 0,
        physical_cores=psutil.cpu_count(logical=False) or 0,
        sockets=None,
        process_count=len(psutil.pids()),
        thread_count=sum(p.num_threads() for p in psutil.process_iter()),
        uptime_seconds=time.time() - _boot,
        virtualization_enabled=None,
        l1_cache_kb=unsupported_cache("KB"),
        l2_cache_mb=unsupported_cache("MB"),
        l3_cache_mb=unsupported_cache("MB"),
        per_core=per_core,
        topology=graph,
    )
