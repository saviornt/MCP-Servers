from pydantic import BaseModel
from typing import Optional, List, Literal


# ================= COMMON =================

ByteUnit = Literal["B", "KB", "MB", "GB"]


class ByteValueModel(BaseModel):
    value: float | int
    unit: ByteUnit
    raw_bytes: int


# ================= CPU =================


class CPUCoreModel(BaseModel):
    core_id: int
    utilization_percent: float
    frequency_ghz: Optional[float]


class CPUTopologyModel(BaseModel):
    architecture: Optional[str]  # x86_64, arm64
    sockets: Optional[int]
    physical_cores: Optional[int]
    logical_cores: Optional[int]
    threads: Optional[float]


class SystemTopologyModel(BaseModel):
    os: str
    cpu: CPUTopologyModel
    memory_model: Optional[dict]


class CacheInfo(BaseModel):
    value: int | None
    unit: str = "KB"
    status: str  # available | not_supported | unknown
    source: str | None = None


class CPUModel(BaseModel):
    model_name: str = "Unknown"
    utilization_percent: float
    base_speed_ghz: Optional[float]
    logical_cores: int
    physical_cores: int
    sockets: Optional[int]
    process_count: int
    thread_count: int
    uptime_seconds: float
    virtualization_enabled: Optional[bool]
    l1_cache_kb: CacheInfo
    l2_cache_mb: CacheInfo
    l3_cache_mb: CacheInfo
    per_core: List[CPUCoreModel]
    topology: SystemTopologyModel


# ================= MEMORY =================


class MemoryModel(BaseModel):
    total_virtual_memory_gb: float
    used_virtual_memory_gb: float
    available_virtual_memory_gb: float
    virtual_memory_usage_percent: float
    total_swap_memory_gb: float
    used_swap_memory_gb: float
    available_swap_memory_gb: float
    swap_memory_usage_percent: float


# ================= DISK =================


class DiskModel(BaseModel):
    mountpoint: str
    total_gb: float
    used_gb: float
    free_gb: float
    usage_percent: float


# ================= GPU =================


class GPUDeviceModel(BaseModel):
    name: Optional[str]
    vendor: Optional[str]

    driver_version: Optional[str]

    # Compute stack (flat)
    cuda_version: Optional[str] = None
    rocm_version: Optional[str] = None
    metal_version: Optional[str] = None

    # Memory
    vram_total_mb: Optional[ByteValueModel]
    vram_used_mb: Optional[ByteValueModel]
    vram_free_mb: Optional[ByteValueModel]

    # Telemetry
    utilization_percent: Optional[float]
    temperature_c: Optional[int]

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(*args, **kwargs)


class GPUModel(BaseModel):
    devices: List[GPUDeviceModel]


# ================= NETWORK =================


class LatencyModel(BaseModel):
    value: Optional[float] = None
    unit: str = "ms"
    status: Literal["ok", "unreachable", "unparseable"]
    target: str


class NetworkInterfaceModel(BaseModel):
    name: str
    is_up: Optional[bool]
    speed_mbps: Optional[int]
    mtu: Optional[int]
    ip_v4: Optional[str]
    ip_v6: Optional[str]


class NetworkModel(BaseModel):
    bytes_sent: ByteValueModel
    bytes_recv: ByteValueModel
    packets_sent: int
    packets_recv: int
    errors_in: int
    errors_out: int
    interfaces: List[NetworkInterfaceModel]
    latency: LatencyModel
    source: str
    platform: str


# ================= SYSTEM =================


class SystemModel(BaseModel):
    os: str
    release: str
    machine: str
    processor: str


# ================= ALL =================


class SystemResourcesModel(BaseModel):
    cpu: CPUModel
    memory: MemoryModel
    disk: List[DiskModel]
    gpu: GPUModel
    network: NetworkModel
    system: SystemModel


# ================= System Capabilities =================
class CPUCapabilitiesModel(BaseModel):
    model_name: bool
    architecture: bool
    per_core_usage: bool
    topology_detection: bool
    socket_detection: bool
    cache_detection: bool


class MemoryCapabilitiesModel(BaseModel):
    virtual_memory: bool
    swap_memory: bool
    detailed_breakdown: bool


class DiskCapabilitiesModel(BaseModel):
    partition_usage: bool
    io_counters: bool


class NetworkCapabilitiesModel(BaseModel):
    interface_detection: bool
    link_speed: bool
    latency_probe: bool
    external_ping: bool


class GPUCapabilitiesModel(BaseModel):
    nvidia_smi: bool
    rocm_smi: bool
    directx: bool
    metal: bool
    driver_version: bool
    compute_stack_version: bool


class ReliabilityModel(BaseModel):
    cpu_topology: Literal["accurate", "estimated", "unknown"]
    gpu_detection: Literal["accurate", "vendor_dependent", "limited"]
    network_latency: Literal["accurate", "active_probe"]


class SystemCapabilitiesModel(BaseModel):
    platform: str
    cpu: CPUCapabilitiesModel
    memory: MemoryCapabilitiesModel
    disk: DiskCapabilitiesModel
    network: NetworkCapabilitiesModel
    gpu: GPUCapabilitiesModel
    reliability: ReliabilityModel
