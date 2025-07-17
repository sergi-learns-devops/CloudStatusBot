#!/bin/bash

echo "========================================"
echo "   Bot de Estado de Servicios Cloud"
echo "========================================"
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "ADVERTENCIA: No se encontró el archivo .env"
    echo "Copiando env_example.txt a .env..."
    cp env_example.txt .env
    echo
    echo "Por favor edita el archivo .env con tu token de bot de Telegram"
    echo "Luego ejecuta este script nuevamente"
    exit 1
fi

# Instalar dependencias si no están instaladas
echo "Verificando dependencias..."
pip3 install -r requirements.txt

echo
echo "Iniciando bot..."
echo "Presiona Ctrl+C para detener"
echo

# Ejecutar el bot
python3 main.py 