"""
Unit tests for Multistage Graph
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph.multistage import MultistageGraph


class TestMultistageGraph(unittest.TestCase):
    """Test cases for MultistageGraph class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.graph = MultistageGraph()
    
    def test_add_node(self):
        """Test adding nodes to the graph"""
        self.graph.add_node('R1', stage=1, name='Restaurant')
        self.assertIn('R1', self.graph.nodes)
        self.assertEqual(self.graph.nodes['R1']['stage'], 1)
        self.assertEqual(self.graph.nodes['R1']['name'], 'Restaurant')
    
    def test_add_multiple_nodes(self):
        """Test adding multiple nodes"""
        self.graph.add_node('R1', stage=1, name='Restaurant')
        self.graph.add_node('H1', stage=2, name='Hub')
        self.graph.add_node('C1', stage=3, name='Customer')
        
        self.assertEqual(len(self.graph.nodes), 3)
        self.assertIn('R1', self.graph.nodes)
        self.assertIn('H1', self.graph.nodes)
        self.assertIn('C1', self.graph.nodes)
    
    def test_add_edge(self):
        """Test adding edges between nodes"""
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('H1', stage=2)
        
        self.graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
        
        edges = self.graph.get_edges_from('R1')
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]['to'], 'H1')
        self.assertEqual(edges[0]['distance'], 5.0)
        self.assertEqual(edges[0]['time'], 10)
    
    def test_forward_approach_simple(self):
        """Test forward approach with simple graph"""
        # Create simple graph: R1 -> H1 -> C1
        self.graph.add_node('R1', stage=1, name='Restaurant')
        self.graph.add_node('H1', stage=2, name='Hub')
        self.graph.add_node('C1', stage=3, name='Customer')
        
        self.graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
        self.graph.add_edge('H1', 'C1', distance=3.0, time=5, cost=30)
        
        path, distance, time = self.graph.forward_approach('R1', 'C1')
        
        self.assertIsNotNone(path)
        self.assertEqual(path, ['R1', 'H1', 'C1'])
        self.assertEqual(distance, 8.0)
        self.assertEqual(time, 15)
    
    def test_forward_approach_multiple_paths(self):
        """Test forward approach with multiple possible paths"""
        # Create graph with multiple paths
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('H1', stage=2)
        self.graph.add_node('H2', stage=2)
        self.graph.add_node('C1', stage=3)
        
        # Two paths: R1->H1->C1 (cost 10) and R1->H2->C1 (cost 8)
        self.graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=100)
        self.graph.add_edge('R1', 'H2', distance=4.0, time=8, cost=80)
        self.graph.add_edge('H1', 'C1', distance=5.0, time=5, cost=50)
        self.graph.add_edge('H2', 'C1', distance=4.0, time=5, cost=40)
        
        path, distance, time = self.graph.forward_approach('R1', 'C1')
        
        self.assertIsNotNone(path)
        # Should choose the cheaper path
        self.assertEqual(path, ['R1', 'H2', 'C1'])
    
    def test_no_path_exists(self):
        """Test when no path exists"""
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('C1', stage=3)
        
        path, distance, time = self.graph.forward_approach('R1', 'C1')
        
        self.assertIsNone(path)
        self.assertEqual(distance, 0)
        self.assertEqual(time, 0)
    
    def test_invalid_node(self):
        """Test with invalid nodes"""
        self.graph.add_node('R1', stage=1)
        
        path, distance, time = self.graph.forward_approach('R1', 'InvalidNode')
        
        self.assertIsNone(path)
    
    def test_get_nodes_in_stage(self):
        """Test retrieving nodes by stage"""
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('H1', stage=2)
        self.graph.add_node('H2', stage=2)
        
        stage1_nodes = self.graph.get_nodes_in_stage(1)
        stage2_nodes = self.graph.get_nodes_in_stage(2)
        
        self.assertEqual(stage1_nodes, ['R1'])
        self.assertEqual(set(stage2_nodes), {'H1', 'H2'})
    
    def test_get_all_stages(self):
        """Test getting all stages"""
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('H1', stage=2)
        self.graph.add_node('C1', stage=3)
        
        stages = self.graph.get_all_stages()
        
        self.assertEqual(len(stages), 3)
        self.assertIn(1, stages)
        self.assertIn(2, stages)
        self.assertIn(3, stages)
    
    def test_invalid_edge_backward(self):
        """Test that edges must go forward in stages"""
        self.graph.add_node('R1', stage=1)
        self.graph.add_node('H1', stage=2)
        
        # Should raise error when trying to add backward edge
        with self.assertRaises(ValueError):
            self.graph.add_edge('H1', 'R1', distance=5.0, time=10)


if __name__ == '__main__':
    unittest.main()