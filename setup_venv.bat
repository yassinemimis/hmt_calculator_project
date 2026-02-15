@echo off
echo ========================================
echo Configuration Environnement Virtuel
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe!
    echo Telechargez Python sur https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python detecte: 
python --version
echo.

REM Vérifier si venv existe déjà
if exist ".venv\" (
    echo Un environnement virtuel existe deja.
    choice /C YN /M "Voulez-vous le supprimer et recreer"
    if errorlevel 2 goto :skip_create
    if errorlevel 1 (
        echo Suppression de l'ancien environnement...
        rmdir /s /q venv
    )
)

:create_venv
echo Creation de l'environnement virtuel...
python -m venv .venv

if errorlevel 1 (
    echo ERREUR lors de la creation de l'environnement virtuel
    pause
    exit /b 1
)

echo.
echo Environnement virtuel cree avec succes!
echo.

:skip_create

echo Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERREUR lors de l'activation
    pause
    exit /b 1
)

echo.
echo Mise a jour de pip...
python -m pip install --upgrade pip --quiet

echo.
echo Installation des dependances du projet...
pip install -e ".[dev]" --quiet

if errorlevel 1 (
    echo ERREUR lors de l'installation
    pause
    exit /b 1
)

echo.
echo ========================================
echo Configuration terminee avec succes!
echo ========================================
echo.
echo Pour activer l'environnement a l'avenir:
echo   .venv\Scripts\activate
echo.
echo Pour lancer l'application:
echo   python main.py
echo.
echo Pour desactiver l'environnement:
echo   deactivate
echo.
pause