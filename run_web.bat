@echo off
cd /d "%~dp0"
uvicorn webapp:app --reload
