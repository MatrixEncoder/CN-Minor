import time
import random
import json
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from queue import Queue, PriorityQueue
from datetime import datetime

class PacketType(Enum):
    ICMP_ECHO = auto()
    ICMP_REPLY = auto()
    TCP = auto()
    UDP = auto()
    ROUTING_UPDATE = auto()

@dataclass
class Packet:
    source: str
    destination: str
    packet_type: PacketType
    payload: any = None
    ttl: int = 64
    size: int = 1500
    timestamp: float = field(default_factory=time.time)
    path: List[str] = field(default_factory=list)
    sequence: int = 0
    
    def __post_init__(self):
        self.path = [self.source]
        self.creation_time = time.time()
    
    def add_hop(self, node: str) -> bool:
        if node in self.path:
            return False
        self.path.append(node)
        self.ttl -= 1
        return self.ttl > 0
    
    def to_dict(self) -> dict:
        return {
            'source': self.source,
            'destination': self.destination,
            'type': self.packet_type.name,
            'ttl': self.ttl,
            'size': self.size,
            'path': self.path,
            'sequence': self.sequence,
            'latency': time.time() - self.creation_time
        }
    
    def __str__(self) -> str:
        return (f"Packet({self.packet_type.name}) from {self.source} to {self.destination} "
                f"TTL:{self.ttl} Size:{self.size}bytes")


