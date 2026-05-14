# 🚚 Food Delivery Route Optimization Using Multistage Graph

A complete web application for optimizing food delivery routes using a **multistage graph** approach with the **forward algorithm**. Built with Flask, Python, and NetworkX.

## 📋 Overview

This project demonstrates an optimal solution for finding the shortest delivery route through multiple stages:

```
Restaurant → Pickup Hub → Delivery Zone → Customer
    (S1)        (S2)          (S3)          (S4)
```

The algorithm uses **Dijkstra's shortest path** to find the optimal route considering distance, time, and cost.

## ✨ Features

- ✅ **Multistage Graph Implementation** - Organized delivery checkpoints in stages
- ✅ **Forward Approach Algorithm** - Dijkstra's shortest path computation
- ✅ **RESTful API** - Complete API for route optimization
- ✅ **Modern Web UI** - Interactive and responsive frontend
- ✅ **Comprehensive Testing** - Unit tests for all core components
- ✅ **Docker Support** - Ready to deploy with Docker
- ✅ **Error Handling** - Robust error management and validation

## 📁 Project Structure

```
food-delivery-route-optimization/
├── src/
│   ├── app.py                          # Flask application entry point
│   ├── config.py                       # Configuration management
│   ├── graph/
│   │   ├── multistage.py              # Core multistage graph class
│   │   └── utils.py                   # Graph utility functions
│   ├── models/
│   │   └── order.py                   # Order data model
│   ├── routes/
│   │   ├── api.py                     # REST API endpoints
│   │   └── __init__.py
│   ├── services/
│   │   ├── optimizer.py               # Route optimization service
│   │   └── __init__.py
│   ├── templates/
│   │   └── index.html                 # Frontend HTML template
│   └── static/
│       ├── css/main.css               # Styling
│       └── js/main.js                 # Frontend logic
├── tests/
│   ├── test_graph.py                  # Graph unit tests
│   └── test_optimizer.py              # Optimizer unit tests
├── requirements.txt                    # Python dependencies
├── pyproject.toml                      # Project configuration
├── .env                                # Environment variables
├── Dockerfile                          # Docker configuration
├── docker-compose.yml                  # Docker Compose configuration
└── README.md                           # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd d:\25mx103\food-delivery-route-optimization
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD)**:
     ```cmd
     venv\Scripts\activate
     ```
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

### Development Mode

1. **Start the Flask application**:
   ```bash
   cd src
   python app.py
   ```

2. **Open in browser**:
   - Navigate to `http://localhost:5000`

### With Docker

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - Open `http://localhost:5000` in your browser

## 🧪 Running Tests

### Run all tests:
```bash
cd src
python -m pytest ../tests/ -v
```

### Run specific test file:
```bash
python -m pytest ../tests/test_graph.py -v
python -m pytest ../tests/test_optimizer.py -v
```

### Run with coverage:
```bash
python -m pytest ../tests/ --cov=. -v
```

## 📊 API Documentation

### Base URL: `/api`

#### 1. **Optimize Route**
- **Endpoint**: `POST /api/optimize`
- **Description**: Find the shortest route between two nodes
- **Request**:
  ```json
  {
    "source": "R1",
    "destination": "C1"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "route": [
      {"step": 1, "node_id": "R1", "stage": 1, "name": "Restaurant Main"},
      {"step": 2, "node_id": "H1", "stage": 2, "name": "Hub North"},
      {"step": 3, "node_id": "Z1", "stage": 3, "name": "Zone East"},
      {"step": 4, "node_id": "C1", "stage": 4, "name": "Customer A"}
    ],
    "total_distance": 10.5,
    "total_time": 23.0,
    "total_steps": 4
  }
  ```

#### 2. **Get All Nodes**
- **Endpoint**: `GET /api/nodes`
- **Response**:
  ```json
  {
    "nodes": {
      "R1": {"stage": 1, "name": "Restaurant Main"},
      "H1": {"stage": 2, "name": "Hub North"},
      ...
    },
    "total": 9
  }
  ```

