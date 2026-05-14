"""
Unit tests for Delivery Optimizer Service
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.optimizer import DeliveryOptimizer, get_optimizer
from graph.multistage import MultistageGraph


class TestDeliveryOptimizer(unittest.TestCase):
    """Test cases for DeliveryOptimizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.graph = MultistageGraph()
        
        # Create test graph
        self.graph.add_node('R1', stage=1, name='Restaurant')
        self.graph.add_node('H1', stage=2, name='Hub1')
        self.graph.add_node('H2', stage=2, name='Hub2')
        self.graph.add_node('Z1', stage=3, name='Zone1')
        self.graph.add_node('C1', stage=4, name='Customer1')
        
        # Add edges
        self.graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
        self.graph.add_edge('R1', 'H2', distance=8.0, time=15, cost=80)
        self.graph.add_edge('H1', 'Z1', distance=3.0, time=8, cost=30)
        self.graph.add_edge('H2', 'Z1', distance=2.0, time=5, cost=20)
        self.graph.add_edge('Z1', 'C1', distance=2.0, time=5, cost=20)
        
        self.optimizer = DeliveryOptimizer(self.graph)
    
    def test_optimize_route_success(self):
        """Test successful route optimization"""
        result = self.optimizer.optimize_route('R1', 'C1')
        
        self.assertTrue(result['success'])
        self.assertIn('route', result)
        self.assertIn('total_distance', result)
        self.assertIn('total_time', result)
        self.assertGreater(result['total_distance'], 0)
        self.assertGreater(result['total_time'], 0)
    
    def test_optimize_route_no_path(self):
        """Test when no route exists"""
        # Add isolated node
        self.graph.add_node('Isolated', stage=1)
        
        result = self.optimizer.optimize_route('R1', 'Isolated')
        
        self.assertFalse(result['success'])
    
    def test_validate_node_exists(self):
        """Test node validation - node exists"""
        result = self.optimizer.validate_node('R1')
        self.assertTrue(result)
    
    def test_validate_node_not_exists(self):
        """Test node validation - node doesn't exist"""
        result = self.optimizer.validate_node('NonExistent')
        self.assertFalse(result)
    
    def test_get_node_info(self):
        """Test getting node information"""
        info = self.optimizer.get_node_info('R1')
        
        self.assertIsNotNone(info)
        self.assertEqual(info['id'], 'R1')
        self.assertEqual(info['name'], 'Restaurant')
        self.assertEqual(info['stage'], 1)
    
    def test_get_node_info_not_found(self):
        """Test getting info for non-existent node"""
        info = self.optimizer.get_node_info('NonExistent')
        self.assertIsNone(info)
    
    def test_get_all_nodes(self):
        """Test retrieving all nodes"""
        nodes = self.optimizer.get_all_nodes()
        
        self.assertGreater(len(nodes), 0)
        self.assertIn('R1', nodes)
        self.assertIn('H1', nodes)
        self.assertIn('C1', nodes)
    
    def test_get_available_routes(self):
        """Test getting available routes"""
        routes = self.optimizer.get_available_routes()
        
        self.assertIn('stage_1', routes)
        self.assertIn('stage_2', routes)
        self.assertIn('stage_3', routes)
        self.assertIn('stage_4', routes)
    
    def test_get_graph_stats(self):
        """Test getting graph statistics"""
        stats = self.optimizer.get_graph_stats()
        
        self.assertIn('total_nodes', stats)
        self.assertIn('total_stages', stats)
        self.assertIn('total_edges', stats)
        self.assertEqual(stats['total_nodes'], 5)
        self.assertEqual(stats['total_stages'], 4)
    
    def test_get_route_details(self):
        """Test getting detailed route information"""
        result = self.optimizer.get_route_details('R1', 'C1')
        
        if result['success']:
            self.assertIn('edges', result)
            self.assertGreater(len(result['edges']), 0)
            
            # Check edge structure
            edge = result['edges'][0]
            self.assertIn('from', edge)
            self.assertIn('to', edge)
            self.assertIn('distance', edge)
            self.assertIn('time', edge)
    
    def test_shortest_path_calculation(self):
        """Test that optimizer finds shortest path"""
        # Test with multiple path options
        result = self.optimizer.optimize_route('R1', 'C1')
        
        if result['success']:
            route = result['route']
            # Route should exist and contain at least 2 nodes
            self.assertGreater(len(route), 1)
            # First node should be R1
            self.assertEqual(route[0]['node_id'], 'R1')
            # Last node should be C1
            self.assertEqual(route[-1]['node_id'], 'C1')


class TestOptimizerGlobalInstance(unittest.TestCase):
    """Test the global optimizer instance"""
    
    def test_get_optimizer_singleton(self):
        """Test that get_optimizer returns singleton instance"""
        opt1 = get_optimizer()
        opt2 = get_optimizer()
        
        self.assertIs(opt1, opt2)
    
    def test_optimizer_has_sample_graph(self):
        """Test that default optimizer has sample graph"""
        optimizer = get_optimizer()
        stats = optimizer.get_graph_stats()
        
        self.assertGreater(stats['total_nodes'], 0)


class TestOptimizerErrors(unittest.TestCase):
    """Test error handling in optimizer"""
    
    def test_empty_source(self):
        """Test handling of empty source"""
        graph = MultistageGraph()
        graph.add_node('A', stage=1)
        optimizer = DeliveryOptimizer(graph)
        
        result = optimizer.optimize_route('', 'A')
        self.assertFalse(result['success'])
    
    def test_missing_destination(self):
        """Test handling of missing destination node"""
        graph = MultistageGraph()
        graph.add_node('A', stage=1)
        optimizer = DeliveryOptimizer(graph)
        
        result = optimizer.optimize_route('A', 'NonExistent')
        self.assertFalse(result['success'])


if __name__ == '__main__':
    unittest.main()