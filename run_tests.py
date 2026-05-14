#!/usr/bin/env python
"""
Test script for Food Delivery Route Optimization
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Food Delivery Route Optimization - Test Suite")
print("=" * 60)

# Test 1: Import MultistageGraph
print("\n[TEST 1] Importing MultistageGraph...")
try:
    from graph.multistage import MultistageGraph
    print("✓ MultistageGraph imported successfully")
except Exception as e:
    print(f"✗ Failed to import MultistageGraph: {e}")
    sys.exit(1)

# Test 2: Create and test graph
print("\n[TEST 2] Creating and testing graph...")
try:
    graph = MultistageGraph()
    graph.add_node('R1', stage=1, name='Restaurant')
    graph.add_node('H1', stage=2, name='Hub')
    graph.add_node('C1', stage=3, name='Customer')
    graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
    graph.add_edge('H1', 'C1', distance=3.0, time=5, cost=30)
    
    path, distance, time = graph.forward_approach('R1', 'C1')
    assert path == ['R1', 'H1', 'C1'], f"Expected ['R1', 'H1', 'C1'], got {path}"
    assert distance == 8.0, f"Expected 8.0, got {distance}"
    assert time == 15, f"Expected 15, got {time}"
    print("✓ Graph creation and pathfinding works correctly")
except Exception as e:
    print(f"✗ Graph test failed: {e}")
    sys.exit(1)

# Test 3: Import Optimizer
print("\n[TEST 3] Importing Optimizer...")
try:
    from services.optimizer import DeliveryOptimizer, get_optimizer
    print("✓ Optimizer imported successfully")
except Exception as e:
    print(f"✗ Failed to import Optimizer: {e}")
    sys.exit(1)

# Test 4: Test optimizer with sample graph
print("\n[TEST 4] Testing Optimizer with sample graph...")
try:
    optimizer = get_optimizer()
    stats = optimizer.get_graph_stats()
    print(f"✓ Optimizer initialized")
    print(f"  - Total Nodes: {stats['total_nodes']}")
    print(f"  - Total Stages: {stats['total_stages']}")
    print(f"  - Total Edges: {stats['total_edges']}")
except Exception as e:
    print(f"✗ Optimizer test failed: {e}")
    sys.exit(1)

# Test 5: Test route optimization
print("\n[TEST 5] Testing route optimization...")
try:
    result = optimizer.optimize_route('R1', 'C1')
    assert result['success'], f"Route optimization failed: {result}"
    print(f"✓ Route optimization successful")
    print(f"  - Distance: {result['total_distance']} km")
    print(f"  - Time: {result['total_time']} minutes")
    print(f"  - Steps: {result['total_steps']}")
except Exception as e:
    print(f"✗ Route optimization test failed: {e}")
    sys.exit(1)

# Test 6: Test API routes
print("\n[TEST 6] Testing Flask app and API routes...")
try:
    from app import app
    client = app.test_client()
    
    # Test health endpoint
    response = client.get('/api/health')
    assert response.status_code == 200, f"Health check failed with status {response.status_code}"
    print("✓ Health check endpoint works")
    
    # Test stats endpoint
    response = client.get('/api/stats')
    assert response.status_code == 200, f"Stats endpoint failed with status {response.status_code}"
    print("✓ Stats endpoint works")
    
    # Test nodes endpoint
    response = client.get('/api/nodes')
    assert response.status_code == 200, f"Nodes endpoint failed with status {response.status_code}"
    print("✓ Nodes endpoint works")
    
    # Test optimize endpoint
    response = client.post('/api/optimize', 
                          json={'source': 'R1', 'destination': 'C1'},
                          content_type='application/json')
    assert response.status_code == 200, f"Optimize endpoint failed with status {response.status_code}"
    print("✓ Optimize endpoint works")
    
except Exception as e:
    print(f"✗ Flask app test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nApplication is ready to run!")
print("Start the server with: python src/app.py")
print("Access at: http://localhost:5000")
