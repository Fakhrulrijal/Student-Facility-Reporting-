@echo off
title Backend FastAPI - Student Facility Reporting
cd /d "D:\Semester 5\Tugas pak mansyur\tugas5modul"
echo ============================================================
echo Menjalankan Backend FastAPI pada http://127.0.0.1:8000
echo Swagger UI Docs: http://127.0.0.1:8000/docs
echo ============================================================
python -m uvicorn --app-dir backend main:app --host 0.0.0.0 --port 8000 --reload
pause
