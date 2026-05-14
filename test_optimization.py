#!/usr/bin/env python
"""
Test script to verify the route optimization fixes
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.optimizer import DeliveryOptimizer
from graph.utils import create_sample_graph

def test_optimization():
    """Test various optimization scenarios"""
    
    print("=" * 60)
    print("Food Delivery Route Optimization - Test Suite")
    print("=" * 60)
    
    optimizer = DeliveryOptimizer()
    
    # Test 1: Valid route (should work)
    print("\n✅ TEST 1: Valid route (R1 to C1)")
    print("-" * 60)
    result = optimizer.optimize_route('R1', 'C1')
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Route: {' → '.join([step['node_id'] for step in result['route']])}")
        print(f"Distance: {result['total_distance']} km")
        print(f"Time: {result['total_time']} min")
    else:
        print(f"Message: {result.get('message')}")
    
    # Test 2: Same stage nodes (should fail with clear message)
    print("\n❌ TEST 2: Same stage nodes (C1 to C2)")
    print("-" * 60)
    result = optimizer.optimize_route('C1', 'C2')
    print(f"Success: {result.get('success')}")
    if not result.get('success'):
        print(f"Message: {result.get('message')}")
    
    # Test 3: Reverse order (should fail with clear message)
    print("\n❌ TEST 3: Reverse order (C1 to R1)")
    print("-" * 60)
    result = optimizer.optimize_route('C1', 'R1')
    print(f"Success: {result.get('success')}")
    if not result.get('success'):
        print(f"Message: {result.get('message')}")
    
    # Test 4: Valid route with different stages
    print("\n✅ TEST 4: Valid route (H1 to C3)")
    print("-" * 60)
    result = optimizer.optimize_route('H1', 'C3')
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Route: {' → '.join([step['node_id'] for step in result['route']])}")
        print(f"Distance: {result['total_distance']} km")
        print(f"Time: {result['total_time']} min")
    else:
        print(f"Message: {result.get('message')}")
    
    # Test 5: Get all nodes
    print("\n📊 TEST 5: Available nodes")
    print("-" * 60)
    nodes = optimizer.get_all_nodes()
    for node_id, info in nodes.items():
        print(f"  {node_id}: {info['name']} (Stage {info['stage']})")
    
    # Test 6: Graph statistics
    print("\n📈 TEST 6: Graph statistics")
    print("-" * 60)
    stats = optimizer.get_graph_stats()
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Stages: {stats['total_stages']}")
    print(f"Total Edges: {stats['total_edges']}")
    print(f"Stages breakdown: {stats['stages']}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == '__main__':
    test_optimization()
