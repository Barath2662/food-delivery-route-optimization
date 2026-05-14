/**
 * Food Delivery Route Optimization - Frontend JavaScript
 * Handles user interactions and API communication
 */

const API_BASE = '/api';

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Application initialized');
    
    // Load initial data
    loadGraphStats();
    loadAvailableNodes();
    
    // Set up form handler
    const form = document.getElementById('routeForm');
    if (form) {
        form.addEventListener('submit', handleRouteSubmit);
    }
});

/**
 * Load and display graph statistics
 */
async function loadGraphStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('totalNodes').textContent = data.total_nodes;
            document.getElementById('totalStages').textContent = data.total_stages;
            document.getElementById('totalEdges').textContent = data.total_edges;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

/**
 * Load available nodes and populate dropdowns
 */
async function loadAvailableNodes() {
    try {
        const response = await fetch(`${API_BASE}/nodes`);
        const data = await response.json();
        
        if (response.ok && data.nodes) {
            populateDropdowns(data.nodes);
        }
    } catch (error) {
        console.error('Error loading nodes:', error);
    }
}

/**
 * Populate source and destination dropdowns with available nodes
 */
function populateDropdowns(nodes) {
    const sourceSelect = document.getElementById('source');
    const destSelect = document.getElementById('destination');
    
    // Clear existing options (keep placeholder)
    while (sourceSelect.options.length > 1) {
        sourceSelect.remove(1);
    }
    while (destSelect.options.length > 1) {
        destSelect.remove(1);
    }
    
    // Add nodes as options
    Object.entries(nodes).forEach(([nodeId, nodeInfo]) => {
        const option1 = document.createElement('option');
        option1.value = nodeId;
        option1.textContent = `${nodeId} - ${nodeInfo.name} (Stage ${nodeInfo.stage})`;
        sourceSelect.appendChild(option1);
        
        const option2 = document.createElement('option');
        option2.value = nodeId;
        option2.textContent = `${nodeId} - ${nodeInfo.name} (Stage ${nodeInfo.stage})`;
        destSelect.appendChild(option2);
    });
}

/**
 * Handle route form submission
 */
async function handleRouteSubmit(event) {
    event.preventDefault();
    
    const source = document.getElementById('source').value.trim();
    const destination = document.getElementById('destination').value.trim();
    const resultDiv = document.getElementById('result');
    const detailsSection = document.getElementById('detailsSection');
    
    // Validation
    if (!source) {
        showError(resultDiv, 'Please select a source node');
        return;
    }
    
    if (!destination) {
        showError(resultDiv, 'Please select a destination node');
        return;
    }
    
    if (source === destination) {
        showError(resultDiv, 'Source and destination must be different');
        return;
    }
    
    // Show loading state
    resultDiv.innerHTML = '<div class="loading"></div> Finding optimal route...';
    detailsSection.style.display = 'none';
    
    try {
        // Fetch route optimization
        const response = await fetch(`${API_BASE}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: source,
                destination: destination
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayResult(data, resultDiv);
            
            // Fetch detailed route information
            fetchRouteDetails(source, destination, detailsSection);
        } else {
            const errorMsg = data.error || data.message || 'Failed to optimize route';
            showError(resultDiv, errorMsg);
        }
    } catch (error) {
        console.error('Error:', error);
        showError(resultDiv, `Error: ${error.message}`);
    }
}

/**
 * Display route result
 */
function displayResult(data, container) {
    if (!data.success) {
        showError(container, data.message || 'No route found');
        return;
    }
    
    let html = '<div class="success">';
    html += '<strong>✓ Route Found!</strong><br><br>';
    html += '<div class="route-info">';
    html += `<div class="info-box">
        <div class="info-box-label">Total Distance</div>
        <div class="info-box-value">${data.total_distance} km</div>
    </div>`;
    html += `<div class="info-box">
        <div class="info-box-label">Estimated Time</div>
        <div class="info-box-value">${data.total_time} min</div>
    </div>`;
    html += `<div class="info-box">
        <div class="info-box-label">Total Steps</div>
        <div class="info-box-value">${data.total_steps}</div>
    </div>`;
    html += '</div>';
    
    // Display route steps
    html += '<div class="route-steps">';
    html += '<h3>🗺️ Route Path</h3>';
    
    data.route.forEach((step, index) => {
        html += `<div class="step">
            <div class="step-number">${step.step}</div>
            <div class="step-content">
                <div class="step-name">${step.name} (${step.node_id})</div>
                <div class="step-stage">Stage ${step.stage}</div>
            </div>`;
        
        if (index < data.route.length - 1) {
            html += '<div class="arrow">→</div>';
        }
        
        html += '</div>';
    });
    
    html += '</div>';
    html += '</div>';
    
    container.innerHTML = html;
}

/**
 * Fetch and display detailed route information
 */
async function fetchRouteDetails(source, destination, container) {
    try {
        const response = await fetch(`${API_BASE}/route-details`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source: source,
                destination: destination
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success && data.edges && data.edges.length > 0) {
            displayRouteDetails(data.edges, container);
        }
    } catch (error) {
        console.error('Error fetching route details:', error);
    }
}

/**
 * Display detailed edge information
 */
function displayRouteDetails(edges, container) {
    let html = '';
    
    edges.forEach((edge, index) => {
        html += `<div class="edge-detail">
            <div class="edge-item">
                <div class="edge-item-label">Step ${index + 1}</div>
                <div class="edge-item-value">${edge.from} → ${edge.to}</div>
            </div>
            <div class="edge-item">
                <div class="edge-item-label">Distance</div>
                <div class="edge-item-value">${edge.distance} km</div>
            </div>
            <div class="edge-item">
                <div class="edge-item-label">Time</div>
                <div class="edge-item-value">${edge.time} min</div>
            </div>
            <div class="edge-item">
                <div class="edge-item-label">Cost</div>
                <div class="edge-item-value">₹${edge.cost}</div>
            </div>
        </div>`;
    });
    
    container.innerHTML = html;
    container.parentElement.style.display = 'block';
}

/**
 * Show error message
 */
function showError(container, message) {
    const errorClass = message.includes('stage') || message.includes('forward') ? 'error-warning' : 'error';
    container.innerHTML = `<div class="${errorClass}">
        <strong>⚠️ Error:</strong> ${message}
    </div>`;
}