# get-system-resources

A cross-platform Model Context Protocol (MCP) server that provides comprehensive system resource inspection capabilities. This tool delivers on-demand snapshots of CPU, memory, disk, GPU, and network status, making it ideal for diagnostics, monitoring, and troubleshooting across different operating systems.

## Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Comprehensive Resource Monitoring**:
  - CPU utilization, core details, and topology
  - Memory usage (virtual and swap)
  - Disk space and usage statistics
  - GPU information (NVIDIA, AMD, Apple Silicon)
  - Network interfaces and traffic
  - System information
- **MCP Integration**: Built with FastMCP for seamless integration with MCP-compatible clients
- **Real-time Data**: Provides current system resource snapshots
- **Structured Output**: Returns well-typed, structured data using Pydantic models

## Installation

### Prerequisites

- Python 3.10 or higher

### Install from Source

1. Clone or download the repository
2. Navigate to the project directory
3. Create a virtual environment:

  ```bash
  python -m venv .venv
  ```

4. Activate the virtual environment:

   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

5. Install the package:

  ```bash
  pip install -e .
  ```

## Usage

### Running the MCP Server

Start the server using Python:

```bash
python -m get_system_resources.server
```

Or directly:

```bash
python get_system_resources/server.py
```

### Available Tools

The server provides the following MCP tools:

#### `get_cpu()`

Returns detailed CPU information including:

- Utilization percentage
- Core count (physical and logical)
- Frequency information
- Per-core utilization
- Cache information
- Virtualization status

#### `get_memory()`

Returns memory statistics:

- Total, used, and available virtual memory
- Swap memory details
- Memory usage percentages

#### `get_disk()`

Returns disk information for all mounted partitions:

- Total, used, and free space
- Usage percentages
- Mount points

#### `get_gpu()`

Returns GPU device information:

- Vendor and model
- Driver versions
- VRAM usage (total, used, free)
- Utilization percentage
- Temperature (where available)
- Supports NVIDIA, AMD, and Apple Silicon GPUs

#### `get_network()`

Returns network interface details:

- Interface names and status
- IP addresses (IPv4 and IPv6)
- Speed and MTU
- Traffic statistics (bytes sent/received)
- Packet counts and errors

#### `get_system()`

Returns general system information:

- Operating system details
- Architecture
- Processor information

#### `get_all()`

Returns a comprehensive snapshot of all system resources in a single call.

#### `get_capabilities()`

Returns information about what system monitoring features are available on the current platform.

#### `get_version()`

Returns the version of the server.

### Integration with MCP Clients

This server is designed to work with MCP-compatible clients such as:

- Claude Desktop with MCP support
- LM Studio with MCP integration
- Other MCP-enabled applications

Configure your MCP client to connect to this server for system monitoring capabilities.

### MCP Configuration

To add this server to your MCP client's configuration, add the following entry to your `mcp.json` file:

```json
{
  "mcpServers": {
    "get-system-resources": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--privileged", "--pid=host", "--network=host", "ghcr.io/saviornt/mcp-servers/get-system-resources:latest"]
    }
  }
}
```

Alternatively, you can use the Docker Hub image:

```json
{
  "mcpServers": {
    "get-system-resources": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--privileged", "--pid=host", "--network=host", "davidwadsworth80/get-system-resources:latest"]
    }
  }
}
```

## Configuration

The server automatically detects available system resources and adapts its behavior based on the platform:

- **Windows**: Full support for all features
- **macOS**: Full support including Apple Silicon GPU detection
- **Linux**: Full support with AMD GPU detection via ROCm

No additional configuration is required for basic operation.

## Development

### Project Structure

```text
get_system_resources/
├── server.py              # Main MCP server implementation
├── models.py              # Pydantic data models
├── utils.py               # Utility functions
├── capabilities.py        # System capability detection
├── collectors/            # Resource collection modules
│   ├── cpu/               # CPU-specific collectors
│   ├── disk_collector.py
│   ├── gpu_collector.py
│   ├── memory_collector.py
│   ├── network_collector.py
│   └── system_collector.py
├── pyproject.toml         # Project configuration
├── LICENSE                # Apache 2.0 license
└── README.md              # This file
```

### Running Tests

```bash
python -m pytest
```

### Building

```bash
python -m build
```

## Dependencies

- **fastmcp**: MCP server framework
- **psutil**: Cross-platform system utilities
- **pydantic**: Data validation and serialization
- **nvidia-ml-py**: NVIDIA GPU monitoring
- **pyrsmi**: AMD GPU monitoring (ROCm)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please open an issue on the project's repository.

## Changelog

### v0.1.0

- Initial release
- Cross-platform system resource monitoring
- MCP server implementation
- Support for CPU, memory, disk, GPU, and network monitoring
