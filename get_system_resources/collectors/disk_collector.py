import psutil
from get_system_resources.models import DiskModel
from get_system_resources.utils import gb


def collect_disk() -> list[DiskModel]:
    disks = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)

            disks.append(
                DiskModel(
                    mountpoint=part.mountpoint,
                    total_gb=gb(usage.total),
                    used_gb=gb(usage.used),
                    free_gb=gb(usage.free),
                    usage_percent=usage.percent,
                )
            )
        except PermissionError:
            continue

    return disks
