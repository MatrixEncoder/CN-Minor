# Network Topology Simulator

A Python-based network topology simulator for creating and visualizing computer networks. This project provides a simple yet powerful way to model network topologies with routers, switches, and hosts.

## Features

- Create and manage network devices (routers, switches, hosts)
- Connect devices with configurable interfaces
- Automatic IP address assignment
- Visualize network topology with device details
- Hierarchical layout for better visualization
- Basic network simulation capabilities

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MatrixEncoder/CN-Minor.git
   cd CN-Minor
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

Run the simple example to see a basic network topology:

```bash
python simple_example.py
```

This will generate a visualization of a simple network with 1 router, 1 switch, and 2 hosts.

## Examples

Check the `examples/` directory for more complex network configurations:

```bash
python examples/simple_network.py
```

## Project Structure

```
network_simulator/
├── __init__.py     # Package initialization
├── device.py      # Device classes (Router, Switch, Host)
├── network.py     # Network topology management
└── simulation.py  # Network simulation logic

examples/          # Example scripts
└── simple_network.py

tests/             # Unit tests
└── test_network.py
```

## Requirements

- Python 3.6+
- networkx
- matplotlib
- numpy

## Running Tests

To run the test suite:

```bash
python -m pytest tests/
```

Or use the run script:
```bash
python scripts/run_simulator.py
```

### Basic Commands

- `new <name>` - Create a new network
- `add <type> <name>` - Add a device (router/switch/host)
- `connect <dev1> <if1> <dev2> <if2> [bandwidth]` - Connect devices
- `ping <source> <destination> [count]` - Test connectivity
- `show [devices|topology|routes]` - View network information
- `draw [filename]` - Save network diagram
- `save/load <file>` - Save/load network configuration
- `exit` or `quit` - Exit the CLI

### Example Session

```
net-sim> new my_network
net-sim> add router R1
net-sim> add switch SW1
net-sim> add host PC1
net-sim> connect R1 eth0 SW1 eth1 1000
net-sim> connect SW1 eth2 PC1 eth0 100
net-sim> show devices
net-sim> ping PC1 R1
net-sim> draw my_network.png
net-sim> save my_network.json
```

## Project Structure

```
network-simulator/
├── network_simulator/     # Core package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py            # Command-line interface
│   ├── device.py         # Device classes
│   ├── network.py        # Network topology
│   └── simulation.py     # Simulation logic
├── examples/             # Example scripts
│   └── simple_network.py
├── scripts/              # Utility scripts
│   └── run_simulator.py
├── tests/                # Unit tests
│   └── test_network.py
├── output/               # Generated files
├── DOCUMENTATION.md      # Detailed documentation
├── README.md             # This file
└── setup.py              # Package configuration
```

## Running Tests

```bash
python -m pytest tests/
```

## License

I built this, from scratch :D
Unlicensed
