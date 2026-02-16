from PyQt5.QtGui import QColor

# Configuración de Ventana
APP_NAME = "NixPen"
APP_VERSION = "1.0.0"
DEFAULT_WIDTH = 400
COLLAPSED_WIDTH = 250
COLLAPSED_HEIGHT = 50
HEADER_HEIGHT = 40

# Estilos
BACKGROUND_COLOR = "#f3f4f6"  # Gromit-MPX uses light gray
FONT_FAMILY = "Ubuntu, 'Segoe UI', Arial, sans-serif"
BASE_FONT_SIZE = "20px"
TOOLTIP_FONT_SIZE = "18px"

STYLESHEET_GLOBAL = f"""
QWidget {{
    font-family: {FONT_FAMILY};
    font-size: {BASE_FONT_SIZE};
}}
QToolTip {{
    font-size: {TOOLTIP_FONT_SIZE};
    padding: 10px;
    border: 1px solid #7f8c8d;
    background-color: #ecf0f1;
    color: #2c3e50;
}}
"""

STYLESHEET_HEADER = """
QWidget {
    background-color: #2c3e50;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
"""

STYLESHEET_CONTENT = """
QWidget {
    background-color: #ecf0f1;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
"""

# Colores de la aplicación (Palette)
BLUE_COLOR = "#3498db"
HOVER_COLOR = "#2980b9"

# --- NUEVO TEMA (Gromit-MPX Style) ---
# Colors based on Tailwind CSS from valid HTML
PRIMARY_COLOR = "#3b82f6"       # Blue-500
PRIMARY_HOVER = "#2563eb"       # Blue-600
BACKGROUND_COLOR = "#f3f4f6"    # Gray-100 (Light Mode Background)
SURFACE_COLOR = "#ffffff"       # White (Card Surface)
BORDER_COLOR = "#e5e7eb"        # Gray-200
TEXT_PRIMARY = "#1f2937"        # Gray-800
TEXT_SECONDARY = "#6b7280"      # Gray-500
DANGER_COLOR = "#ef4444"        # Red-500
WARNING_COLOR = "#f59e0b"       # Amber-500
SUCCESS_COLOR = "#22c55e"       # Green-500

# Constants
BORDER_RADIUS = "12px"
SHADOW_SOFT = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"

COLORS = [
    (QColor("#ef4444"), 'red'),      # Red-500
    (QColor("#3b82f6"), 'blue'),     # Blue-500
    (QColor("#22c55e"), 'green'),    # Green-500
    (QColor("#facc15"), 'yellow'),   # Yellow-400
    (QColor("#000000"), 'black'),
    (QColor("#ffffff"), 'white'),
    (QColor("#f97316"), 'orange'),   # Orange-500
    (QColor("#9333ea"), 'purple'),   # Purple-600
]

# Estilo común para la ayuda
HELP_CSS = """
<style>
    body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14pt; }
    h2 { color: #2c3e50; background-color: #ecf0f1; padding: 10px; border-radius: 5px; }
    h3 { color: #3498db; margin-top: 15px; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    td { padding: 8px; border-bottom: 1px solid #ddd; font-size: 13pt; }
    .key { background-color: #34495e; color: white; padding: 4px 8px; 
           border-radius: 4px; font-family: monospace; font-weight: bold; font-size: 12pt; }
    .desc { color: #555; padding-left: 15px; }
    .section { margin: 15px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
    .badge { background-color: #e67e22; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10pt; vertical-align: middle; }
</style>
"""

