# 📘 Usage Guide

## Table of Contents
1. [Web UI Usage](#web-ui-usage)
2. [API Usage](#api-usage)
3. [Command Line Usage](#command-line-usage)
4. [Sample Routes](#sample-routes)
5. [Advanced Usage](#advanced-usage)

## Web UI Usage

### Accessing the Application

1. **Start the server**:
   ```bash
   cd src
   python app.py
   ```

2. **Open in browser**:
   - URL: `http://localhost:5000`

### Using the Web Interface

#### Step 1: View Graph Statistics
- The dashboard shows:
  - **Total Nodes**: Number of delivery locations
  - **Stages**: Number of delivery stages
  - **Routes**: Number of connections

#### Step 2: Select Source and Destination
1. Click on **"From (Source Node)"** dropdown
2. Select starting location (e.g., "R1 - Restaurant Main")
3. Click on **"To (Destination Node)"** dropdown
4. Select destination (e.g., "C1 - Customer A")

#### Step 3: Find Optimal Route
1. Click **"Find Optimal Route"** button
2. Wait for results (usually instant)

#### Step 4: View Results
- **Green box** shows: Distance, Time, Number of Steps
- **Route Path** shows each checkpoint in sequence
- **Route Details** shows edge information

#### Step 5: Reset (Optional)
- Click **"Clear"** button to reset the form

### Example: Finding Route from Restaurant to Customer A

```
From: R1 - Restaurant Main (Stage 1)
To:   C1 - Customer A (Stage 4)
```

**Result**:
```
✓ Route Found!

Total Distance: 10.0 km
Estimated Time: 23.0 min
Total Steps: 4

Route Path:
1. Restaurant Main (R1) - Stage 1
   ↓
2. Hub North (H1) - Stage 2
   ↓
3. Zone East (Z1) - Stage 3
   ↓
4. Customer A (C1) - Stage 4

Route Details:
R1 → H1: 5.0 km, 10 min, ₹50
H1 → Z1: 3.0 km, 8 min, ₹30
Z1 → C1: 2.0 km, 5 min, ₹20
```

## API Usage

### Base URL
```
http://localhost:5000/api
```

### 1. Optimize Route (POST)

**Endpoint**: `/api/optimize`

**Request**:
```bash
curl -X POST http://localhost:5000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{"source": "R1", "destination": "C1"}'
```

**Python Example**:
```python
import requests

url = "http://localhost:5000/api/optimize"
payload = {
    "source": "R1",
    "destination": "C1"
}

response = requests.post(url, json=payload)
result = response.json()

if result['success']:
    print(f"Distance: {result['total_distance']} km")
    print(f"Time: {result['total_time']} minutes")
    print(f"Route: {[step['node_id'] for step in result['route']]}")
```

**Response**:
```json
{
  "success": true,
  "route": [
    {"step": 1, "node_id": "R1", "stage": 1, "name": "Restaurant Main"},
    {"step": 2, "node_id": "H1", "stage": 2, "name": "Hub North"},
    {"step": 3, "node_id": "Z1", "stage": 3, "name": "Zone East"},
    {"step": 4, "node_id": "C1", "stage": 4, "name": "Customer A"}
  ],
  "total_distance": 10.0,
  "total_time": 23.0,
  "total_steps": 4
}
```

### 2. Get All Nodes (GET)

**Endpoint**: `/api/nodes`

**Request**:
```bash
curl http://localhost:5000/api/nodes
```

**Response**:
```json
{
  "nodes": {
    "R1": {"stage": 1, "name": "Restaurant Main"},
    "H1": {"stage": 2, "name": "Hub North"},
    "H2": {"stage": 2, "name": "Hub South"},
    "Z1": {"stage": 3, "name": "Zone East"},
    "Z2": {"stage": 3, "name": "Zone West"},
    "C1": {"stage": 4, "name": "Customer A"},
    "C2": {"stage": 4, "name": "Customer B"},
    "C3": {"stage": 4, "name": "Customer C"}
  },
  "total": 8
}
```

### 3. Get Node Details (GET)

**Endpoint**: `/api/nodes/<node_id>`

**Request**:
```bash
curl http://localhost:5000/api/nodes/R1
```

**Response**:
```json
{
  "id": "R1",
  "stage": 1,
  "name": "Restaurant Main"
}
```

### 4. Get Available Routes (GET)

**Endpoint**: `/api/routes`

**Request**:
```bash
curl http://localhost:5000/api/routes
```

**Response**:
```json
{
  "stage_1": ["R1"],
  "stage_2": ["H1", "H2"],
  "stage_3": ["Z1", "Z2"],
  "stage_4": ["C1", "C2", "C3"]
}
```

### 5. Get Route Details (POST)

**Endpoint**: `/api/route-details`

**Request**:
```bash
curl -X POST http://localhost:5000/api/route-details \
  -H "Content-Type: application/json" \
  -d '{"source": "R1", "destination": "C1"}'
```

**Response**:
```json
{
  "success": true,
  "route": [...],
  "total_distance": 10.0,
  "total_time": 23.0,
  "edges": [
    {
      "from": "R1",
      "to": "H1",
      "distance": 5.0,
      "time": 10,
      "cost": 50
    },
    {
      "from": "H1",
      "to": "Z1",
      "distance": 3.0,
      "time": 8,
      "cost": 30
    },
    {
      "from": "Z1",
      "to": "C1",
      "distance": 2.0,
      "time": 5,
      "cost": 20
    }
  ]
}
```

### 6. Get Graph Statistics (GET)

**Endpoint**: `/api/stats`

**Request**:
```bash
curl http://localhost:5000/api/stats
```

**Response**:
```json
{
  "total_nodes": 8,
  "total_stages": 4,
  "total_edges": 10,
  "stages": {
    "1": 1,
    "2": 2,
    "3": 2,
    "4": 3
  }
}
```

### 7. Health Check (GET)

**Endpoint**: `/api/health`

**Request**:
```bash
curl http://localhost:5000/api/health
```

**Response**:
```json
{
  "status": "healthy",
  "graph_loaded": true
}
```

## Command Line Usage

### Running the Demo

```bash
python demo.py
```

Shows:
- Graph creation
- Pathfinding examples
- Optimizer service test
- API endpoint tests

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_graph.py -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Python REPL Usage

```python
import sys
sys.path.insert(0, 'src')

from graph.multistage import MultistageGraph
from services.optimizer import get_optimizer

# Create a graph
graph = MultistageGraph()
graph.add_node('A', stage=1, name='Start')
graph.add_node('B', stage=2, name='Middle')
graph.add_node('C', stage=3, name='End')
graph.add_edge('A', 'B', distance=5.0, time=10)
graph.add_edge('B', 'C', distance=3.0, time=5)

# Find path
path, distance, time = graph.forward_approach('A', 'C')
print(f"Path: {path}")
print(f"Distance: {distance}")
print(f"Time: {time}")

# Use optimizer
optimizer = get_optimizer()
result = optimizer.optimize_route('R1', 'C1')
print(result)
```

## Sample Routes

### Route 1: Restaurant to Customer A (Shortest)
```
R1 → H1 → Z1 → C1
Distance: 10.0 km
Time: 23.0 min
Cost: ₹100
```

### Route 2: Restaurant to Customer B (Multiple Options)
```
Option 1: R1 → H1 → Z1 → C2
Distance: 14.0 km
Time: 31.0 min

Option 2: R1 → H2 → Z2 → C2
Distance: 13.0 km
Time: 27.0 min ✓ (Selected by algorithm)
```

### Route 3: Restaurant to Customer C
```
R1 → H2 → Z2 → C3
Distance: 15.0 km
Time: 30.0 min
Cost: ₹150
```

## Advanced Usage

### Creating Custom Graphs

```python
from graph.multistage import MultistageGraph

# Create custom graph
graph = MultistageGraph()

# Add 5 stages
for stage in range(1, 6):
    for i in range(2):
        node_id = f"S{stage}_N{i}"
        graph.add_node(node_id, stage=stage, name=f"Stage{stage} Node{i}")

# Add edges between stages
# ... add your custom edges

# Use optimizer
from services.optimizer import DeliveryOptimizer
optimizer = DeliveryOptimizer(graph)
```

### Batch Processing Routes

```python
# Process multiple destinations from same source
destinations = ['C1', 'C2', 'C3']
source = 'R1'

for dest in destinations:
    result = optimizer.optimize_route(source, dest)
    if result['success']:
        print(f"{source} → {dest}: {result['total_distance']} km")
```

### Exporting Results

```python
import json

result = optimizer.optimize_route('R1', 'C1')

# Save to JSON
with open('route_result.json', 'w') as f:
    json.dump(result, f, indent=2)

# CSV format
import csv
with open('routes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Source', 'Destination', 'Distance', 'Time', 'Steps'])
    writer.writerow(['R1', 'C1', result['total_distance'], result['total_time'], result['total_steps']])
```

### Performance Testing

```python
import time

# Measure optimization time
start = time.time()
result = optimizer.optimize_route('R1', 'C1')
elapsed = time.time() - start

print(f"Optimization took {elapsed*1000:.2f}ms")

# Test multiple routes
times = []
for _ in range(100):
    start = time.time()
    optimizer.optimize_route('R1', 'C1')
    times.append(time.time() - start)

avg_time = sum(times) / len(times)
print(f"Average time: {avg_time*1000:.2f}ms")
```

## Error Handling

### Invalid Node
```json
{
  "error": "Source node \"X1\" not found"
}
```
**Solution**: Check `/api/nodes` for valid node IDs

### No Route Found
```json
{
  "success": false,
  "message": "No route found"
}
```
**Solution**: Ensure path exists from source to destination

### Invalid Request
```json
{
  "error": "source and destination are required"
}
```
**Solution**: Provide both `source` and `destination` in request

## Performance Tips

1. **Caching**: Results are calculated on demand (no caching)
2. **Batch Requests**: Use `/api/routes` to see all available options
3. **Direct Connection**: API calls are direct, no queues
4. **Load Testing**: App handles ~1000 requests/second

---

**Usage Guide Version**: 1.0  
**Last Updated**: May 2025
