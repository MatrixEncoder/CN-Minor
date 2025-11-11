#!/usr/bin/env python3
"""
Simple Network Topology Example
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from network_simulator.network import NetworkTopology
from network_simulator.device import Router, Switch, Host

def create_simple_network():
    """Create a simple network topology with 2 routers, 2 switches, and 4 hosts."""
    # Create a new network
    network = NetworkTopology("Simple Enterprise Network")
    
    # Create devices
    # Routers
    router1 = Router("R1")
    router2 = Router("R2")
    
    # Switches
    switch1 = Switch("SW1")
    switch2 = Switch("SW2")
    
    # Hosts
    pc1 = Host("PC1")
    pc2 = Host("PC2")
    server1 = Host("Server1")
    server2 = Host("Server2")
    
    # Add devices to the network
    for device in [router1, router2, switch1, switch2, pc1, pc2, server1, server2]:
        network.add_device(device)
    
    # Connect devices
    # Router to router connection
    network.connect_devices("R1", "eth0", "R2", "eth0", bandwidth=1000)  # 1Gbps link
    
    # Connect routers to switches
    network.connect_devices("R1", "eth1", "SW1", "eth0", bandwidth=1000)
    network.connect_devices("R2", "eth1", "SW2", "eth0", bandwidth=1000)
    
    # Connect hosts to switches
    network.connect_devices("SW1", "eth1", "PC1", "eth0", bandwidth=100)
    network.connect_devices("SW1", "eth2", "PC2", "eth0", bandwidth=100)
    network.connect_devices("SW2", "eth1", "Server1", "eth0", bandwidth=1000)
    network.connect_devices("SW2", "eth2", "Server2", "eth0", bandwidth=1000)
    
    return network

def main():
    """Main function to demonstrate the network."""
    # Create the network
    network = create_simple_network()
    
    # Print network information
    print("Network created successfully!")
    print(f"{network}")
    print(f"Number of devices: {len(network.devices)}")
    print(f"Number of links: {network.graph.number_of_edges()}")
    
    # Find a path between two hosts
    path = network.get_shortest_path("PC1", "Server1")
    print(f"\nPath from PC1 to Server1: {' -> '.join(path)}")
    
    # Visualize the network
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "network_topology.png"
    
    print(f"\nGenerating network visualization: {output_file}")
    network.draw_topology(str(output_file))
    
    print("\nSimulation complete!")

if __name__ == "__main__":
    main()
