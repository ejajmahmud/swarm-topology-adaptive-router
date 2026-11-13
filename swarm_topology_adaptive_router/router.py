"""Dynamic adaptive graph topology router."""
import heapq
from typing import Dict, List, Set, Optional, Tuple, Any

class RoutePacket:
    def __init__(self, source: str, destination: str, payload: Any):
        self.source = source
        self.destination = destination
        self.payload = payload
        self.hops: List[str] = [source]

class TopologyRouter:
    """Manages weighted communication graphs and dynamically optimizes shortest-path routing."""

    def __init__(self):
        self.adjacency: Dict[str, Dict[str, float]] = {}
        self.traffic_volume: Dict[Tuple[str, str], int] = {}

    def add_node(self, node_id: str):
        if node_id not in self.adjacency:
            self.adjacency[node_id] = {}

    def add_edge(self, node_a: str, node_b: str, weight: float = 1.0):
        self.add_node(node_a)
        self.add_node(node_b)
        self.adjacency[node_a][node_b] = weight
        self.adjacency[node_b][node_a] = weight

    def record_traffic(self, source: str, destination: str):
        pair = (min(source, destination), max(source, destination))
        self.traffic_volume[pair] = self.traffic_volume.get(pair, 0) + 1

        # Dynamic adaptation: if traffic volume exceeds threshold, reduce weight or peer directly
        if self.traffic_volume[pair] > 5:
            # Shortcut link
            self.adjacency[source][destination] = 0.5
            self.adjacency[destination][source] = 0.5

    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        if start not in self.adjacency or end not in self.adjacency:
            return None
        if start == end:
            return [start]

        distances: Dict[str, float] = {node: float("inf") for node in self.adjacency}
        distances[start] = 0.0
        previous: Dict[str, Optional[str]] = {node: None for node in self.adjacency}
        pq = [(0.0, start)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            if curr_node == end:
                break
            if curr_dist > distances[curr_node]:
                continue

            for neighbor, weight in self.adjacency[curr_node].items():
                alt = curr_dist + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = curr_node
                    heapq.heappush(pq, (alt, neighbor))

        if previous[end] is None:
            return None

        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        return path

    def route_packet(self, packet: RoutePacket) -> bool:
        path = self.find_shortest_path(packet.source, packet.destination)
        if not path:
            return False
        packet.hops = path
        self.record_traffic(packet.source, packet.destination)
        return True
