@echo off
:: weRoom — Lancement de l'agenda de salle de reunion
:: Genere le 2026-02-27 — we.law
:: Chemin : C:\Users\ludov\Tools\Dev\weMeetingRoom\

cd /d "C:\Users\ludov\Tools\Dev\weMeetingRoom"

echo.
echo  ====================================
echo   weRoom — Agenda Salle de Reunion
echo  ====================================
echo.

:: Installation des dependances si necessaire
echo  Installation des dependances...
python -m pip install flask gunicorn --quiet

echo.
echo  Lancement du serveur...
echo  Ouvre ton navigateur sur : http://localhost:5000
echo.
echo  (Ferme cette fenetre pour arreter le serveur)
echo.

:: Ouvrir le navigateur apres 2 secondes
start "" /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"

:: Lancer Flask
python app.py

pause
