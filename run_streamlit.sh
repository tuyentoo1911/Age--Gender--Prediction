#!/bin/bash

echo "🤖 Starting AI Age & Gender Prediction Streamlit App..."
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${GREEN}[INFO]${NC} Activating virtual environment..."
    source venv/bin/activate
else
    echo -e "${YELLOW}[WARNING]${NC} Virtual environment not found. Using global Python."
fi

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo -e "${RED}[ERROR]${NC} app.py not found in current directory!"
    exit 1
fi

# Check if model files exist
if [ ! -f "models/best_age_model.h5" ] && [ ! -f "best_age_model.h5" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Age model file not found!"
    echo "Please ensure you have models/best_age_model.h5 or best_age_model.h5"
fi

if [ ! -f "models/best_gender_model.h5" ] && [ ! -f "best_gender_model.h5" ]; then
    echo -e "${YELLOW}[WARNING]${NC} Gender model file not found!"
    echo "Please ensure you have models/best_gender_model.h5 or best_gender_model.h5"
fi

echo -e "${GREEN}[INFO]${NC} Starting Streamlit server..."
echo -e "${GREEN}[INFO]${NC} App will open at: http://localhost:8501"
echo

# Run Streamlit app
streamlit run app.py --server.port 8501 --server.headless false

echo
echo "App stopped." 