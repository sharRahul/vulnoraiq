@echo off
REM VulnoraIQ Web UI double-click launcher for Windows.
cd /d "%~dp0"
echo Starting VulnoraIQ Web UI...
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py scripts\launch_webui.py %*
) else (
  python scripts\launch_webui.py %*
)
echo VulnoraIQ Web UI launcher has stopped.
pause
