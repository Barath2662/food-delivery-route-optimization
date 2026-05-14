#!/usr/bin/env python
"""
Quick Start and Demo Script for Food Delivery Route Optimization
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_banner():
    print("\n" + "="*70)
    print(" 🚚 FOOD DELIVERY ROUTE OPTIMIZATION - QUICK START DEMO")
    print("="*70 + "\n")

def test_basic_functionality():
    print("[DEMO 1] Creating a Multistage Graph")
    print("-" * 70)
    
    from graph.multistage import MultistageGraph
    
    graph = MultistageGraph()
    
    # Create stages
    print("✓ Adding Stage 1 (Restaurant)...")
    graph.add_node('R1', stage=1, name='Restaurant Main')
    
    print("✓ Adding Stage 2 (Pickup Hubs)...")
    graph.add_node('H1', stage=2, name='Hub North')
    graph.add_node('H2', stage=2, name='Hub South')
    
    print("✓ Adding Stage 3 (Delivery Zones)...")
    graph.add_node('Z1', stage=3, name='Zone East')
    graph.add_node('Z2', stage=3, name='Zone West')
    
    print("✓ Adding Stage 4 (Customers)...")
    graph.add_node('C1', stage=4, name='Customer A')
    graph.add_node('C2', stage=4, name='Customer B')
    graph.add_node('C3', stage=4, name='Customer C')
    
    print("\n✓ Adding edges (routes with distances and times)...")
    graph.add_edge('R1', 'H1', distance=5.0, time=10, cost=50)
    graph.add_edge('R1', 'H2', distance=8.0, time=15, cost=80)
    graph.add_edge('H1', 'Z1', distance=3.0, time=8, cost=30)
    graph.add_edge('H1', 'Z2', distance=7.0, time=12, cost=70)
    graph.add_edge('H2', 'Z1', distance=6.0, time=12, cost=60)
    graph.add_edge('H2', 'Z2', distance=2.0, time=5, cost=20)
    graph.add_edge('Z1', 'C1', distance=2.0, time=5, cost=20)
    graph.add_edge('Z1', 'C2', distance=4.0, time=8, cost=40)
    graph.add_edge('Z2', 'C2', distance=3.0, time=7, cost=30)
    graph.add_edge('Z2', 'C3', distance=5.0, time=10, cost=50)
    
    stats = graph.get_all_stages()
    print(f"\n✓ Graph Statistics:")
    print(f"  - Total Nodes: {len(graph.nodes)}")
    print(f"  - Total Edges: {sum(len(edges) for edges in graph.edges.values())}")
    print(f"  - Total Stages: {len(stats)}")
    for stage, nodes in sorted(stats.items()):
        print(f"    Stage {stage}: {nodes}")
    
    return graph

def test_pathfinding(graph):
    print("\n[DEMO 2] Finding Optimal Routes Using Forward Approach (Dijkstra)")
    print("-" * 70)
    
    # Test case 1: R1 to C1
    print("\nRoute 1: Restaurant → Customer A")
    path, distance, time = graph.forward_approach('R1', 'C1')
    
    if path:
        print(f"  Path: {' → '.join(path)}")
        print(f"  Total Distance: {distance} km")
        print(f"  Total Time: {time} minutes")
        print(f"  Steps: {len(path)}")
    
    # Test case 2: R1 to C2 (multiple possible routes)
    print("\nRoute 2: Restaurant → Customer B (Multiple Path Options)")
    path, distance, time = graph.forward_approach('R1', 'C2')
    
    if path:
        print(f"  Path: {' → '.join(path)}")
        print(f"  Total Distance: {distance} km")
        print(f"  Total Time: {time} minutes")
        print(f"  Steps: {len(path)}")
        print(f"  ✓ Algorithm chose the optimal route!")
    
    # Test case 3: R1 to C3
    print("\nRoute 3: Restaurant → Customer C")
    path, distance, time = graph.forward_approach('R1', 'C3')
    
    if path:
        print(f"  Path: {' → '.join(path)}")
        print(f"  Total Distance: {distance} km")
        print(f"  Total Time: {time} minutes")
        print(f"  Steps: {len(path)}")

def test_optimizer_service(graph):
    print("\n[DEMO 3] Using the Delivery Optimizer Service")
    print("-" * 70)
    
    from services.optimizer import DeliveryOptimizer
    
    optimizer = DeliveryOptimizer(graph)
    
    print("\n✓ Optimizer initialized with graph")
    stats = optimizer.get_graph_stats()
    print(f"  - Total Nodes: {stats['total_nodes']}")
    print(f"  - Total Stages: {stats['total_stages']}")
    print(f"  - Total Edges: {stats['total_edges']}")
    
    print("\n✓ Testing route optimization API:")
    result = optimizer.optimize_route('R1', 'C1')
    
    if result['success']:
        print(f"\n  SUCCESS! Route optimized:")
        for step in result['route']:
            print(f"    Step {step['step']}: {step['name']} ({step['node_id']}) - Stage {step['stage']}")
        print(f"\n  Summary:")
        print(f"    - Total Distance: {result['total_distance']} km")
        print(f"    - Total Time: {result['total_time']} minutes")
        print(f"    - Total Steps: {result['total_steps']}")

def test_flask_api():
    print("\n[DEMO 4] Testing Flask REST API Endpoints")
    print("-" * 70)
    
    from app import app
    
    client = app.test_client()
    
    print("\n✓ Testing /api/health endpoint...")
    response = client.get('/api/health')
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Response: {data}")
    
    print("\n✓ Testing /api/stats endpoint...")
    response = client.get('/api/stats')
    data = response.get_json()
    print(f"  Total Nodes: {data['total_nodes']}")
    print(f"  Total Stages: {data['total_stages']}")
    print(f"  Total Edges: {data['total_edges']}")
    
    print("\n✓ Testing /api/nodes endpoint...")
    response = client.get('/api/nodes')
    data = response.get_json()
    print(f"  Available Nodes: {data['total']}")
    
    print("\n✓ Testing /api/optimize endpoint (POST)...")
    response = client.post('/api/optimize',
                          json={'source': 'R1', 'destination': 'C1'},
                          content_type='application/json')
    data = response.get_json()
    print(f"  Status: {response.status_code}")
    print(f"  Route Success: {data['success']}")
    if data['success']:
        print(f"  Distance: {data['total_distance']} km")
        print(f"  Time: {data['total_time']} minutes")

def main():
    print_banner()
    
    try:
        # Test 1: Basic functionality
        graph = test_basic_functionality()
        
        # Test 2: Pathfinding
        test_pathfinding(graph)
        
        # Test 3: Optimizer service
        test_optimizer_service(graph)
        
        # Test 4: Flask API
        test_flask_api()
        
        # Summary
        print("\n" + "="*70)
        print("✓ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nTo start the web server, run:")
        print("  cd src")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
