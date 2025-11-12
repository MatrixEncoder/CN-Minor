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
    
    def _generate_ip_address(self, base_network, host_num):
        base_parts = list(map(int, base_network.split('.')))
        base_parts[3] += host_num
        return '.'.join(map(str, base_parts))

    def draw_topology(self, filename=None):
        """
        Draw an enhanced network topology visualization with improved styling.
        
        Args:
            filename (str, optional): If provided, saves the plot to the specified file.
        """
        plt.figure(figsize=(14, 10))
        plt.style.use('default')  # Use default style for better compatibility
        plt.rcParams['figure.facecolor'] = 'white'  # Set white background
        
        # Define network segments and their base IPs
        network_segments = {
            'R1-SW1': '192.168.1.0',
            'R2-SW2': '192.168.2.0',
            'R1-R2': '10.0.0.0',
            'SW1-PC1': '192.168.1.0',
            'SW1-PC2': '192.168.1.0',
            'SW2-WebServer': '192.168.2.0',
            'SW2-DBServer': '192.168.2.0'
        }
        
        # Define device type styling
        device_styles = {
            'router': {
                'color': '#FF6B6B',  # Coral red
                'shape': 's',        # Square
                'size': 1500,
                'edgecolor': '#CC0000',
                'linewidth': 2
            },
            'switch': {
                'color': '#4ECDC4',  # Turquoise
                'shape': 'h',        # Hexagon
                'size': 1200,
                'edgecolor': '#1A7F7A',
                'linewidth': 1.5
            },
            'host': {
                'color': '#A5D8A2',  # Light green
                'shape': '^',        # Triangle up
                'size': 1000,
                'edgecolor': '#3D8B37',
                'linewidth': 1.5
            },
            'default': {
                'color': '#D3D3D3',  # Light gray
                'shape': 'o',        # Circle
                'size': 800,
                'edgecolor': '#A9A9A9',
                'linewidth': 1
            }
        }
        
        # Prepare node data
        node_data = {}
        for node in self.graph.nodes():
            device_type = self.graph.nodes[node].get('type', 'unknown').lower()
            device = self.graph.nodes[node].get('device')
            
            # Get style for this device type
            style = device_styles.get(device_type, device_styles['default'])
            
            # Build node label
            label_parts = [f"{node} ({device_type.upper()})"]
            
            # Add IP addresses if available
            if device and hasattr(device, 'interfaces'):
                for iface, config in device.interfaces.items():
                    if 'ip_address' in config and config['ip_address']:
                        subnet = config.get('subnet_mask', '24')
                        label_parts.append(f"{iface}: {config['ip_address']}/{subnet}")
            
            node_data[node] = {
                'style': style,
                'label': '\n'.join(label_parts),
                'type': device_type
            }
        
        # Create a hierarchical layout
        pos = {}  # Position dictionary
        level_height = 0
        levels = {
            'router': 0,
            'switch': 1,
            'host': 2,
            'default': 3
        }
        
        # Group nodes by type
        nodes_by_type = {}
        for node, data in node_data.items():
            node_type = data['type']
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)
        
        # Position nodes in hierarchical levels
        for node_type in ['router', 'switch', 'host', 'default']:
            if node_type in nodes_by_type:
                level_nodes = nodes_by_type[node_type]
                level_width = 1.0 / (len(level_nodes) + 1)
                
                for i, node in enumerate(level_nodes):
                    x = (i + 1) * level_width
                    y = 1.0 - (levels.get(node_type, 3) * 0.3)
                    pos[node] = (x, y)
        
        # Adjust layout for better spacing
        pos = nx.spring_layout(self.graph, pos=pos, k=0.8, iterations=50)
        
        # Draw edges with bandwidth labels
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            # Generate IPs for this connection
            segment_key = f"{u}-{v}" if f"{u}-{v}" in network_segments else f"{v}-{u}"
            base_network = network_segments.get(segment_key, '10.0.0.0')
            
            # Get interface names
            iface1 = data.get('interface1', 'eth0')
            iface2 = data.get('interface2', 'eth0')
            
            # Assign IPs based on device types
            if node_data[u]['type'] == 'router' or node_data[v]['type'] == 'router':
                # Router connections
                if node_data[u]['type'] == 'router':
                    router, switch = u, v
                    ip1 = f"{base_network}.1"
                    ip2 = f"{base_network}.2"
                else:
                    router, switch = v, u
                    ip1 = f"{base_network}.2"
                    ip2 = f"{base_network}.1"
                
                # Update device interfaces
                if self.graph.nodes[u].get('device'):
                    self.graph.nodes[u]['device'].add_interface(iface1, 
                                                              ip_address=ip1,
                                                              subnet_mask='24',
                                                              status='up')
                
                if self.graph.nodes[v].get('device'):
                    self.graph.nodes[v]['device'].add_interface(iface2,
                                                              ip_address=ip2,
                                                              subnet_mask='24',
                                                              status='up')
                
                edge_labels[(u, v)] = f"{iface1}: {ip1}/24\n{iface2}: {ip2}/24"
            else:
                # Host connections
                host = u if node_data[u]['type'] == 'host' else v
                switch = v if host == u else u
                host_num = 10 + len([n for n in self.graph.neighbors(switch) 
                                   if node_data.get(n, {}).get('type') == 'host' and n != host])
                
                if self.graph.nodes[host].get('device'):
                    ip = f"{base_network.split('.')[0]}.{base_network.split('.')[1]}.{base_network.split('.')[2]}.{host_num}"
                    self.graph.nodes[host]['device'].add_interface('eth0',
                                                                 ip_address=ip,
                                                                 subnet_mask='24',
                                                                 status='up')
                    edge_labels[(u, v)] = f"eth0: {ip}/24"
        
        # Draw edges with different styles
        for u, v, data in self.graph.edges(data=True):
            edge_color = '#888888'
            edge_style = 'solid'
            edge_width = 1.5
            
            # Style router connections differently
            if node_data[u]['type'] == 'router' or node_data[v]['type'] == 'router':
                edge_color = '#FF6B6B'  # Match router color
                edge_width = 2.5
            
            nx.draw_networkx_edges(
                self.graph, 
                pos, 
                edgelist=[(u, v)],
                width=edge_width,
                alpha=0.8,
                edge_color=edge_color,
                style=edge_style,
                arrows=False
            )
        
        # Draw nodes with individual styling
        for node, data in node_data.items():
            nx.draw_networkx_nodes(
                self.graph,
                pos,
                nodelist=[node],
                node_size=data['style']['size'],
                node_color=data['style']['color'],
                node_shape=data['style']['shape'],
                edgecolors=data['style']['edgecolor'],
                linewidths=data['style']['linewidth'],
                alpha=0.9
            )
        
        # Draw edge labels with better formatting
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            font_weight='normal',
            bbox=dict(
                facecolor='white',
                edgecolor='none',
                alpha=0.85,
                boxstyle='round,pad=0.2',
                linewidth=0.5
            )
        )
        
        # Draw node labels with improved formatting
        for node, (x, y) in pos.items():
            plt.text(
                x, y + 0.02,  # Slight vertical offset
                node_data[node]['label'],
                horizontalalignment='center',
                verticalalignment='bottom',
                fontsize=9,
                fontweight='bold',
                bbox=dict(
                    facecolor='white',
                    edgecolor='#DDDDDD',
                    alpha=0.8,
                    boxstyle='round,pad=0.3',
                    linewidth=0.5
                )
            )
        
        # Add title and subtitle
        plt.suptitle(
            f"Network Topology: {self.name}",
            fontsize=16,
            fontweight='bold',
            y=0.98
        )
        
        plt.title(
            "IP Addressing Scheme: Class C Private Networks | Line: Solid=Router, Dashed=Switch",
            fontsize=10,
            color='#666666'
        )
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], 
                      marker='s', color='w', 
                      label='Router',
                      markerfacecolor='#FF6B6B',
                      markersize=12,
                      markeredgecolor='#CC0000',
                      markeredgewidth=1.5),
            plt.Line2D([0], [0],
                      marker='h', color='w',
                      label='Switch',
                      markerfacecolor='#4ECDC4',
                      markersize=12,
                      markeredgecolor='#1A7F7A',
                      markeredgewidth=1.5),
            plt.Line2D([0], [0],
                      marker='^', color='w',
                      label='Host',
                      markerfacecolor='#A5D8A2',
                      markersize=12,
                      markeredgecolor='#3D8B37',
                      markeredgewidth=1.5)
        ]
        
        legend = plt.legend(
            handles=legend_elements,
            loc='upper right',
            frameon=True,
            framealpha=0.9,
            edgecolor='#DDDDDD',
            title='Device Types',
            title_fontsize=10
        )
        legend.get_frame().set_linewidth(0.5)
        
        # Remove axis
        plt.axis('off')
        plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust for suptitle
        
        # Save or show the plot
        if filename:
            plt.savefig(
                filename,
                dpi=300,
                bbox_inches='tight',
                facecolor='white'
            )
            print(f"Network topology saved to {filename}")
        else:
            plt.show()
    
    def get_device(self, device_name):
        """Get a device by name."""
        return self.devices.get(device_name)
    
    def __str__(self):
        """String representation of the network."""
        return f"Network '{self.name}' with {len(self.devices)} devices and {self.graph.number_of_edges()} links"
