@echo off
REM Remove .venv folder if it exists
if exist .venv rmdir /s /q .venv

REM Remove __pycache__ folder if it exists
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

REM Create a new virtual environment
python -m venv .venv

REM Activate the virtual environment
call activate.bat

REM Install the required packages
pip install -r requirements.txt
