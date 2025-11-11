import time
import random
from queue import Queue
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Packet:
    """Class representing a network packet."""
    source: str
    destination: str
    payload: any
    ttl: int = 64
    protocol: str = "tcp"
    size: int = 1500  # bytes
    timestamp: float = field(default_factory=time.time)
    path: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.path = [self.source]
    
    def add_hop(self, node: str) -> None:
        """Add a hop to the packet's path."""
        self.path.append(node)
        self.ttl -= 1
        if self.ttl <= 0:
            raise TimeoutError("Packet TTL expired")


class NetworkSimulation:
    """Class for simulating network behavior."""
    
    def __init__(self, network):
        """Initialize the simulation with a network topology."""
        self.network = network
        self.event_queue = Queue()
        self.time = 0
        self.packet_loss_rate = 0.01  # 1% packet loss
        self.latency_range = (1, 10)   # ms
        self.bandwidth = 1000  # Mbps
        self.running = False
    
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