# Texto de Ayuda HTML (ESPAÑOL)
HELP_HTML_ES = HELP_CSS + """
<div class="section">
<h2>⌨️ NixPen — Atajos de Teclado</h2>

<h3>🛠 Herramientas (Ctrl + Shift)</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+P</span></td><td class="desc">Lápiz</td></tr>
    <tr><td><span class="key">Ctrl+Shift+E</span></td><td class="desc">Borrador</td></tr>
    <tr><td><span class="key">Ctrl+Shift+L</span></td><td class="desc">Línea</td></tr>
    <tr><td><span class="key">Ctrl+Shift+A</span></td><td class="desc">Flecha</td></tr>
    <tr><td><span class="key">Ctrl+Shift+R</span></td><td class="desc">Rectángulo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+M</span></td><td class="desc">Elipse</td></tr>
    <tr><td><span class="key">Ctrl+Shift+T</span></td><td class="desc">Texto</td></tr>
    <tr><td><span class="key">Ctrl+Shift+S</span></td><td class="desc">Foco</td></tr>
</table>

<h3>🎮 Control</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+D</span></td><td class="desc">Activar/Desactivar Dibujo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+C</span></td><td class="desc">Limpiar Pantalla</td></tr>
    <tr><td><span class="key">Ctrl+Shift+W</span></td><td class="desc">Pizarra Blanca</td></tr>
    <tr><td><span class="key">Ctrl+Shift+B</span></td><td class="desc">Pizarra Negra</td></tr>
    <tr><td><span class="key">Ctrl+Shift+H</span></td><td class="desc">Mostrar Ayuda</td></tr>
</table>

<h3>↩ Acciones</h3>
<table>
    <tr><td><span class="key">Ctrl+Z</span></td><td class="desc">Deshacer</td></tr>
    <tr><td><span class="key">Ctrl+Y</span></td><td class="desc">Rehacer</td></tr>
</table>

<h3>🎨 Colores</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+1</span></td><td class="desc">Rojo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+2</span></td><td class="desc">Azul</td></tr>
    <tr><td><span class="key">Ctrl+Shift+3</span></td><td class="desc">Verde</td></tr>
    <tr><td><span class="key">Ctrl+Shift+4</span></td><td class="desc">Amarillo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+5</span></td><td class="desc">Negro</td></tr>
    <tr><td><span class="key">Ctrl+Shift+6</span></td><td class="desc">Blanco</td></tr>
    <tr><td><span class="key">Ctrl+Shift+7</span></td><td class="desc">Naranja</td></tr>
    <tr><td><span class="key">Ctrl+Shift+8</span></td><td class="desc">Morado</td></tr>
</table>

<h3>⚡ Otros</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+↑ / ↓</span></td><td class="desc">Tamaño del Pincel</td></tr>
    <tr><td><span class="key">ESC</span></td><td class="desc">Salir</td></tr>
</table>
</div>
"""

# Texto de Ayuda HTML (ENGLISH)
HELP_HTML_EN = HELP_CSS + """
<div class="section">
<h2>⌨️ NixPen — Keyboard Shortcuts</h2>

<h3>🛠 Tools (Ctrl + Shift)</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+P</span></td><td class="desc">Pen</td></tr>
    <tr><td><span class="key">Ctrl+Shift+E</span></td><td class="desc">Eraser</td></tr>
    <tr><td><span class="key">Ctrl+Shift+L</span></td><td class="desc">Line</td></tr>
    <tr><td><span class="key">Ctrl+Shift+A</span></td><td class="desc">Arrow</td></tr>
    <tr><td><span class="key">Ctrl+Shift+R</span></td><td class="desc">Rectangle</td></tr>
    <tr><td><span class="key">Ctrl+Shift+M</span></td><td class="desc">Ellipse</td></tr>
    <tr><td><span class="key">Ctrl+Shift+T</span></td><td class="desc">Text</td></tr>
    <tr><td><span class="key">Ctrl+Shift+S</span></td><td class="desc">Spotlight</td></tr>
</table>

<h3>🎮 Control</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+D</span></td><td class="desc">Toggle Drawing</td></tr>
    <tr><td><span class="key">Ctrl+Shift+C</span></td><td class="desc">Clear Screen</td></tr>
    <tr><td><span class="key">Ctrl+Shift+W</span></td><td class="desc">Whiteboard (White)</td></tr>
    <tr><td><span class="key">Ctrl+Shift+B</span></td><td class="desc">Whiteboard (Black)</td></tr>
    <tr><td><span class="key">Ctrl+Shift+H</span></td><td class="desc">Show Help</td></tr>
</table>

<h3>↩ Actions</h3>
<table>
    <tr><td><span class="key">Ctrl+Z</span></td><td class="desc">Undo</td></tr>
    <tr><td><span class="key">Ctrl+Y</span></td><td class="desc">Redo</td></tr>
</table>

<h3>🎨 Colors</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+1</span></td><td class="desc">Red</td></tr>
    <tr><td><span class="key">Ctrl+Shift+2</span></td><td class="desc">Blue</td></tr>
    <tr><td><span class="key">Ctrl+Shift+3</span></td><td class="desc">Green</td></tr>
    <tr><td><span class="key">Ctrl+Shift+4</span></td><td class="desc">Yellow</td></tr>
    <tr><td><span class="key">Ctrl+Shift+5</span></td><td class="desc">Black</td></tr>
    <tr><td><span class="key">Ctrl+Shift+6</span></td><td class="desc">White</td></tr>
    <tr><td><span class="key">Ctrl+Shift+7</span></td><td class="desc">Orange</td></tr>
    <tr><td><span class="key">Ctrl+Shift+8</span></td><td class="desc">Purple</td></tr>
</table>

<h3>⚡ Other</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+↑ / ↓</span></td><td class="desc">Brush Size</td></tr>
    <tr><td><span class="key">ESC</span></td><td class="desc">Exit</td></tr>
</table>
</div>
"""
# Default just in case (pointing to ES)
HELP_HTML = HELP_HTML_ES
