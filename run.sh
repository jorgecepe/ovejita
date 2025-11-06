#!/bin/bash
# Launcher script for Ovejita Desktop Pet

echo "🐑 Iniciando Ovejita..."

# Check if Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Error: Python 3.12 no está instalado"
    echo "Instálalo con: sudo apt-get install python3.12 python3.12-tk"
    exit 1
fi

# Check if Pillow is installed
if ! python3.12 -c "import PIL" &> /dev/null; then
    echo "⚠️  Pillow no está instalado. Instalando..."
    python3.12 -m pip install --break-system-packages Pillow
fi

# Run the program
python3.12 "$(dirname "$0")/ovejita.py"
