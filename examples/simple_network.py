#!/usr/bin/env python3
"""
Enhanced Network Topology Example with IP Addressing
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from network_simulator.network import NetworkTopology
from network_simulator.device import Router, Switch, Host

def create_simple_network():
    """
    Create a network topology with 2 routers, 2 switches, and 4 hosts.
    Implements IP addressing with proper subnetting.
    """
    # Create a new network
    network = NetworkTopology("Enterprise Network with IP Addressing")
    
    # ===== Create Devices =====
    # Routers (Layer 3 devices)
    router1 = Router("R1")
    router2 = Router("R2")
    
    # Switches (Layer 2 devices)
    switch1 = Switch("SW1")
    switch2 = Switch("SW2")
    
    # End Devices
    pc1 = Host("PC1")
    pc2 = Host("PC2")
    server1 = Host("WebServer")
    server2 = Host("DBServer")
    
    # Add all devices to the network
    for device in [router1, router2, switch1, switch2, pc1, pc2, server1, server2]:
        network.add_device(device)
    
    # ===== Network Segments =====
    # - 192.168.1.0/24: R1's LAN (PC1, PC2)
    # - 192.168.2.0/24: R2's LAN (WebServer, DBServer)
    # - 10.0.0.0/30: Point-to-point link between R1 and R2
    
    # ===== Connect Devices =====
    # 1. Connect R1 and R2 (WAN link)
    network.connect_devices(
        "R1", "eth0", 
        "R2", "eth0", 
        bandwidth=1000,  # 1Gbps link
        description="WAN Link"
    )
    
    # 2. Connect R1 to SW1 (LAN 1)
    network.connect_devices(
        "R1", "eth1", 
        "SW1", "eth0", 
        bandwidth=1000,
        description="LAN 1 Uplink"
    )
    
    # 3. Connect R2 to SW2 (LAN 2)
    network.connect_devices(
        "R2", "eth1", 
        "SW2", "eth0", 
        bandwidth=1000,
        description="LAN 2 Uplink"
    )
    
    # 4. Connect hosts to SW1 (LAN 1)
    network.connect_devices(
        "SW1", "eth1", 
        "PC1", "eth0", 
        bandwidth=100,
        description="PC1 Connection"
    )
    
    network.connect_devices(
        "SW1", "eth2", 
        "PC2", "eth0", 
        bandwidth=100,
        description="PC2 Connection"
    )
    
    # 5. Connect servers to SW2 (LAN 2)
    network.connect_devices(
        "SW2", "eth1", 
        "WebServer", "eth0", 
        bandwidth=1000,
        description="Web Server Connection"
    )
    
    network.connect_devices(
        "SW2", "eth2", 
        "DBServer", "eth0", 
        bandwidth=1000,
        description="Database Server Connection"
    )
    
    return network

def main():
    network = create_simple_network()
    
    print("Network created successfully!")
    print(f"{network}")
    print(f"Number of devices: {len(network.devices)}")
    print(f"Number of links: {network.graph.number_of_edges()}")
    
    path = network.get_shortest_path("PC1", "WebServer")
    print(f"\nPath from PC1 to WebServer: {' -> '.join(path)}")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "network_topology.png"
    
    print(f"\nGenerating network visualization: {output_file}")
    network.draw_topology(str(output_file))
    
    print("\nSimulation complete!")

if __name__ == "__main__":
    main()
