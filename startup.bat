@echo off
REM Activate Conda environment and run the Flask application
call conda activate summarizer_pro
if %ERRORLEVEL% neq 0 (
    echo Failed to activate Conda environment
    pause
    exit /b 1
)

python booksummarizerpro/app.py
if %ERRORLEVEL% neq 0 (
    echo Failed to start the Flask application
    pause
    exit /b 1
)
