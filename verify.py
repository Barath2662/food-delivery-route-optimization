#!/usr/bin/env python
"""
Comprehensive Verification Script
Verifies all aspects of the Food Delivery Route Optimization project
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

CHECKS = {
    'imports': [],
    'graph': [],
    'optimizer': [],
    'api': [],
    'ui': []
}

def print_header(text):
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70)

def print_section(text):
    print(f"\n[{text}]")
    print("-" * 70)

def check_mark(success, message):
    symbol = "✓" if success else "✗"
    status = "PASS" if success else "FAIL"
    print(f"  {symbol} {message:<50} [{status}]")
    return success

# SECTION 1: Import Verification
print_header("VERIFICATION SUITE - Food Delivery Route Optimization")
print_section("1. Import Verification")

try:
    from graph.multistage import MultistageGraph
    CHECKS['imports'].append(check_mark(True, "MultistageGraph import"))
except Exception as e:
    CHECKS['imports'].append(check_mark(False, f"MultistageGraph import: {e}"))

try:
    from graph.utils import create_sample_graph, format_route_result
    CHECKS['imports'].append(check_mark(True, "Graph utils import"))
except Exception as e:
    CHECKS['imports'].append(check_mark(False, f"Graph utils import: {e}"))

try:
    from services.optimizer import DeliveryOptimizer, get_optimizer
    CHECKS['imports'].append(check_mark(True, "Optimizer import"))
except Exception as e:
    CHECKS['imports'].append(check_mark(False, f"Optimizer import: {e}"))

try:
    from models.order import Order
    CHECKS['imports'].append(check_mark(True, "Order model import"))
except Exception as e:
    CHECKS['imports'].append(check_mark(False, f"Order model import: {e}"))

try:
    from app import app
    CHECKS['imports'].append(check_mark(True, "Flask app import"))
except Exception as e:
    CHECKS['imports'].append(check_mark(False, f"Flask app import: {e}"))

# SECTION 2: Graph Verification
print_section("2. Graph Functionality")

try:
    graph = MultistageGraph()
    CHECKS['graph'].append(check_mark(True, "Graph instantiation"))
except Exception as e:
    CHECKS['graph'].append(check_mark(False, f"Graph instantiation: {e}"))
    sys.exit(1)

try:
    graph.add_node('N1', stage=1, name='Node1')
    graph.add_node('N2', stage=2, name='Node2')
    CHECKS['graph'].append(check_mark(True, "Add nodes"))
except Exception as e:
    CHECKS['graph'].append(check_mark(False, f"Add nodes: {e}"))

try:
    graph.add_edge('N1', 'N2', distance=5.0, time=10, cost=50)
    CHECKS['graph'].append(check_mark(True, "Add edges"))
except Exception as e:
    CHECKS['graph'].append(check_mark(False, f"Add edges: {e}"))

try:
    path, dist, time = graph.forward_approach('N1', 'N2')
    assert path == ['N1', 'N2'], f"Expected ['N1', 'N2'], got {path}"
    assert dist == 5.0
    assert time == 10
    CHECKS['graph'].append(check_mark(True, "Forward approach algorithm"))
except Exception as e:
    CHECKS['graph'].append(check_mark(False, f"Forward approach: {e}"))

try:
    graph2 = create_sample_graph()
    stats = graph2.get_all_stages()
    assert len(stats) == 4, f"Expected 4 stages, got {len(stats)}"
    CHECKS['graph'].append(check_mark(True, "Sample graph creation"))
except Exception as e:
    CHECKS['graph'].append(check_mark(False, f"Sample graph: {e}"))

# SECTION 3: Optimizer Verification
print_section("3. Optimizer Service")

try:
    optimizer = get_optimizer()
    CHECKS['optimizer'].append(check_mark(True, "Optimizer initialization"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Optimizer init: {e}"))
    sys.exit(1)

try:
    stats = optimizer.get_graph_stats()
    assert stats['total_nodes'] > 0
    assert stats['total_stages'] > 0
    CHECKS['optimizer'].append(check_mark(True, "Graph statistics"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Graph stats: {e}"))

try:
    all_nodes = optimizer.get_all_nodes()
    assert len(all_nodes) > 0
    CHECKS['optimizer'].append(check_mark(True, "Get all nodes"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Get all nodes: {e}"))

try:
    result = optimizer.optimize_route('R1', 'C1')
    assert result['success'] == True
    assert result['total_distance'] > 0
    assert result['total_time'] > 0
    CHECKS['optimizer'].append(check_mark(True, "Route optimization"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Route optimization: {e}"))

try:
    result = optimizer.get_route_details('R1', 'C1')
    assert result['success'] == True
    assert 'edges' in result
    CHECKS['optimizer'].append(check_mark(True, "Route details"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Route details: {e}"))

try:
    node_info = optimizer.get_node_info('R1')
    assert node_info is not None
    assert node_info['id'] == 'R1'
    CHECKS['optimizer'].append(check_mark(True, "Node information"))
except Exception as e:
    CHECKS['optimizer'].append(check_mark(False, f"Node info: {e}"))

# SECTION 4: API Verification
print_section("4. API Endpoints")

try:
    from app import app
    client = app.test_client()
    
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    CHECKS['api'].append(check_mark(True, "Health endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Health endpoint: {e}"))

try:
    response = client.get('/api/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_nodes' in data
    CHECKS['api'].append(check_mark(True, "Stats endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Stats endpoint: {e}"))

try:
    response = client.get('/api/nodes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'nodes' in data
    CHECKS['api'].append(check_mark(True, "Nodes endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Nodes endpoint: {e}"))

try:
    response = client.get('/api/nodes/R1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 'R1'
    CHECKS['api'].append(check_mark(True, "Node details endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Node details endpoint: {e}"))

try:
    response = client.get('/api/routes')
    assert response.status_code == 200
    CHECKS['api'].append(check_mark(True, "Routes endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Routes endpoint: {e}"))

try:
    response = client.post('/api/optimize',
                          json={'source': 'R1', 'destination': 'C1'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    CHECKS['api'].append(check_mark(True, "Optimize endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Optimize endpoint: {e}"))

try:
    response = client.post('/api/route-details',
                          json={'source': 'R1', 'destination': 'C1'},
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    CHECKS['api'].append(check_mark(True, "Route details endpoint"))
except Exception as e:
    CHECKS['api'].append(check_mark(False, f"Route details endpoint: {e}"))

# SECTION 5: UI/Frontend Verification
print_section("5. User Interface")

try:
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'Food Delivery' in html
    assert 'routeForm' in html
    CHECKS['ui'].append(check_mark(True, "Home page loads"))
except Exception as e:
    CHECKS['ui'].append(check_mark(False, f"Home page: {e}"))

try:
    response = client.get('/static/css/main.css')
    assert response.status_code == 200
    CHECKS['ui'].append(check_mark(True, "CSS loads"))
except Exception as e:
    CHECKS['ui'].append(check_mark(False, f"CSS loading: {e}"))

try:
    response = client.get('/static/js/main.js')
    assert response.status_code == 200
    CHECKS['ui'].append(check_mark(True, "JavaScript loads"))
except Exception as e:
    CHECKS['ui'].append(check_mark(False, f"JavaScript loading: {e}"))

# Summary Report
print_header("VERIFICATION SUMMARY")

total_checks = 0
passed_checks = 0

for category, results in CHECKS.items():
    category_title = category.replace('_', ' ').title()
    passed = sum(results)
    total = len(results)
    total_checks += total
    passed_checks += passed
    
    status = "✓ PASS" if passed == total else "✗ FAIL"
    print(f"\n{category_title:<25} {passed:>2}/{total:<2} {status}")

print("\n" + "="*70)
print(f"OVERALL: {passed_checks}/{total_checks} checks passed")
print("="*70)

if passed_checks == total_checks:
    print("\n✓ ALL VERIFICATION CHECKS PASSED!")
    print("\nThe project is ready for production deployment.")
    print("\nTo start the server:")
    print("  cd src")
    print("  python app.py")
    print("\nAccess at: http://localhost:5000")
    print("\n" + "="*70 + "\n")
    sys.exit(0)
else:
    print(f"\n✗ {total_checks - passed_checks} check(s) failed")
    print("Please review the errors above.")
    print("\n" + "="*70 + "\n")
    sys.exit(1)
