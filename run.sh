#!/usr/bin/env bash
# ==============================================================================
# Breast Cancer AI Diagnostic Platform - Universal macOS / Linux Runner
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "🎗️  Breast Cancer AI Diagnostic Platform - Launching..."
echo "======================================================================"

# 1. Check Python installation
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python 3 is not installed or not in your PATH."
    echo "Please install Python 3.9 - 3.12 from https://www.python.org/"
    exit 1
fi

PY_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Detected Python version: $PY_VERSION"

# 2. Setup Virtual Environment if missing
if [ ! -d ".venv" ]; then
    echo "📦 Initializing virtual environment in .venv..."
    $PYTHON_CMD -m venv .venv
    echo "✓ Virtual environment created."
    
    echo "📥 Installing required dependencies from requirements.txt..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
    echo "✓ Dependencies installed."
fi

# 3. Guard: Remove pyarrow if installed on macOS to prevent SIGABRT mutex clash
if .venv/bin/pip list 2>/dev/null | grep -q "pyarrow"; then
    echo "⚠️  Detected pyarrow (known macOS C++ mutex clash with TensorFlow). Removing..."
    .venv/bin/pip uninstall -y pyarrow >/dev/null 2>&1 || true
fi

# 4. Generate sample scans if missing
if [ ! -d "sample_scans" ] || [ ! -f "sample_scans/benign_scan_01_fibroadenoma.png" ]; then
    echo "🧪 Generating sample test scans..."
    .venv/bin/python generate_sample_data.py
fi

# 5. Launch Streamlit Dashboard
echo ""
echo "🚀 Starting Streamlit Web App on http://localhost:8501"
echo "Press Ctrl+C to stop the server anytime."
echo "======================================================================"
exec .venv/bin/streamlit run app.py --server.port 8501

