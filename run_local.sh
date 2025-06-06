#!/bin/bash
set -e

echo "============================================================="
echo "Checking virtual environment (venv)..."
echo "============================================================="

if [ ! -d "venv" ]; then
  echo "Creating virtual environment (venv)..."
  python3 -m venv venv
else
  echo "Virtual environment already exists. Skipping creation."
fi

echo "============================================================="
echo "Activating virtual environment..."
echo "============================================================="
source venv/bin/activate

echo "============================================================="
echo "Upgrading pip..."
echo "============================================================="
python -m pip install --upgrade pip

echo "============================================================="
echo "Installing dependencies from requirements.txt..."
echo "============================================================="
pip install -r requirements.txt

echo "============================================================="
echo "Installing Translation models..."
echo "============================================================="
python -c "import translation_models; translation_models.install()"

echo "============================================================="
echo "Starting FastAPI server..."
echo "============================================================="
uvicorn translate_api:app --host 0.0.0.0 --port 30001
