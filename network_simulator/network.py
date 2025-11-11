import networkx as nx
import matplotlib.pyplot as plt
from .device import Device

class NetworkTopology:
    """Class representing a network topology."""
    
    def __init__(self, name):
        """Initialize an empty network topology."""
        self.name = name
        self.graph = nx.Graph()
        self.devices = {}
    
    def add_device(self, device):
        """Add a device to the network."""
        if not isinstance(device, Device):
            raise ValueError("Device must be an instance of Device class")
        
        if device.name in self.devices:
            raise ValueError(f"Device with name '{device.name}' already exists")
        
        self.devices[device.name] = device
        self.graph.add_node(device.name, device=device, type=device.device_type)
    
    def remove_device(self, device_name):
        """Remove a device from the network."""
        if device_name in self.devices:
            self.graph.remove_node(device_name)
            del self.devices[device_name]
    
    def connect_devices(self, device1_name, interface1, device2_name, interface2, **link_attrs):
        """
        Connect two devices with a network link.
        
        Args:
            device1_name: Name of the first device
            interface1: Interface name on the first device
            device2_name: Name of the second device
            interface2: Interface name on the second device
            **link_attrs: Additional link attributes (e.g., bandwidth, delay)
        """
        if device1_name not in self.devices or device2_name not in self.devices:
            raise ValueError("Both devices must exist in the network")
        
        # Update device interfaces
        self.devices[device1_name].add_interface(interface1, connected_to=device2_name)
        self.devices[device2_name].add_interface(interface2, connected_to=device1_name)
        
        # Add edge to the graph
        self.graph.add_edge(
            device1_name, 
            device2_name, 
            interface1=interface1,
            interface2=interface2,
            **link_attrs
        )
    
    def get_shortest_path(self, source, target):
        """Get the shortest path between two devices."""
        try:
            return nx.shortest_path(self.graph, source=source, target=target)
        except nx.NetworkXNoPath:
            return None
    
    def draw_topology(self, filename=None):
        """Visualize the network topology."""
        plt.figure(figsize=(12, 8))
        
        # Define node colors based on device type
        node_colors = []
        for node in self.graph.nodes():
            device_type = self.graph.nodes[node].get('type', 'unknown')
            if device_type == 'router':
                node_colors.append('lightblue')
            elif device_type == 'switch':
                node_colors.append('lightgreen')
            elif device_type == 'host':
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightgray')
        
        # Draw the graph
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
        nx.draw_networkx_nodes(
            self.graph, 
            pos, 
            node_size=1000,
            node_color=node_colors,
            alpha=0.9
        )
        
        # Draw edges with labels
        edge_labels = {(u, v): f"{self.graph.edges[u, v].get('interface1', '')}-{self.graph.edges[u, v].get('interface2', '')}" 
                      for u, v in self.graph.edges()}
        
        nx.draw_networkx_edges(self.graph, pos, width=1.5, alpha=0.6)
        nx.draw_networkx_edge_labels(
            self.graph, 
            pos, 
            edge_labels=edge_labels,
            font_size=8
        )
        
        # Draw node labels
        nx.draw_networkx_labels(
            self.graph, 
            pos, 
            {n: f"{n}\n({self.graph.nodes[n].get('type', '?')})" 
             for n in self.graph.nodes()},
            font_size=10
        )
        
        plt.title(f"Network Topology: {self.name}")
        plt.axis('off')
        
        if filename:
            plt.savefig(filename, format='PNG', dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def get_device(self, device_name):
        """Get a device by name."""
        return self.devices.get(device_name)
    
    def __str__(self):
        """String representation of the network."""
        return f"Network '{self.name}' with {len(self.devices)} devices and {self.graph.number_of_edges()} links"
