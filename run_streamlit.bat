@echo off
echo 🤖 Starting AI Age & Gender Prediction Streamlit App...
echo ================================================

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment not found. Using global Python.
)

REM Check if app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found in current directory!
    pause
    exit /b 1
)

REM Check if model files exist
if not exist "models\best_age_model.h5" (
    if not exist "best_age_model.h5" (
        echo [WARNING] Age model file not found!
        echo Please ensure you have models\best_age_model.h5 or best_age_model.h5
    )
)

if not exist "models\best_gender_model.h5" (
    if not exist "best_gender_model.h5" (
        echo [WARNING] Gender model file not found!
        echo Please ensure you have models\best_gender_model.h5 or best_gender_model.h5
    )
)

echo [INFO] Starting Streamlit server...
echo [INFO] App will open at: http://localhost:8501
echo.

REM Run Streamlit app
streamlit run app.py --server.port 8501 --server.headless false

echo.
echo App stopped. Press any key to exit...
pause 