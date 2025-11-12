# Network Topology Simulator Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Advanced Usage](#advanced-usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Testing](#testing)
9. [Contributing](#contributing)

## Project Overview
This project simulates computer networks with routers, switches, and hosts. It provides visualization and simulation capabilities for network analysis.

## Installation
```bash
git clone https://github.com/MatrixEncoder/CN-Minor.git
cd network-topology-simulator
pip install -r requirements.txt
```

## Quick Start
```python
from network_simulator import NetworkTopology, Router, Switch, Host

# Create network
network = NetworkTopology("My Network")

# Add devices
r1 = Router("R1")
sw1 = Switch("SW1"
pc1 = Host("PC1")

network.add_device(r1)
network.add_device(sw1)
network.add_device(pc1)

# Connect devices
network.connect_devices("R1", "eth0", "SW1", "eth1")
network.connect_devices("SW1", "eth2", "PC1", "eth0")

# Visualize
network.draw_topology("network.png")
```

## Core Concepts
- **Devices**: Routers, switches, and hosts
- **Interfaces**: Network interfaces with IP configuration
- **Links**: Connections between devices
- **Topology**: The overall network structure

## Advanced Usage
See `examples/advanced_network.py` for more complex scenarios.

## API Reference
Detailed API documentation is available in the code docstrings.

## Examples
Check the `examples/` directory for various use cases.

## Testing
Run tests with:
```bash
python -m pytest tests/
```

## Contributing
Contributions are welcome! Please follow the standard fork and pull request workflow.
