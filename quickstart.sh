#!/bin/bash

# Virtual Try-On AI - Quick Start Script
# This script helps you get started quickly with the project

set -e

echo "=========================================="
echo "Virtual Try-On AI - Quick Start"
echo "=========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if command_exists docker && command_exists docker-compose; then
    echo "✓ Docker and Docker Compose found"
    HAS_DOCKER=true
else
    echo "✗ Docker not found. Will use manual setup."
    HAS_DOCKER=false
fi

if command_exists python3; then
    echo "✓ Python3 found"
    HAS_PYTHON=true
else
    echo "✗ Python3 not found"
    HAS_PYTHON=false
fi

if command_exists node; then
    echo "✓ Node.js found"
    HAS_NODE=true
else
    echo "✗ Node.js not found"
    HAS_NODE=false
fi

echo ""
echo "Choose setup method:"
echo "1) Docker (recommended - requires Docker)"
echo "2) Manual setup (requires Python 3.11+ and Node.js 18+)"
echo "3) Backend only"
echo "4) Frontend only"
echo "5) Run tests only"
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        if [ "$HAS_DOCKER" = false ]; then
            echo "Error: Docker not found. Please install Docker first."
            exit 1
        fi
        echo ""
        echo "Starting with Docker..."
        docker-compose up -d
        echo ""
        echo "✓ Services started!"
        echo "  Backend API: http://localhost:8000/docs"
        echo "  Frontend Dashboard: http://localhost:3000"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        ;;
    
    2)
        if [ "$HAS_PYTHON" = false ] || [ "$HAS_NODE" = false ]; then
            echo "Error: Python or Node.js not found."
            exit 1
        fi
        
        echo ""
        echo "Setting up backend..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✓ Backend dependencies installed"
        
        echo ""
        echo "Starting backend in background..."
        nohup python run.py > ../backend.log 2>&1 &
        BACKEND_PID=$!
        echo "Backend PID: $BACKEND_PID"
        cd ..
        
        echo ""
        echo "Setting up frontend..."
        cd frontend
        npm install
        echo "✓ Frontend dependencies installed"
        
        echo ""
        echo "Starting frontend in background..."
        nohup npm run dev > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo "Frontend PID: $FRONTEND_PID"
        cd ..
        
        echo ""
        echo "✓ Services started!"
        echo "  Backend API: http://localhost:8000/docs"
        echo "  Frontend Dashboard: http://localhost:3000"
        echo ""
        echo "Process IDs saved to .pids file"
        echo "$BACKEND_PID" > .pids
        echo "$FRONTEND_PID" >> .pids
        echo ""
        echo "To stop: kill \$(cat .pids)"
        ;;
    
    3)
        if [ "$HAS_PYTHON" = false ]; then
            echo "Error: Python not found."
            exit 1
        fi
        
        echo ""
        echo "Setting up backend..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✓ Backend dependencies installed"
        
        echo ""
        echo "Starting backend..."
        python run.py
        ;;
    
    4)
        if [ "$HAS_NODE" = false ]; then
            echo "Error: Node.js not found."
            exit 1
        fi
        
        echo ""
        echo "Setting up frontend..."
        cd frontend
        npm install
        echo "✓ Frontend dependencies installed"
        
        echo ""
        echo "Starting frontend..."
        npm run dev
        ;;
    
    5)
        if [ "$HAS_PYTHON" = false ]; then
            echo "Error: Python not found."
            exit 1
        fi
        
        echo ""
        echo "Setting up test environment..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        
        echo ""
        echo "Running tests..."
        pytest
        
        echo ""
        echo "✓ All tests completed!"
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
