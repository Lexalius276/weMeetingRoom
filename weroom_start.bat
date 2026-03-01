@echo off
:: weRoom v2.0 — Lancement local
:: we.law — Genere le 2026-03-01
cd /d "C:\Users\ludov\Tools\Dev\weMeetingRoom"

echo.
echo  ====================================
echo   weRoom v2.0 — we.law
echo  ====================================
echo.
echo  Installation des dependances...
python -m pip install flask gunicorn --quiet
echo.
echo  Lancement du serveur...
echo  Ouvre : http://localhost:5000
echo  (Ferme cette fenetre pour arreter)
echo.

start "" /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"
python app.py
pause
