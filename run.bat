@echo off
echo ========================================
echo    Bot de Estado de Servicios Cloud
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo ADVERTENCIA: No se encontró el archivo .env
    echo Copiando env_example.txt a .env...
    copy env_example.txt .env
    echo.
    echo Por favor edita el archivo .env con tu token de bot de Telegram
    echo Luego ejecuta este script nuevamente
    pause
    exit /b 1
)

REM Instalar dependencias si no están instaladas
echo Verificando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando bot...
echo Presiona Ctrl+C para detener
echo.

REM Ejecutar el bot
python main.py

pause 