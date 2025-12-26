@echo off
echo Installing requirements...
python -m pip install flask
echo Starting SAN Store Server...
echo Go to http://localhost:8000
python app.py
pause
