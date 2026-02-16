#!/bin/bash

echo "=========================================="
echo "  Screen Pen - Instalador para Linux"
echo "=========================================="
echo ""

# Verificar si se ejecuta como usuario normal
if [ "$EUID" -eq 0 ]; then 
    echo "❌ No ejecutes este script como root/sudo"
    echo "   El script pedirá permisos cuando sea necesario"
    exit 1
fi

# Verificar Python3
echo "📋 Verificando dependencias..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "   Instálalo con: sudo apt-get install python3"
    exit 1
fi
echo "✅ Python3 encontrado"

# Verificar/Instalar PyQt5
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo ""
    echo "📦 PyQt5 no está instalado. Instalando..."
    
    # Intentar con apt primero (más rápido y confiable en Ubuntu)
    if command -v apt-get &> /dev/null; then
        echo "   Usando apt-get (requiere permisos de administrador)..."
        sudo apt-get update
        sudo apt-get install -y python3-pyqt5
    else
        echo "   Usando pip3..."
        pip3 install --user PyQt5
    fi
    
    # Verificar instalación
    if ! python3 -c "import PyQt5" 2>/dev/null; then
        echo "❌ No se pudo instalar PyQt5"
        echo "   Intenta manualmente:"
        echo "   sudo apt-get install python3-pyqt5"
        echo "   O: pip3 install PyQt5"
        exit 1
    fi
fi
echo "✅ PyQt5 instalado"

# Crear directorio de instalación
INSTALL_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/screen-pen"

echo ""
echo "📁 Creando directorios de instalación..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$APP_DIR"

# Copiar archivo principal
echo "📝 Instalando archivos..."
cp screen_pen.py "$APP_DIR/screen_pen.py"
chmod +x "$APP_DIR/screen_pen.py"

# Crear ejecutable wrapper
cat > "$INSTALL_DIR/screen-pen" << 'EOF'
#!/bin/bash
exec python3 "$HOME/.local/share/screen-pen/screen_pen.py" "$@"
EOF

chmod +x "$INSTALL_DIR/screen-pen"

# Crear .desktop file para el menú de aplicaciones
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/screen-pen.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Screen Pen
Comment=Herramienta de anotación en pantalla
Exec=$INSTALL_DIR/screen-pen
Icon=draw-brush
Terminal=false
Categories=Graphics;Utility;
Keywords=draw;annotate;pen;screen;
EOF

# Actualizar base de datos de aplicaciones
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null
fi

# Verificar PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️  IMPORTANTE: Añade la siguiente línea a tu ~/.bashrc o ~/.zshrc:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "   Luego ejecuta: source ~/.bashrc"
fi

echo ""
echo "=========================================="
echo "  ✅ Instalación completada con éxito"
echo "=========================================="
echo ""
echo "🚀 Para ejecutar Screen Pen:"
echo "   1. Desde terminal: screen-pen"
echo "   2. Desde el menú de aplicaciones: busca 'Screen Pen'"
echo ""
echo "📝 Atajos de teclado principales:"
echo "   • Ctrl+Shift+D  → Activar/Desactivar dibujo"
echo "   • Ctrl+Shift+C  → Limpiar pantalla"
echo "   • Ctrl+Shift+1-8 → Cambiar colores"
echo "   • ESC → Salir"
echo ""
echo "📚 Ejecuta 'screen-pen' para ver todas las instrucciones"
echo ""
