import pytest
from network_simulator.network import NetworkTopology
from network_simulator.device import Router, Switch, Host

class TestNetworkTopology:
    def setup_method(self):
        self.network = NetworkTopology("Test Network")
        self.router = Router("R1")
        self.switch = Switch("SW1")
        self.host = Host("PC1")
        
        self.network.add_device(self.router)
        self.network.add_device(self.switch)
        self.network.add_device(self.host)

    def test_add_device(self):
        assert len(self.network.devices) == 3
        assert "R1" in self.network.devices
        assert "SW1" in self.network.devices
        assert "PC1" in self.network.devices

    def test_connect_devices(self):
        self.network.connect_devices("R1", "eth0", "SW1", "eth1")
        self.network.connect_devices("SW1", "eth2", "PC1", "eth0")
        
        assert self.network.graph.has_edge("R1", "SW1")
        assert self.network.graph.has_edge("SW1", "PC1")
        assert not self.network.graph.has_edge("R1", "PC1")

    def test_shortest_path(self):
        self.network.connect_devices("R1", "eth0", "SW1", "eth1")
        self.network.connect_devices("SW1", "eth2", "PC1", "eth0")
        
        path = self.network.get_shortest_path("R1", "PC1")
        assert path == ["R1", "SW1", "PC1"]

    def test_remove_device(self):
        self.network.remove_device("PC1")
        assert "PC1" not in self.network.devices
        assert len(self.network.devices) == 2

class TestDevice:
    def test_router_initialization(self):
        router = Router("R1")
        assert router.name == "R1"
        assert router.device_type == "router"
        assert hasattr(router, 'routing_table')

    def test_switch_initialization(self):
        switch = Switch("SW1")
        assert switch.name == "SW1"
        assert switch.device_type == "switch"
        assert hasattr(switch, 'mac_table')

    def test_host_initialization(self):
        host = Host("PC1")
        assert host.name == "PC1"
        assert host.device_type == "host"
        assert hasattr(host, 'running_processes')
