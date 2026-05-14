"""
API Routes for Food Delivery Route Optimization
"""

from flask import Blueprint, request, jsonify
from services.optimizer import DeliveryOptimizer, get_optimizer

api_bp = Blueprint('api', __name__)

# Get optimizer instance
optimizer = get_optimizer()


@api_bp.route('/optimize', methods=['POST'])
def optimize_route():
    """
    POST /api/optimize
    
    Optimize delivery route between two nodes
    
    Request JSON:
    {
        "source": "node_id",
        "destination": "node_id"
    }
    
    Response:
    {
        "success": true,
        "route": [...],
        "total_distance": 10.5,
        "total_time": 20.5
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'Request body must be JSON'}), 400
        
        source = data.get('source', '').strip()
        destination = data.get('destination', '').strip()
        
        if not source or not destination:
            return jsonify({'success': False, 'error': 'source and destination are required'}), 400
        
        if source == destination:
            return jsonify({'success': False, 'error': 'Source and destination must be different'}), 400
        
        # Optimize route (handles validation internally)
        result = optimizer.optimize_route(source, destination)
        
        if not result.get('success'):
            return jsonify(result), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@api_bp.route('/nodes', methods=['GET'])
def get_all_nodes():
    """
    GET /api/nodes
    
    Get all available nodes in the graph
    
    Response:
    {
        "nodes": {
            "R1": {"stage": 1, "name": "Restaurant Main"},
            ...
        }
    }
    """
    try:
        nodes = optimizer.get_all_nodes()
        return jsonify({
            'nodes': nodes,
            'total': len(nodes)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/nodes/<node_id>', methods=['GET'])
def get_node_details(node_id):
    """
    GET /api/nodes/<node_id>
    
    Get details of a specific node
    
    Response:
    {
        "id": "R1",
        "stage": 1,
        "name": "Restaurant Main"
    }
    """
    try:
        node_info = optimizer.get_node_info(node_id)
        
        if not node_info:
            return jsonify({'error': f'Node "{node_id}" not found'}), 404
        
        return jsonify(node_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/routes', methods=['GET'])
def get_available_routes():
    """
    GET /api/routes
    
    Get all available routes organized by stage
    
    Response:
    {
        "stage_1": ["R1"],
        "stage_2": ["H1", "H2"],
        ...
    }
    """
    try:
        routes = optimizer.get_available_routes()
        return jsonify(routes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/route-details', methods=['POST'])
def get_route_details():
    """
    POST /api/route-details
    
    Get detailed route information including edges
    
    Request JSON:
    {
        "source": "node_id",
        "destination": "node_id"
    }
    
    Response:
    {
        "success": true,
        "route": [...],
        "total_distance": 10.5,
        "total_time": 20.5,
        "edges": [...]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        source = data.get('source', '').strip()
        destination = data.get('destination', '').strip()
        
        if not source or not destination:
            return jsonify({'error': 'source and destination are required'}), 400
        
        if not optimizer.validate_node(source):
            return jsonify({'error': f'Source node "{source}" not found'}), 404
        
        if not optimizer.validate_node(destination):
            return jsonify({'error': f'Destination node "{destination}" not found'}), 404
        
        result = optimizer.get_route_details(source, destination)
        
        if not result.get('success'):
            return jsonify(result), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stats', methods=['GET'])
def get_graph_stats():
    """
    GET /api/stats
    
    Get graph statistics
    
    Response:
    {
        "total_nodes": 9,
        "total_stages": 4,
        "total_edges": 12,
        "stages": {"1": 1, "2": 2, "3": 2, "4": 3}
    }
    """
    try:
        stats = optimizer.get_graph_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health
    
    Health check endpoint
    """
    try:
        stats = optimizer.get_graph_stats()
        return jsonify({
            'status': 'healthy',
            'graph_loaded': stats['total_nodes'] > 0
        }), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500