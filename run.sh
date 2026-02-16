#!/bin/bash
# Script para lanzar ScreenPen con el entorno virtual correcto

# Obtener el directorio del script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activar entorno virtual y ejecutar
if [ -d "$DIR/.venv" ]; then
    "$DIR/.venv/bin/python3" "$DIR/main.py"
else
    echo "Error: No se encuentra el entorno virtual (.venv)."
    echo "Por favor ejecuta ./install.sh primero."
    exit 1
fi
