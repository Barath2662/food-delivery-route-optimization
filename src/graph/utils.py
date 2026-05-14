"""
Utility functions for graph operations
"""

from typing import Dict, List, Tuple
from .multistage import MultistageGraph


def create_sample_graph() -> MultistageGraph:
    """
    Create a sample multistage graph for testing and demonstration
    
    Graph structure:
    Stage 1 (Restaurant): R1
    Stage 2 (Hub): H1, H2
    Stage 3 (Zone): Z1, Z2
    Stage 4 (Customer): C1, C2, C3
    """
    graph = MultistageGraph()
    
    # Stage 1: Restaurant
    graph.add_node('R1', stage=1, name='Restaurant Main')
    
    # Stage 2: Pickup Hub
    graph.add_node('H1', stage=2, name='Hub North')
    graph.add_node('H2', stage=2, name='Hub South')
    
    # Stage 3: Delivery Zone
    graph.add_node('Z1', stage=3, name='Zone East')
    graph.add_node('Z2', stage=3, name='Zone West')
    
    # Stage 4: Customer
    graph.add_node('C1', stage=4, name='Customer A')
    graph.add_node('C2', stage=4, name='Customer B')
    graph.add_node('C3', stage=4, name='Customer C')
    
    # Edges: Restaurant to Hubs
    graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
    graph.add_edge('R1', 'H2', distance=8.0, time=15, cost=80)
    
    # Edges: Hubs to Zones
    graph.add_edge('H1', 'Z1', distance=3.0, time=8, cost=30)
    graph.add_edge('H1', 'Z2', distance=7.0, time=12, cost=70)
    graph.add_edge('H2', 'Z1', distance=6.0, time=12, cost=60)
    graph.add_edge('H2', 'Z2', distance=2.0, time=5, cost=20)
    
    # Edges: Zones to Customers
    graph.add_edge('Z1', 'C1', distance=2.0, time=5, cost=20)
    graph.add_edge('Z1', 'C2', distance=4.0, time=8, cost=40)
    graph.add_edge('Z2', 'C2', distance=3.0, time=7, cost=30)
    graph.add_edge('Z2', 'C3', distance=5.0, time=10, cost=50)
    
    return graph


def format_route_result(path: List[str], distance: float, time: float, 
                        graph: MultistageGraph) -> Dict:
    """
    Format route result with node information
    
    Args:
        path: List of node IDs in the route
        distance: Total distance in km
        time: Total time in minutes
        graph: The MultistageGraph object
    
    Returns:
        Formatted dictionary with route details
    """
    if not path:
        return {
            'success': False,
            'message': 'No route found',
            'route': [],
            'total_distance': 0,
            'total_time': 0
        }
    
    route_details = []
    for i, node_id in enumerate(path):
        node_info = graph.get_node_info(node_id)
        stage = node_info.get('stage', 'Unknown')
        name = node_info.get('name', node_id)
        
        route_details.append({
            'step': i + 1,
            'node_id': node_id,
            'stage': stage,
            'name': name
        })
    
    return {
        'success': True,
        'route': route_details,
        'total_distance': round(distance, 2),
        'total_time': round(time, 2),
        'total_steps': len(path)
    }


def calculate_multiple_routes(start_node: str, destinations: List[str], 
                               graph: MultistageGraph) -> Dict:
    """
    Calculate routes from start node to multiple destinations
    
    Args:
        start_node: Starting node ID
        destinations: List of destination node IDs
        graph: The MultistageGraph object
    
    Returns:
        Dictionary with routes to all destinations
    """
    results = {}
    
    for dest in destinations:
        path, distance, time = graph.forward_approach(start_node, dest)
        results[dest] = format_route_result(path, distance, time, graph)
    
    return results


def get_graph_summary(graph: MultistageGraph) -> Dict:
    """
    Get summary information about the graph
    
    Args:
        graph: The MultistageGraph object
    
    Returns:
        Dictionary with graph statistics
    """
    total_nodes = len(graph.nodes)
    total_stages = len(graph.stages)
    total_edges = sum(len(edges) for edges in graph.edges.values())
    
    return {
        'total_nodes': total_nodes,
        'total_stages': total_stages,
        'total_edges': total_edges,
        'stages': {stage: len(nodes) for stage, nodes in graph.stages.items()}
    }