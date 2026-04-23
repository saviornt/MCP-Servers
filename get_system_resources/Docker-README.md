# get-system-resources

[![Docker Pulls](https://img.shields.io/docker/pulls/davidwadsworth80/get-system-resources)](https://hub.docker.com/r/davidwadsworth80/get-system-resources)

A cross-platform Model Context Protocol (MCP) server that provides comprehensive system resource inspection capabilities. This Docker container delivers on-demand snapshots of CPU, memory, disk, GPU, and network status, making it ideal for diagnostics, monitoring, and troubleshooting across different operating systems.

## Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux hosts
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

## Quick Start

### Quick Start with MCP

1. Open your MCP client's configuration file (e.g., `mcp.json`)
2. Add the following entry to register the `get-system-resources` server:

```json
{
  "mcpServers": {
    "get-system-resources": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--privileged", "--pid=host", "--gpus", "all", "--network=host", "davidwadsworth80/get-system-resources:latest"]
    }
  }
}
```

> **GPU Support**: Add `--gpus all` if you want the `get_gpu()` tool to detect NVIDIA/AMD GPUs on the host. This is required on Docker Desktop (including WSL2).

3. Save the configuration and start your MCP client. The `get-system-resources` server will now be available for use.
4. Ask your tools-usage-capable assistant to find out how much free memory you have, or your system information, or any other system resource details!

### Pull the Image

```bash
docker pull ghcr.io/saviornt/mcp-servers/get-system-resources:latest
```

### Run the Container

To run the MCP server in a container with access to host system resources:

```bash
docker run --rm -it \
  --privileged \
  --pid=host \
  --gpus all \
  --network=host \
  ghcr.io/saviornt/mcp-servers/get-system-resources:latest
```

> **Note**: The `--privileged`, `--pid=host`, `--gpus`, `all`, and `--network=host` flags are required for the container to access system resources like CPU, memory, disk, and network information.
> **GPU Support**: Add `--gpus all` if you want the `get_gpu()` tool to detect NVIDIA/AMD GPUs on the host. This is required on Docker Desktop (including WSL2).

## Usage

The container runs the MCP server, which provides the following tools:

- `get_cpu()`: Detailed CPU information
- `get_memory()`: Memory statistics
- `get_disk()`: Disk usage information
- `get_gpu()`: GPU device information
- `get_network()`: Network interface details
- `get_system()`: General system information
- `get_all()`: Comprehensive snapshot of all resources
- `get_capabilities()`: System monitoring capabilities
- `get_version()`: Server version

Integrate this container with MCP-compatible clients such as Claude Desktop or other MCP-enabled applications.

### MCP Configuration

To add this server to your MCP client's configuration, add the following entry to your `mcp.json` file:

```json
{
  "mcpServers": {
    "get-system-resources": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--privileged", "--pid=host", "--gpus", "all", "--network=host", "ghcr.io/saviornt/mcp-servers/get-system-resources:latest"]
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
      "args": ["run", "--rm", "-i", "--privileged", "--pid=host","--gpus", "all",  "--network=host", "davidwadsworth80/get-system-resources:latest"]
    }
  }
}
```

> **GPU Support**: Add `--gpus all` if you want the `get_gpu()` tool to detect NVIDIA/AMD GPUs on the host. This is required on Docker Desktop (including WSL2).

## Configuration

No additional configuration is required. The server automatically detects available system resources.

## Requirements

- Docker
- Host system with supported OS (Windows, macOS, Linux)

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/yourusername/get-system-resources).

## License

This project is licensed under the Apache License 2.0.