#### 3. **Get Node Details**
- **Endpoint**: `GET /api/nodes/<node_id>`
- **Response**:
  ```json
  {
    "id": "R1",
    "stage": 1,
    "name": "Restaurant Main"
  }
  ```

#### 4. **Get Available Routes**
- **Endpoint**: `GET /api/routes`
- **Response**:
  ```json
  {
    "stage_1": ["R1"],
    "stage_2": ["H1", "H2"],
    "stage_3": ["Z1", "Z2"],
    "stage_4": ["C1", "C2", "C3"]
  }
  ```

#### 5. **Get Route Details**
- **Endpoint**: `POST /api/route-details`
- **Description**: Get detailed information about edges in the route
- **Request**:
  ```json
  {
    "source": "R1",
    "destination": "C1"
  }
  ```

#### 6. **Get Graph Statistics**
- **Endpoint**: `GET /api/stats`
- **Response**:
  ```json
  {
    "total_nodes": 9,
    "total_stages": 4,
    "total_edges": 12,
    "stages": {"1": 1, "2": 2, "3": 2, "4": 3}
  }
  ```

#### 7. **Health Check**
- **Endpoint**: `GET /api/health`
- **Response**:
  ```json
  {
    "status": "healthy",
    "graph_loaded": true
  }
  ```

## 🔧 Configuration

### Environment Variables (.env)
```
DEBUG=True                          # Enable debug mode
TESTING=False                       # Disable testing mode
SECRET_KEY=food-delivery-secret-key # Secret key for Flask
FLASK_ENV=development               # Environment type
PORT=5000                           # Server port
```

## 🎓 Algorithm Details

### Multistage Graph
- **Stages**: 1 to N (typically 4: Restaurant → Hub → Zone → Customer)
- **Nodes**: Locations at each stage
- **Edges**: Routes with distance, time, and cost

### Forward Approach (Dijkstra's Algorithm)
1. Initialize all nodes with infinite distance
2. Set source distance to 0
3. Use priority queue to process nodes in order of distance
4. Update neighbors when shorter paths are found
5. Reconstruct path from source to destination

**Time Complexity**: O((V + E) log V)
**Space Complexity**: O(V)

## 📈 Sample Graph

### Nodes:
- **Stage 1**: R1 (Restaurant)
- **Stage 2**: H1 (Hub North), H2 (Hub South)
- **Stage 3**: Z1 (Zone East), Z2 (Zone West)
- **Stage 4**: C1, C2, C3 (Customers)

### Sample Route:
```
Restaurant (R1) → Hub North (H1) → Zone East (Z1) → Customer A (C1)
Distance: 10 km | Time: 23 minutes
```

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Ensure you're in the `src` directory or add the path to PYTHONPATH:
```bash
set PYTHONPATH=%cd%\src
```

### Issue: Port 5000 already in use
**Solution**: Change the port in `.env` or run:
```bash
python app.py --port 5001
```

### Issue: Tests not running
**Solution**: Install pytest:
```bash
pip install pytest pytest-cov
```

## 📚 Dependencies

- **Flask** (2.3.3) - Web framework
- **NetworkX** (3.1) - Graph algorithms
- **python-dotenv** (1.0.0) - Environment variable management
- **pytest** (7.4.0) - Testing framework

## 🎯 Use Cases

1. **Food Delivery Services** - Optimize delivery routes
2. **Logistics** - Find efficient paths through distribution networks
3. **Supply Chain** - Optimize multi-stage logistics
4. **GPS Navigation** - Multi-waypoint route planning

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Built as an AI-assisted development project for educational purposes.

## 📞 Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Last Updated**: May 2025  
**Status**: Production Ready ✅
   ```
   git clone <repository-url>
   cd food-delivery-route-optimization
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in the `.env` file as needed.

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Access the application in your web browser at `http://localhost:5000`.

## Testing

To run the tests, use:
```
pytest tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.