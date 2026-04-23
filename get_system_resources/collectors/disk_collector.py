import psutil
from models import DiskModel
from utils import gb


def collect_disk() -> list[DiskModel]:
    disks = []

    # Skip common noisy virtual filesystems that show up in Docker/WSL2
    ignore_fstypes = {"tmpfs", "devtmpfs", "overlay", "squashfs", "fuse.lxcfs"}

    for part in psutil.disk_partitions(all=False):
        if part.fstype in ignore_fstypes:
            continue

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

    # Sort by size descending (largest drive first) → root / will almost always be first
    disks.sort(key=lambda d: d.total_gb, reverse=True)

    # Extra safety: if / exists anywhere, move it to the very front
    root_disk = next((d for d in disks if d.mountpoint == "/"), None)
    if root_disk:
        disks.remove(root_disk)
        disks.insert(0, root_disk)

    return disks
