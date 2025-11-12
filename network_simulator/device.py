class Device:
    def __init__(self, name, device_type, **kwargs):
        self.name = name
        self.device_type = device_type
        self.interfaces = {}
        self.attributes = kwargs
        
    def add_interface(self, interface_name, **kwargs):
        """Add a network interface to the device."""
        self.interfaces[interface_name] = {
            'status': 'down',  # 'up' or 'down'
            'ip_address': None,
            'subnet_mask': None,
            'mac_address': None,
            **kwargs
        }
    
    def set_interface_status(self, interface_name, status):
        """Set the status of an interface (up/down)."""
        if interface_name in self.interfaces:
            if status.lower() in ['up', 'down']:
                self.interfaces[interface_name]['status'] = status.lower()
                return True
        return False
    
    def __str__(self):
        """String representation of the device."""
        return f"{self.device_type.upper()}: {self.name}"


class Router(Device):
    """Router network device."""
    
    def __init__(self, name, **kwargs):
        super().__init__(name, 'router', **kwargs)
        self.routing_table = {}
    
    def add_route(self, network, next_hop, interface, metric=1):
        """Add a route to the routing table."""
        self.routing_table[network] = {
            'next_hop': next_hop,
            'interface': interface,
            'metric': metric
        }


class Switch(Device):
    """Switch network device."""
    
    def __init__(self, name, **kwargs):
        super().__init__(name, 'switch', **kwargs)
        self.mac_table = {}  # MAC address to port mapping
    
    def learn_mac(self, mac_address, port):
        """Learn a MAC address on a specific port."""
        self.mac_table[mac_address] = port


class Host(Device):
    """Host (end device) network device."""
    
    def __init__(self, name, **kwargs):
        super().__init__(name, 'host', **kwargs)
        self.running_processes = []
    
    def start_process(self, process_name, **kwargs):
        """Start a network process on the host."""
        self.running_processes.append({
            'name': process_name,
            'status': 'running',
            **kwargs
        })
