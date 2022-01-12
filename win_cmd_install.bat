@echo off
echo Installing dependency libraries...
timeout /t 1 /nobreak > nul
pip install discord
cls
echo Library Installation Complete! 1 library successfully installed. Press any key to exit.
pause > nul
exit /b
