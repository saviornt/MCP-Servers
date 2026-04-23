import socket
from collections import namedtuple

import pytest

from get_system_resources.capabilities import collect_capabilities
from get_system_resources.collectors.disk_collector import collect_disk
from get_system_resources.collectors.gpu_collector import collect_gpu, GPUDeviceModel
from get_system_resources.collectors.network_collector import collect_network
from get_system_resources.collectors.system_collector import collect_system
from get_system_resources.collectors.memory_collector import collect_memory
import get_system_resources.collectors.gpu_collector as gpu_collector
import get_system_resources.collectors.network_collector as network_collector
import get_system_resources.collectors.disk_collector as disk_collector
import get_system_resources.collectors.system_collector as system_collector
import get_system_resources.collectors.memory_collector as memory_collector
import get_system_resources.collectors.cpu.dispatcher as cpu_dispatcher


class DummyVCObject:
    def __init__(self, total, used, available, percent):
        self.total = total
        self.used = used
        self.available = available
        self.percent = percent


class DummySwapObject:
    def __init__(self, total, used, free, percent):
        self.total = total
        self.used = used
        self.free = free
        self.percent = percent


def test_collect_system_returns_system_model(monkeypatch):
    monkeypatch.setattr(system_collector.platform, "system", lambda: "Linux")
    monkeypatch.setattr(system_collector.platform, "release", lambda: "5.15")
    monkeypatch.setattr(system_collector.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(system_collector.platform, "processor", lambda: "Intel")

    system_model = collect_system()

    assert system_model.os == "Linux"
    assert system_model.release == "5.15"
    assert system_model.machine == "x86_64"
    assert system_model.processor == "Intel"


def test_collect_memory_converts_values(monkeypatch):
    monkeypatch.setattr(
        memory_collector.psutil,
        "virtual_memory",
        lambda: DummyVCObject(8 * 1024**3, 2 * 1024**3, 6 * 1024**3, 25.0),
    )
    monkeypatch.setattr(
        memory_collector.psutil,
        "swap_memory",
        lambda: DummySwapObject(1 * 1024**3, 200 * 1024**2, 824 * 1024**2, 20.0),
    )

    memory_model = collect_memory()

    assert memory_model.total_virtual_memory_gb == 8.0
    assert memory_model.used_virtual_memory_gb == 2.0
    assert memory_model.available_virtual_memory_gb == 6.0
    assert memory_model.virtual_memory_usage_percent == 25.0
    assert memory_model.total_swap_memory_gb == 1.0
    assert memory_model.used_swap_memory_gb == 0.2
    assert memory_model.available_swap_memory_gb == 0.8
    assert memory_model.swap_memory_usage_percent == 20.0


def test_collect_disk_honors_permissions(monkeypatch):
    Partition = namedtuple("Partition", ["mountpoint"])
    Usage = namedtuple("Usage", ["total", "used", "free", "percent"])

    monkeypatch.setattr(
        disk_collector.psutil, "disk_partitions", lambda all=False: [Partition("/mnt")]
    )
    monkeypatch.setattr(
        disk_collector.psutil,
        "disk_usage",
        lambda mp: Usage(100 * 1024**3, 50 * 1024**3, 50 * 1024**3, 50.0),
    )

    disks = collect_disk()

    assert len(disks) == 1
    assert disks[0].mountpoint == "/mnt"
    assert disks[0].usage_percent == 50.0


def test_collect_network_builds_interface_data(monkeypatch):
    Addr = namedtuple("Addr", ["family", "address"])
    Stat = namedtuple("Stat", ["isup", "speed", "mtu"])
    IoCounters = namedtuple(
        "IoCounters",
        ["bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin", "errout"],
    )

    monkeypatch.setattr(
        network_collector.psutil,
        "net_io_counters",
        lambda: IoCounters(1000, 2000, 10, 20, 0, 0),
    )
    monkeypatch.setattr(
        network_collector.psutil,
        "net_if_addrs",
        lambda: {
            "eth0": [
                Addr(socket.AF_INET, "192.168.0.2"),
                Addr(socket.AF_INET6, "fe80::1"),
            ]
        },
    )
    monkeypatch.setattr(
        network_collector.psutil,
        "net_if_stats",
        lambda: {"eth0": Stat(True, 1000, 1500)},
    )
    monkeypatch.setattr(
        network_collector.subprocess,
        "check_output",
        lambda *args, **kwargs: (
            "64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=10.3 ms"
        ),
    )

    network_model = collect_network()

    assert network_model.bytes_sent.raw_bytes == 1000
    assert network_model.latency.status == "ok"
    assert network_model.interfaces[0].ip_v4 == "192.168.0.2"


def test_collect_gpu_returns_empty_when_no_backends(monkeypatch):
    monkeypatch.setattr(gpu_collector, "_collect_nvidia", lambda: [])
    monkeypatch.setattr(gpu_collector, "_collect_amd", lambda: [])
    monkeypatch.setattr(gpu_collector.platform, "system", lambda: "Linux")

    gpu_model = collect_gpu()

    assert gpu_model.devices == []


def test_cpu_dispatcher_raises_for_unknown_platform(monkeypatch):
    monkeypatch.setattr(cpu_dispatcher.platform, "system", lambda: "UnsupportedOS")
    with pytest.raises(NotImplementedError):
        cpu_dispatcher.collect_cpu()
