#!/usr/bin/env pwsh
<#
    Food Delivery Route Optimization - PowerShell Startup Script
#>

Write-Host "`n" -NoNewline
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " 🚚 Food Delivery Route Optimization System" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n"

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Check Python installation
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python.exe --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "`n[2/4] Installing dependencies..." -ForegroundColor Yellow
python.exe -m pip install -q -r "$scriptDir\requirements.txt"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green

# Run tests
Write-Host "`n[3/4] Running tests and demo..." -ForegroundColor Yellow
python.exe "$scriptDir\demo.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Tests failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start server
Write-Host "`n[4/4] Starting Flask server..." -ForegroundColor Yellow
Write-Host "`n" -NoNewline
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Server starting at http://localhost:5000" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "`n"
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "`n"

Set-Location "$scriptDir\src"
python.exe app.py
