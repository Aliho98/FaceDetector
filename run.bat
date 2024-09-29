@echo off

echo Running VideoFrames.py...
python VideoFrames.py

if %errorlevel% neq 0 (
    echo VideoFrames.py failed. Exiting...
    pause
    exit /b %errorlevel%
)

echo VideoFrames.py finished. Running inference.py...
python inference.py

if %errorlevel% neq 0 (
    echo inference.py failed. Exiting...
    pause
    exit /b %errorlevel%
)

echo inference.py finished. Running VideoC.py...
python VideoC.py

if %errorlevel% neq 0 (
    echo VideoC.py failed. Exiting...
    pause
    exit /b %errorlevel%
)

echo All scripts ran successfully.
pause
