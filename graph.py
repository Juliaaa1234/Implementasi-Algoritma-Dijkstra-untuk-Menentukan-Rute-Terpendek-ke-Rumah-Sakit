"""
core/graph.py - Modul Inti Sistem
==================================
Berisi:
  • Data Structures: Node, Edge, Graph
  • Algorithm: Dijkstra
"""

import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

# ========== DATA STRUCTURES ==========

@dataclass
class Node:
    """Simpul (titik) dalam graf: lokasi geografis"""
    id: str
    name: str
    lat: float
    lng: float
    node_type: str  # 'start' | 'hospital'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False


@dataclass
class Edge:
    """Sisi (jalan) dalam graf: koneksi antar node"""
    to_node: Node
    weight: float  # jarak dalam km


@dataclass
class Graph:
    """Graf berbobot tidak berarah - adjacency list"""
    nodes: Dict[str, Node] = field(default_factory=dict)
    adjacency_list: Dict[str, List[Edge]] = field(default_factory=dict)

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        if node.id not in self.adjacency_list:
            self.adjacency_list[node.id] = []

    def add_edge(self, from_id: str, to_id: str, weight: float, bidirectional: bool = True):
        if from_id not in self.nodes or to_id not in self.nodes:
            raise ValueError(f"Node tidak ditemukan: {from_id} atau {to_id}")

        self.adjacency_list[from_id].append(Edge(self.nodes[to_id], weight))
        if bidirectional:
            self.adjacency_list[to_id].append(Edge(self.nodes[from_id], weight))

    def get_neighbors(self, node_id: str) -> List[Edge]:
        return self.adjacency_list.get(node_id, [])

    def get_starts(self) -> List[Node]:
        return [n for n in self.nodes.values() if n.node_type == 'start']

    def get_hospitals(self) -> List[Node]:
        return [n for n in self.nodes.values() if n.node_type == 'hospital']


# ========== ALGORITHM: DIJKSTRA ==========

class DijkstraAlgorithm:
    """Algoritma Dijkstra untuk shortest path"""

    def find_path(self, graph: Graph, start_id: str, target_id: str) -> Tuple[Optional[List[Node]], float]:
        """Cari jalur terpendek dari start ke target"""
        dist = {nid: float('inf') for nid in graph.nodes}
        dist[start_id] = 0
        prev = {nid: None for nid in graph.nodes}
        pq = [(0, start_id)]
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)

            if u == target_id:
                break
            if u in visited:
                continue
            visited.add(u)

            for edge in graph.get_neighbors(u):
                v, w = edge.to_node.id, edge.weight
                if d + w < dist[v]:
                    dist[v] = d + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))

        if dist[target_id] == float('inf'):
            return None, float('inf')

        # Rekonstruksi path
        path = []
        cur = target_id
        while cur is not None:
            path.append(graph.nodes[cur])
            cur = prev[cur]
        path.reverse()

        return path, dist[target_id]

    def find_nearest_hospital(self, graph: Graph, start_id: str):
        """Cari RS terdekat dari start_id"""
        hospitals = [nid for nid, n in graph.nodes.items() if n.node_type == 'hospital']

        best, best_dist, best_id = None, float('inf'), None
        for hid in hospitals:
            p, d = self.find_path(graph, start_id, hid)
            if p and d < best_dist:
                best, best_dist, best_id = p, d, hid

        return best, best_dist, best_id
