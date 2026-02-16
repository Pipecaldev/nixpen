#!/bin/bash

echo "=========================================="
echo "  Screen Pen - Desinstalador"
echo "=========================================="
echo ""

# Definir ubicaciones
INSTALL_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/screen-pen"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "🗑️  Eliminando archivos..."

# Eliminar ejecutable
if [ -f "$INSTALL_DIR/screen-pen" ]; then
    rm "$INSTALL_DIR/screen-pen"
    echo "✅ Ejecutable eliminado"
fi

# Eliminar directorio de aplicación
if [ -d "$APP_DIR" ]; then
    rm -rf "$APP_DIR"
    echo "✅ Archivos de aplicación eliminados"
fi

# Eliminar archivo .desktop
if [ -f "$DESKTOP_DIR/screen-pen.desktop" ]; then
    rm "$DESKTOP_DIR/screen-pen.desktop"
    echo "✅ Entrada del menú eliminada"
    
    # Actualizar base de datos de aplicaciones
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null
    fi
fi

echo ""
echo "=========================================="
echo "  ✅ Desinstalación completada"
echo "=========================================="
echo ""
echo "ℹ️  Nota: PyQt5 no ha sido desinstalado ya que"
echo "   otras aplicaciones pueden necesitarlo."
echo ""
echo "   Si deseas desinstalarlo manualmente:"
echo "   sudo apt-get remove python3-pyqt5"
echo ""
