# 🚀 Installation & Setup Guide

## Quick Start (Recommended)

### Windows Users

#### Option 1: Batch File (Simplest)
```batch
run.bat
```

#### Option 2: PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\run.ps1
```

#### Option 3: Manual Steps
1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```cmd
   cd d:\25mx103\food-delivery-route-optimization
   ```
3. Create virtual environment:
   ```cmd
   python -m venv venv
   ```
4. Activate virtual environment:
   - **Command Prompt**:
     ```cmd
     venv\Scripts\activate
     ```
   - **PowerShell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
6. Run the demo (optional):
   ```cmd
   python demo.py
   ```
7. Start the server:
   ```cmd
   cd src
   python app.py
   ```
8. Open browser:
   - Navigate to `http://localhost:5000`

### Linux/macOS Users

1. Navigate to project:
   ```bash
   cd /path/to/food-delivery-route-optimization
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run demo (optional):
   ```bash
   python demo.py
   ```

6. Start server:
   ```bash
   cd src
   python app.py
   ```

7. Open browser:
   - Navigate to `http://localhost:5000`

## Verify Installation

### Test 1: Check Python
```bash
python --version
```
Should show Python 3.8 or higher.

### Test 2: Check Dependencies
```bash
python -c "import flask; import networkx; print('All dependencies OK')"
```

### Test 3: Run Demo
```bash
python demo.py
```
Should show successful test output.

### Test 4: Run Unit Tests
```bash
python -m pytest tests/ -v
```

## Docker Setup (Alternative)

### Build and Run with Docker Compose
```bash
docker-compose up --build
```

Access at: http://localhost:5000

### Build Docker Image Manually
```bash
docker build -t food-delivery-optimizer .
docker run -p 5000:5000 food-delivery-optimizer
```

## Troubleshooting

### Issue: "Python not found"
**Solution**: 
- Add Python to PATH
- Or use full path: `C:\Python39\python.exe`
- Or reinstall Python with "Add Python to PATH" checked

### Issue: "Module not found"
**Solution**:
```bash
# Ensure you're in the right directory
cd src

# Or add to PYTHONPATH (Windows)
set PYTHONPATH=%cd%

# Or add to PYTHONPATH (Linux/macOS)
export PYTHONPATH=$PWD
```

### Issue: "Port 5000 already in use"
**Solution 1**: Kill existing process
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>
```

**Solution 2**: Use different port
```bash
# In src/app.py, change: app.run(port=5001)
```

### Issue: Permission denied on run.ps1
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\run.ps1
```

## System Requirements

### Minimum
- Python 3.8+
- 100 MB disk space
- 256 MB RAM

### Recommended
- Python 3.10+
- 500 MB disk space
- 1 GB RAM

### Dependencies (Auto-installed)
- Flask 2.3.3
- NetworkX 3.1
- matplotlib 3.7.1
- python-dotenv 1.0.0
- pytest 7.4.0
- Werkzeug 2.3.7

## Virtual Environment Management

### Create
```bash
python -m venv venv
```

### Activate
- Windows CMD: `venv\Scripts\activate`
- Windows PS: `.\venv\Scripts\Activate.ps1`
- Linux/Mac: `source venv/bin/activate`

### Deactivate
```bash
deactivate
```

### Delete
```bash
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv
```

## Development Setup

### Install with Development Dependencies
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

### Code Quality Tools
```bash
# Format code
black src/

# Lint code
flake8 src/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

## Common Commands

```bash
# Start development server
cd src
python app.py

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_graph.py -v

# Run demo/verification
python demo.py

# Install all requirements
pip install -r requirements.txt

# Check installed packages
pip list

# Upgrade Flask
pip install --upgrade Flask

# Generate requirements from current environment
pip freeze > requirements.txt
```

## Environment Variables

Create `.env` file in project root:

```
DEBUG=True
TESTING=False
SECRET_KEY=your-secret-key
FLASK_ENV=development
PORT=5000
```

## Support & Help

If you encounter issues:

1. **Check Python version**: `python --version` (should be 3.8+)
2. **Check dependencies**: `pip list`
3. **Review error message**: Often indicates the solution
4. **Run demo**: `python demo.py` helps identify the issue
5. **Check virtual environment**: Ensure it's activated
6. **Check firewall**: Port 5000 might be blocked

## Next Steps

1. ✅ Installation complete!
2. 📖 Read [README.md](README.md) for project overview
3. 🌐 Open http://localhost:5000 in browser
4. 🧪 Run tests: `python -m pytest tests/ -v`
5. 📝 Explore the code in `src/` directory

## File Permissions

If you get permission errors on Linux/macOS:

```bash
chmod +x run.ps1
chmod +x run.bat
chmod -R +x src/
```

---

**Installation Guide Version**: 1.0  
**Last Updated**: May 2025
