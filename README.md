# SaviorNT's MCP Servers

A mono-repository containing various Model Context Protocol (MCP) servers that provide specialized tools and integrations for AI assistants and applications. Each subdirectory represents a separate MCP server project with its own functionality and dependencies.

## Projects

### get-system-resources

A cross-platform MCP server for comprehensive system resource monitoring and diagnostics.

**Features:**

- Real-time CPU, memory, disk, GPU, and network monitoring
- Cross-platform support (Windows, macOS, Linux)
- Support for NVIDIA, AMD, and Apple Silicon GPUs
- Structured data output using Pydantic models

**Installation:**

```bash
cd get_system_resources
pip install -e .
```

**Usage:**

```bash
python -m get_system_resources.server
```

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd MCP-Servers
   ```

2. **Choose a server project** and navigate to its directory

3. **Install dependencies** (each project has its own requirements):

   ```bash
   pip install -e .
   ```

4. **Run the MCP server:**

   ```bash
   python -m <project_name>.server
   ```

## MCP Integration

These servers are designed to work with MCP-compatible clients such as:

- Claude Desktop with MCP support
- LM Studio with MCP integration
- Other MCP-enabled AI applications
- Custom MCP clients

Each server provides tools that can be invoked by MCP clients to perform specific tasks.

## Project Structure

```text
MCP-Servers/
├── get_system_resources/     # System resource monitoring server
│   ├── server.py
│   ├── models.py
│   ├── collectors/
│   └── ...
├── LICENSE                   # Apache 2.0 license
├── README.md                 # This file
└── .gitignore                # Python project ignore patterns
```

## Development

### Adding a New MCP Server

1. Create a new directory for your server project
2. Implement the MCP server using FastMCP or compatible framework
3. Add appropriate documentation and tests
4. Update this README to include your new project

### Requirements

- Python 3.10+
- MCP-compatible client for testing
- Platform-specific dependencies (e.g., GPU drivers for monitoring servers)

## Contributing

1. Fork the repository
2. Create a feature branch for your changes
3. Follow the existing code style and patterns
4. Add tests for new functionality
5. Update documentation as needed
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions related to specific servers, please check the individual project directories for more detailed documentation and issue trackers.
