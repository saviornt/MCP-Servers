import platform
import pytest

from get_system_resources.capabilities import collect_capabilities


def test_collect_capabilities_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        "get_system_resources.capabilities.shutil.which", lambda cmd: False
    )

    capabilities = collect_capabilities()

    assert capabilities.platform == "Windows"
    assert capabilities.cpu.socket_detection is True
    assert capabilities.gpu.directx is True
    assert capabilities.gpu.metal is False
    assert capabilities.disk.partition_usage is True
    assert capabilities.disk.io_counters is True
    assert capabilities.reliability.cpu_topology == "estimated"


def test_collect_capabilities_macos(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        "get_system_resources.capabilities.shutil.which", lambda cmd: False
    )

    capabilities = collect_capabilities()

    assert capabilities.platform == "Darwin"
    assert capabilities.gpu.metal is True
    assert capabilities.gpu.directx is False
