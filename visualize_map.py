"""
Graphical visualization of the delivery network
Displays all locations and their connections in a visual format
"""

import matplotlib.pyplot as plt
import networkx as nx
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from graph.utils import create_sample_graph


def visualize_network():
    """
    Create a visual representation of the delivery network
    """
    # Create the graph
    graph = create_sample_graph()
    
    # Create NetworkX graph for visualization
    G = nx.DiGraph()
    
    # Add nodes with their attributes
    for node_id, node_data in graph.nodes.items():
        G.add_node(node_id, **node_data)
    
    # Add edges with their attributes
    for from_node, edges_list in graph.edges.items():
        for edge_data in edges_list:
            to_node = edge_data['to']
            G.add_edge(from_node, to_node, 
                      distance=edge_data['distance'],
                      time=edge_data['time'],
                      cost=edge_data['cost'])
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 10))
    
    # Main network visualization
    ax1 = plt.subplot(1, 2, 1)
    
    # Define positions based on stages (vertical layout)
    pos = {}
    stage_nodes = {}
    
    # Group nodes by stage
    for node_id, node_data in graph.nodes.items():
        stage = node_data['stage']
        if stage not in stage_nodes:
            stage_nodes[stage] = []
        stage_nodes[stage].append(node_id)
    
    # Assign positions: x = stage, y = distributed within stage
    for stage, nodes in stage_nodes.items():
        num_nodes = len(nodes)
        for i, node_id in enumerate(nodes):
            x = stage
            y = (num_nodes - 1) / 2 - i  # Center vertically
            pos[node_id] = (x, y)
    
    # Define colors for different stages
    stage_colors = {
        1: '#FF6B6B',      # Red for Restaurant
        2: '#4ECDC4',      # Teal for Hubs
        3: '#45B7D1',      # Blue for Zones
        4: '#FFA07A'       # Light Salmon for Customers
    }
    
    node_colors = [stage_colors[graph.nodes[node]['stage']] for node in G.nodes()]
    
    # Draw the network
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2500, ax=ax1, alpha=0.9)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                          arrowsize=20, arrowstyle='->', ax=ax1, 
                          connectionstyle='arc3,rad=0.1', width=2, alpha=0.6)
    
    # Draw labels
    labels = {node_id: f"{node_id}\n{graph.nodes[node_id]['name']}" 
              for node_id in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold', ax=ax1)
    
    # Draw edge labels (distance)
    edge_labels = {}
    for from_node, edges_list in graph.edges.items():
        for edge_data in edges_list:
            to_node = edge_data['to']
            edge_labels[(from_node, to_node)] = f"{edge_data['distance']}km\n{edge_data['time']}min"
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax1)
    
    ax1.set_title('Food Delivery Network - Full Map', fontsize=16, fontweight='bold')
    ax1.axis('off')
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Stage 1: Restaurant',
                   markerfacecolor=stage_colors[1], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Stage 2: Pickup Hub',
                   markerfacecolor=stage_colors[2], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Stage 3: Delivery Zone',
                   markerfacecolor=stage_colors[3], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Stage 4: Customer',
                   markerfacecolor=stage_colors[4], markersize=10),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Right subplot: Network Statistics
    ax2 = plt.subplot(1, 2, 2)
    ax2.axis('off')
    
    # Get graph statistics
    stats = {
        'total_nodes': len(graph.nodes),
        'total_edges': sum(len(edges_list) for edges_list in graph.edges.values()),
        'total_stages': len(set(node['stage'] for node in graph.nodes.values()))
    }
    
    # Create stats table
    stats_text = f"""
NETWORK STATISTICS
{'='*50}

Total Nodes: {stats['total_nodes']}
Total Edges: {stats['total_edges']}
Total Stages: {stats['total_stages']}

LOCATION BREAKDOWN
{'='*50}

Stage 1 - Restaurant:
  • R1: Restaurant Main

Stage 2 - Pickup Hubs:
  • H1: Hub North
  • H2: Hub South

Stage 3 - Delivery Zones:
  • Z1: Zone East
  • Z2: Zone West

Stage 4 - Customers:
  • C1: Customer A
  • C2: Customer B
  • C3: Customer C

CONNECTIONS
{'='*50}

Restaurant → Hubs: 2 connections
Hubs → Zones: 4 connections
Zones → Customers: 4 connections

Total Connections: 10 routes
    """
    
    ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save the figure
    output_path = os.path.join(os.path.dirname(__file__), 'network_map.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Network map saved to: {output_path}")
    
    # Display the figure
    plt.show()
    
    print("\n" + "="*60)
    print("FOOD DELIVERY NETWORK VISUALIZATION")
    print("="*60)
    print("\nNetwork Details:")
    print(f"  Total Nodes: {stats['total_nodes']}")
    print(f"  Total Edges: {stats['total_edges']}")
    print(f"  Total Stages: {stats['total_stages']}")
    print("\n" + "="*60)


def print_location_details():
    """
    Print detailed information about all locations
    """
    graph = create_sample_graph()
    
    print("\n" + "="*70)
    print("ALL LOCATIONS IN THE DELIVERY NETWORK")
    print("="*70)
    
    # Group by stage
    stages = {}
    for node_id, node_data in graph.nodes.items():
        stage = node_data['stage']
        if stage not in stages:
            stages[stage] = []
        stages[stage].append((node_id, node_data))
    
    stage_names = {
        1: "STAGE 1: RESTAURANT (ORDER SOURCE)",
        2: "STAGE 2: PICKUP HUBS (DISTRIBUTION CENTERS)",
        3: "STAGE 3: DELIVERY ZONES (REGIONAL AREAS)",
        4: "STAGE 4: CUSTOMERS (DELIVERY DESTINATIONS)"
    }
    
    for stage in sorted(stages.keys()):
        print(f"\n{stage_names.get(stage, f'STAGE {stage}')}")
        print("-" * 70)
        for node_id, node_data in stages[stage]:
            print(f"  [{node_id}] {node_data['name']}")
    
    # Print all connections
    print("\n" + "="*70)
    print("ALL CONNECTIONS AND ROUTES")
    print("="*70)
    
    for from_node in sorted(graph.edges.keys()):
        print(f"\nFrom {from_node} ({graph.nodes[from_node]['name']}):")
        for edge_data in sorted(graph.edges[from_node], key=lambda x: x['to']):
            to_node = edge_data['to']
            print(f"  → {to_node} ({graph.nodes[to_node]['name']})")
            print(f"      Distance: {edge_data['distance']} km")
            print(f"      Time: {edge_data['time']} minutes")
            print(f"      Cost: ${edge_data['cost']}")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    print("Generating Food Delivery Network Visualization...\n")
    
    # Print location details
    print_location_details()
    
    # Create visualization
    visualize_network()
    
    print("\n✓ Visualization complete!")
    print("  The network map has been saved and displayed.")
