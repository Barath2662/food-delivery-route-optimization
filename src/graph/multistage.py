"""
Multistage Graph Implementation for Route Optimization
Supports forward approach to find shortest path through multiple stages
"""

from typing import Dict, List, Tuple, Optional
import heapq
from collections import defaultdict


class MultistageGraph:
    """
    A multistage graph where nodes are organized in stages.
    Each stage represents a checkpoint in the delivery route.
    
    Example stages:
    Stage 1: Restaurant
    Stage 2: Pickup Hub
    Stage 3: Delivery Zone
    Stage 4: Customer
    """
    
    def __init__(self):
        """Initialize the multistage graph"""
        self.nodes = {}  # {node_id: {'stage': stage_num, 'name': node_name}}
        self.edges = defaultdict(list)  # {from_node: [(to_node, distance, time, cost)]}
        self.stages = defaultdict(list)  # {stage_num: [node_ids]}
    
    def add_node(self, node_id: str, stage: int, name: str = None) -> None:
        """
        Add a node to the graph
        
        Args:
            node_id: Unique identifier for the node
            stage: Stage number (1, 2, 3, etc.)
            name: Optional display name for the node
        """
        self.nodes[node_id] = {
            'stage': stage,
            'name': name or node_id
        }
        self.stages[stage].append(node_id)
    
    def add_edge(self, from_node: str, to_node: str, 
                 distance: float, time: float, cost: float = None) -> None:
        """
        Add an edge between two nodes
        
        Args:
            from_node: Source node ID
            to_node: Destination node ID
            distance: Distance in km
            time: Time in minutes
            cost: Cost (optional, defaults to distance)
        """
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError(f"Node not found: {from_node} or {to_node}")
        
        # Ensure from_node stage < to_node stage (forward progression)
        from_stage = self.nodes[from_node]['stage']
        to_stage = self.nodes[to_node]['stage']
        
        if from_stage >= to_stage:
            raise ValueError(f"Edge must go from earlier stage to later stage")
        
        if cost is None:
            cost = distance
        
        self.edges[from_node].append({
            'to': to_node,
            'distance': distance,
            'time': time,
            'cost': cost
        })
    
    def get_node_info(self, node_id: str) -> Dict:
        """Get information about a node"""
        return self.nodes.get(node_id, {})
    
    def get_edges_from(self, node_id: str) -> List:
        """Get all edges from a given node"""
        return self.edges.get(node_id, [])
    
    def get_nodes_in_stage(self, stage: int) -> List[str]:
        """Get all nodes in a specific stage"""
        return self.stages.get(stage, [])
    
    def get_all_stages(self) -> Dict[int, List[str]]:
        """Get all stages and their nodes"""
        return dict(self.stages)
    
    def forward_approach(self, start_node: str, end_node: str) -> Tuple[Optional[List[str]], float, float]:
        """
        Find the shortest path from start to end using forward approach with Dijkstra
        
        Args:
            start_node: Starting node ID
            end_node: Ending node ID
        
        Returns:
            Tuple of (path, total_distance, total_time)
            Returns (None, 0, 0) if no path exists
        """
        if start_node not in self.nodes or end_node not in self.nodes:
            return None, 0, 0
        
        # Dijkstra's algorithm
        distances = {node: float('inf') for node in self.nodes}
        times = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0
        times[start_node] = 0
        
        previous = {node: None for node in self.nodes}
        pq = [(0, start_node)]  # (cost, node)
        visited = set()
        
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == end_node:
                # Reconstruct path
                path = []
                node = end_node
                while node is not None:
                    path.append(node)
                    node = previous[node]
                path.reverse()
                
                return path, distances[end_node], times[end_node]
            
            # Check all neighbors
            for edge in self.edges[current_node]:
                to_node = edge['to']
                new_distance = distances[current_node] + edge['distance']
                new_time = times[current_node] + edge['time']
                
                if new_distance < distances[to_node]:
                    distances[to_node] = new_distance
                    times[to_node] = new_time
                    previous[to_node] = current_node
                    heapq.heappush(pq, (new_distance, to_node))
        
        return None, 0, 0
    
    def get_all_paths(self, start_node: str) -> Dict[str, Tuple[List[str], float, float]]:
        """Get shortest paths from start node to all reachable nodes"""
        result = {}
        
        for end_node in self.nodes:
            if end_node != start_node:
                path, distance, time = self.forward_approach(start_node, end_node)
                if path:
                    result[end_node] = {
                        'path': path,
                        'distance': distance,
                        'time': time
                    }
        
        return result
    
    def __repr__(self) -> str:
        """String representation of the graph"""
        return f"MultistageGraph(nodes={len(self.nodes)}, stages={dict(self.stages)})"