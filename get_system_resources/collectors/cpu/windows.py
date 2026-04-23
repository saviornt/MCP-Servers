import psutil
import time
import subprocess
from typing import List
from models import CPUModel, CPUCoreModel, SystemTopologyModel
from .shared import build_per_core, build_topology, unsupported_cache

_boot = psutil.boot_time()


def _wmic(query: str) -> str:
    try:
        return subprocess.check_output(query, shell=True, text=True).strip()
    except Exception:
        return ""


def collect_cpu_windows() -> CPUModel:
    per_core_usage = psutil.cpu_percent(interval=0.3, percpu=True)
    freq = psutil.cpu_freq()
    per_core: List[CPUCoreModel] = build_per_core(per_core_usage, freq)

    # sockets (best-effort)
    sockets = None
    try:
        out = _wmic("wmic cpu get SocketDesignation")
        sockets = len(set(out.splitlines())) - 1
    except Exception:
        pass

    # virtualization
    virtualization = None
    try:
        out = _wmic("systeminfo")
        virtualization = "Hyper-V" in out or "Virtualization" in out
    except Exception:
        pass

    graph: SystemTopologyModel = build_topology("windows")

    return CPUModel(
        utilization_percent=psutil.cpu_percent(interval=0.3),
        base_speed_ghz=freq.current / 1000 if freq else None,
        logical_cores=psutil.cpu_count(logical=True) or 0,
        physical_cores=psutil.cpu_count(logical=False) or 0,
        sockets=sockets,
        process_count=len(psutil.pids()),
        thread_count=sum(p.num_threads() for p in psutil.process_iter()),
        uptime_seconds=time.time() - _boot,
        virtualization_enabled=virtualization,
        l1_cache_kb=unsupported_cache("KB"),
        l2_cache_mb=unsupported_cache("MB"),
        l3_cache_mb=unsupported_cache("MB"),
        per_core=per_core,
        topology=graph,
    )
