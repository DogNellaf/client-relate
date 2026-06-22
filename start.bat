@echo off

set VENV_DIR=.venv

if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

call %VENV_DIR%\Scripts\activate

if exist requirements.txt (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
)

echo Starting Django development server...
python manage.py runserver

deactivate

pause
