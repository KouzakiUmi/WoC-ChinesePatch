@echo off
chcp 65001 >nul
title WoC Chinese Patch - Uninstall
where py >nul 2>nul && (set PY=py -3) || (set PY=python)
%PY% "%~dp0tools\patch_tool.py" uninstall %*
echo.
pause
