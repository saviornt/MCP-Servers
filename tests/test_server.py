import pytest

from get_system_resources import server


@pytest.mark.asyncio
async def test_get_cpu_calls_underlying_collector(monkeypatch):
    monkeypatch.setattr(server, "collect_cpu", lambda: {"cpu": 1})
    assert await server.get_cpu() == {"cpu": 1}


@pytest.mark.asyncio
async def test_get_all_builds_combined_model(monkeypatch):
    monkeypatch.setattr(server, "collect_cpu", lambda: "cpu_data")
    monkeypatch.setattr(server, "collect_memory", lambda: "memory_data")
    monkeypatch.setattr(server, "collect_disk", lambda: "disk_data")
    monkeypatch.setattr(server, "collect_gpu", lambda: "gpu_data")
    monkeypatch.setattr(server, "collect_network", lambda: "network_data")
    monkeypatch.setattr(server, "collect_system", lambda: "system_data")
    monkeypatch.setattr(server, "SystemResourcesModel", lambda **kwargs: kwargs)

    result = await server.get_all()

    assert result == {
        "cpu": "cpu_data",
        "memory": "memory_data",
        "disk": "disk_data",
        "gpu": "gpu_data",
        "network": "network_data",
        "system": "system_data",
    }


def test_get_version_returns_package_version():
    assert server.get_version() == {"version": server.__version__}
