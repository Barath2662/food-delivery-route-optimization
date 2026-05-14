"""
Delivery Route Optimizer Service
Handles route optimization using multistage graph and forward approach
"""

from typing import Dict, List, Tuple, Optional
from graph.multistage import MultistageGraph
from graph.utils import format_route_result, create_sample_graph


class DeliveryOptimizer:
    """
    Service class for optimizing delivery routes using multistage graphs
    """
    
    def __init__(self, graph: MultistageGraph = None):
        """
        Initialize the optimizer with a graph
        
        Args:
            graph: MultistageGraph instance, if None uses sample graph
        """
        if graph is None:
            self.graph = create_sample_graph()
        else:
            self.graph = graph
    
    def optimize_route(self, start_node: str, end_node: str) -> Dict:
        """
        Find the optimal route from start to end node
        
        Args:
            start_node: Starting node ID
            end_node: Destination node ID
        
        Returns:
            Dictionary containing the optimized route and metrics
        """
        # Validate nodes exist
        if not self.validate_node(start_node):
            return {'success': False, 'message': f'Source node "{start_node}" not found'}
        
        if not self.validate_node(end_node):
            return {'success': False, 'message': f'Destination node "{end_node}" not found'}
        
        # Check if nodes are in different stages
        start_stage = self.graph.nodes[start_node]['stage']
        end_stage = self.graph.nodes[end_node]['stage']
        
        if start_stage == end_stage:
            return {'success': False, 'message': f'Source and destination must be in different stages. Both nodes are in stage {start_stage}'}
        
        if start_stage > end_stage:
            return {'success': False, 'message': f'Route must go forward through stages. Start stage ({start_stage}) must be before end stage ({end_stage})'}
        
        # Attempt to find path
        path, distance, time = self.graph.forward_approach(start_node, end_node)
        
        if not path:
            return {'success': False, 'message': f'No direct route exists from {start_node} (Stage {start_stage}) to {end_node} (Stage {end_stage})'}
        
        return format_route_result(path, distance, time, self.graph)
    
    def get_available_routes(self) -> Dict[str, List[str]]:
        """
        Get all available nodes organized by stage
        
        Returns:
            Dictionary of stages and their nodes
        """
        stages = self.graph.get_all_stages()
        return {f"stage_{stage}": nodes for stage, nodes in stages.items()}
    
    def get_route_details(self, start_node: str, end_node: str) -> Dict:
        """
        Get detailed route information including each edge
        
        Args:
            start_node: Starting node ID
            end_node: Destination node ID
        
        Returns:
            Dictionary with route details and edge information
        """
        path, distance, time = self.graph.forward_approach(start_node, end_node)
        
        if not path:
            return {
                'success': False,
                'message': f'No route found from {start_node} to {end_node}'
            }
        
        route_details = format_route_result(path, distance, time, self.graph)
        
        # Add edge information
        edges_info = []
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            
            for edge in self.graph.get_edges_from(from_node):
                if edge['to'] == to_node:
                    edges_info.append({
                        'from': from_node,
                        'to': to_node,
                        'distance': edge['distance'],
                        'time': edge['time'],
                        'cost': edge['cost']
                    })
                    break
        
        route_details['edges'] = edges_info
        return route_details
    
    def validate_node(self, node_id: str) -> bool:
        """
        Check if a node exists in the graph
        
        Args:
            node_id: Node ID to validate
        
        Returns:
            True if node exists, False otherwise
        """
        return node_id in self.graph.nodes
    
    def get_node_info(self, node_id: str) -> Optional[Dict]:
        """
        Get information about a specific node
        
        Args:
            node_id: Node ID
        
        Returns:
            Dictionary with node information or None if not found
        """
        if self.validate_node(node_id):
            info = self.graph.get_node_info(node_id)
            info['id'] = node_id
            return info
        return None
    
    def get_all_nodes(self) -> Dict[str, Dict]:
        """
        Get information about all nodes in the graph
        
        Returns:
            Dictionary with all nodes and their information
        """
        nodes_info = {}
        for node_id, info in self.graph.nodes.items():
            nodes_info[node_id] = info
        return nodes_info
    
    def get_graph_stats(self) -> Dict:
        """
        Get statistics about the graph
        
        Returns:
            Dictionary with graph statistics
        """
        total_nodes = len(self.graph.nodes)
        total_stages = len(self.graph.stages)
        total_edges = sum(len(edges) for edges in self.graph.edges.values())
        
        return {
            'total_nodes': total_nodes,
            'total_stages': total_stages,
            'total_edges': total_edges,
            'stages': {stage: len(nodes) for stage, nodes in self.graph.stages.items()}
        }


# Global optimizer instance
_optimizer_instance = None


def get_optimizer() -> DeliveryOptimizer:
    """
    Get or create the global optimizer instance
    
    Returns:
        DeliveryOptimizer instance
    """
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = DeliveryOptimizer()
    return _optimizer_instance


def optimize_route(start_node: str, end_node: str) -> Dict:
    """
    Convenience function to optimize a route
    
    Args:
        start_node: Starting node ID
        end_node: Destination node ID
    
    Returns:
        Dictionary with optimized route
    """
    optimizer = get_optimizer()
    return optimizer.optimize_route(start_node, end_node)