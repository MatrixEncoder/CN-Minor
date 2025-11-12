"""
Simple Network Topology Example
"""
from network_simulator.network import NetworkTopology
from network_simulator.device import Router, Switch, Host

def main():
    # Create a new network
    print("Creating a simple network...")
    network = NetworkTopology("Simple Network")
    
    # Create devices
    router = Router("R1")
    switch = Switch("SW1")
    pc1 = Host("PC1")
    pc2 = Host("PC2")
    
    # Add devices to network
    for device in [router, switch, pc1, pc2]:
        network.add_device(device)
    
    # Connect devices
    network.connect_devices("R1", "eth0", "SW1", "eth1")
    network.connect_devices("SW1", "eth2", "PC1", "eth0")
    network.connect_devices("SW1", "eth3", "PC2", "eth0")
    
    # Draw the network
    output_file = "simple_network.png"
    print(f"Drawing network topology to {output_file}")
    network.draw_topology(output_file)
    
    # Show some information
    print("\nNetwork Devices:")
    for name, device in network.devices.items():
        print(f"- {name} ({device.device_type})")
    
    print("\nNetwork Connections:")
    for src, dst, data in network.graph.edges(data=True):
        print(f"{src} --[{data.get('bandwidth', 100)}Mbps]--> {dst}")
    
    print("\nDone! Check the generated image file.")

if __name__ == "__main__":
    main()