class NetworkSimulation:
    """
    Advanced network simulation with routing protocols and traffic analysis.
    
    Features:
    - Packet routing with TTL
    - ICMP (Ping) simulation
    - Basic routing table management
    - Network traffic analysis
    - Packet loss and latency simulation
    """
    
    def __init__(self, network):
        self.network = network
        self.event_queue = PriorityQueue()
        self.time = 0
        self.packet_loss_rate = 0.01  # 1% packet loss
        self.latency_range = (1, 10)   # ms
        self.bandwidth = 1000  # Mbps
        self.running = False
        self.packet_counter = 0
        self.routing_tables = {}
        self.traffic_stats = {
            'sent': 0,
            'received': 0,
            'dropped': 0,
            'latency': []
        }
        self._init_routing_tables()
    
    def _init_routing_tables(self):
        """Initialize routing tables for all routers."""
        for device_name, device in self.network.devices.items():
            if device.device_type == 'router':
                self.routing_tables[device_name] = {
                    'direct': {},
                    'static': {},
                    'dynamic': {}
                }
    
    def update_routing_table(self, router_name, network, next_hop, metric=1, route_type='static'):
        """Update the routing table of a router."""
        if router_name in self.routing_tables:
            self.routing_tables[router_name][route_type][network] = {
                'next_hop': next_hop,
                'metric': metric,
                'last_updated': time.time()
            }
    
    def get_route(self, source, destination):
        """Get the best route from source to destination."""
        try:
            path = self.network.get_shortest_path(source, destination)
            if path and len(path) > 1:
                return path[1]  # Next hop
            return None
        except Exception as e:
            print(f"Routing error: {e}")
            return None
    
    def send_packet(self, packet: Packet) -> bool:
        """Send a packet through the network."""
        if not self.running:
            return False
        
        self.traffic_stats['sent'] += 1
        self.packet_counter += 1
        packet.sequence = self.packet_counter
        
        if random.random() < self.packet_loss_rate:
            self.traffic_stats['dropped'] += 1
            return False
        
        current = packet.path[-1]
        
        if current == packet.destination:
            self.traffic_stats['received'] += 1
            self.traffic_stats['latency'].append(time.time() - packet.creation_time)
            return True
        
        next_hop = self.get_route(current, packet.destination)
        if not next_hop or not packet.add_hop(next_hop):
            return False
        
        latency = random.uniform(*self.latency_range) / 1000  # Convert to seconds
        self.event_queue.put((time.time() + latency, packet))
        return True
    
    def ping(self, source: str, destination: str, count: int = 4) -> dict:
        """Simulate ICMP ping between two hosts."""
        results = {
            'source': source,
            'destination': destination,
            'transmitted': 0,
            'received': 0,
            'lost': 0,
            'times': [],
            'min': 0,
            'avg': 0,
            'max': 0,
            'mdev': 0
        }
        
        for i in range(count):
            packet = Packet(
                source=source,
                destination=destination,
                packet_type=PacketType.ICMP_ECHO,
                sequence=i+1
            )
            
            start_time = time.time()
            success = self.send_packet(packet)
            rtt = (time.time() - start_time) * 1000  # Convert to ms
            
            results['transmitted'] += 1
            if success:
                results['received'] += 1
                results['times'].append(rtt)
                print(f"64 bytes from {destination}: icmp_seq={i+1} ttl=64 time={rtt:.2f}ms")
            else:
                results['lost'] += 1
                print(f"Request timeout for icmp_seq {i+1}")
            
            time.sleep(1)  # Wait 1 second between pings
        
        # Calculate statistics
        if results['times']:
            results['min'] = min(results['times'])
            results['max'] = max(results['times'])
            results['avg'] = sum(results['times']) / len(results['times'])
            if len(results['times']) > 1:
                squared_diffs = [(x - results['avg'])**2 for x in results['times']]
                results['mdev'] = (sum(squared_diffs) / (len(results['times']) - 1)) ** 0.5
        
        print(f"\n--- {source} ping statistics ---")
        print(f"{results['transmitted']} packets transmitted, "
              f"{results['received']} received, "
              f"{results['lost']*100/results['transmitted']:.1f}% packet loss, "
              f"time {results['transmitted']*1000:.0f}ms")
        
        if results['received'] > 0:
            print(f"rtt min/avg/max/mdev = "
                  f"{results['min']:.3f}/{results['avg']:.3f}/"
                  f"{results['max']:.3f}/{results['mdev']:.3f} ms")
        
        return results
    
    def send_packet(self, source: str, destination: str, payload: any) -> Optional[Packet]:
        """
        Send a packet from source to destination.
        
        Args:
            source: Source device name
            destination: Destination device name
            payload: Packet payload
            
        Returns:
            The sent packet if successful, None if dropped
        """
        if source not in self.network.devices or destination not in self.network.devices:
            print(f"Error: Source or destination device not found")
            return None
        
        # Simulate packet loss
        if random.random() < self.packet_loss_rate:
            print(f"Packet from {source} to {destination} was lost!")
            return None
        
        # Create and return the packet
        return Packet(source, destination, payload)
    
    def start(self):
        """Start the simulation."""
        self.running = True
        print(f"Simulation started at time {self.time}")
    
    def stop(self):
        """Stop the simulation."""
        self.running = False
        print(f"Simulation stopped at time {self.time}")
    
    def run(self, duration: float):
        """
        Run the simulation for a specified duration.
        
        Args:
            duration: Simulation duration in seconds
        """
        if not self.running:
            self.start()
        
        end_time = self.time + duration
        
        while self.running and self.time < end_time:
            self.step()
            time.sleep(0.1)  # Simulated time step
            self.time += 0.1
    
    def step(self):
        """Advance the simulation by one time step."""
        # Process events in the queue
        while not self.event_queue.empty():
            event = self.event_queue.get()
            # Process event here
            # This is where you would implement event handling
            pass
    
    def ping(self, source: str, destination: str, count: int = 4) -> Dict:
        """
        Simulate a ping between two devices.
        
        Args:
            source: Source device name
            destination: Destination device name
            count: Number of ping packets to send
            
        Returns:
            Dictionary with ping statistics
        """
        if source not in self.network.devices or destination not in self.network.devices:
            return {"error": "Source or destination device not found"}
        
        results = {
            "source": source,
            "destination": destination,
            "sent": 0,
            "received": 0,
            "lost": 0,
            "times": [],
            "path": []
        }
        
        # Get the path
        path = self.network.get_shortest_path(source, destination)
        if not path:
            return {"error": "No path found between devices"}
            
        results["path"] = path
        
        # Simulate pings
        for i in range(count):
            results["sent"] += 1
            
            # Simulate network delay
            latency = random.uniform(*self.latency_range) / 1000  # Convert to seconds
            time.sleep(latency)
            
            # Check if packet is lost
            if random.random() < self.packet_loss_rate:
                results["lost"] += 1
                print(f"Ping request to {destination} timed out")
                continue
            
            # Packet made it
            results["received"] += 1
            results["times"].append(latency * 1000)  # Convert to ms
            
            # Print ping response
            print(f"Reply from {destination}: bytes=32 time={latency*1000:.2f}ms TTL=64")
        
        # Calculate statistics
        if results["received"] > 0:
            results["min"] = min(results["times"])
            results["max"] = max(results["times"])
            results["avg"] = sum(results["times"]) / len(results["times"])
            results["loss"] = (results["lost"] / results["sent"]) * 100
        
        return results
