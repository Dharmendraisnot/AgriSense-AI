#!/usr/bin/env bash
# AgriSense AI – Linux/macOS start script
# Run from project root:  bash run.sh

set -e

echo "🌾 Starting AgriSense AI..."

# Create venv if missing
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

# Start FastAPI backend
echo "🚀 Starting FastAPI backend on http://localhost:8000 ..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
sleep 2

# Start Streamlit frontend
echo "🌐 Starting Streamlit frontend on http://localhost:8501 ..."
streamlit run frontend/app.py

# Cleanup
kill $BACKEND_PID 2>/dev/null || true
