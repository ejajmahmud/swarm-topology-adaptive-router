"""Unit tests for swarm-topology-adaptive-router."""
import unittest
from swarm_topology_adaptive_router.router import TopologyRouter, RoutePacket

class TestTopologyRouter(unittest.TestCase):
    def setUp(self):
        self.router = TopologyRouter()

    def test_dijkstra_path(self):
        self.router.add_edge("n1", "n2", 1.0)
        self.router.add_edge("n2", "n3", 2.0)
        self.router.add_edge("n1", "n3", 5.0)
        path = self.router.find_shortest_path("n1", "n3")
        self.assertEqual(path, ["n1", "n2", "n3"])

    def test_adaptive_shortcut(self):
        self.router.add_edge("A", "Hub", 2.0)
        self.router.add_edge("Hub", "B", 2.0)
        for _ in range(6):
            self.router.record_traffic("A", "B")
        path = self.router.find_shortest_path("A", "B")
        self.assertEqual(path, ["A", "B"])

    def test_unreachable_node(self):
        self.router.add_node("isolated")
        self.router.add_edge("A", "B", 1.0)
        path = self.router.find_shortest_path("A", "isolated")
        self.assertIsNone(path)

if __name__ == "__main__":
    unittest.main()
