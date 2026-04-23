import psutil
import platform
import socket
import subprocess
import re
from ..models import (
    NetworkModel,
    NetworkInterfaceModel,
    LatencyModel,
)

from ..utils import human_readable_size


def _ping_google() -> LatencyModel:
    """
    Single ICMP ping to a stable public endpoint.
    """
    system = platform.system()

    if system == "Windows":
        cmd = ["ping", "-n", "1", "8.8.8.8"]
    else:
        cmd = ["ping", "-c", "1", "8.8.8.8"]

    try:
        output = subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.DEVNULL,
        )

        match = re.search(r"time[=<]([\d.]+)\s*ms", output)
        if match:
            return LatencyModel(
                value=float(match.group(1)),
                unit="ms",
                status="ok",
                target="8.8.8.8",
            )

        return LatencyModel(
            value=None,
            unit="ms",
            status="unparseable",
            target="8.8.8.8",
        )

    except Exception:
        return LatencyModel(
            value=None,
            unit="ms",
            status="unreachable",
            target="8.8.8.8",
        )


def _get_interfaces() -> list[NetworkInterfaceModel]:
    """
    Returns NIC information: IPs, speed, MTU, state.
    """
    interfaces = []

    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for name, addr_list in addrs.items():
        stat = stats.get(name)

        iface = {
            "name": name,
            "is_up": stat.isup if stat else None,
            "speed_mbps": stat.speed if stat else None,
            "mtu": stat.mtu if stat else None,
            "ip_v4": None,
            "ip_v6": None,
        }

        for addr in addr_list:
            if addr.family == socket.AF_INET:
                iface["ip_v4"] = addr.address
            elif addr.family == socket.AF_INET6:
                iface["ip_v6"] = addr.address

        interfaces.append(iface)

    return interfaces


def collect_network() -> NetworkModel:
    net = psutil.net_io_counters()

    return NetworkModel(
        bytes_sent=human_readable_size(net.bytes_sent),
        bytes_recv=human_readable_size(net.bytes_recv),
        packets_sent=net.packets_sent,
        packets_recv=net.packets_recv,
        errors_in=net.errin,
        errors_out=net.errout,
        interfaces=_get_interfaces(),
        latency=_ping_google(),
        source="psutil + system_ping",
        platform=platform.system(),
    )
