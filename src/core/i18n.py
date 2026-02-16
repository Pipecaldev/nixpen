from PyQt5.QtCore import QObject, pyqtSignal

class LanguageManager(QObject):
    """Gestor de idiomas para la aplicación (Singleton-ish)"""
    
    languageChanged = pyqtSignal(str) # Emite código de idioma (es, en)
    
    TRANSLATIONS = {
        "es": {
            "toolbar": {
                "title_tools": "🛠️ HERRAMIENTAS",
                "title_bg": "🎨 PIZARRA",
                "title_shapes": "📐 FORMAS",
                "title_thick": "📏 GROSOR",
                "tooltip_pen": "Lápiz (Ctrl+Shift+P)",
                "tooltip_eraser": "Borrador (Ctrl+Shift+E)",
                "tooltip_text": "Texto (Ctrl+Shift+T)",
                "tooltip_spot": "Foco (Ctrl+Shift+S)",
                "tooltip_white": "Pizarra Blanca (Ctrl+Shift+W)",
                "tooltip_black": "Pizarra Negra (Ctrl+Shift+B)",
                "tooltip_line": "Línea",
                "tooltip_arrow": "Flecha",
                "tooltip_rect": "Rectángulo",
                "tooltip_ellipse": "Elipse",
                "screens_title": "🖥️ PANTALLAS",
                "screen_prefix": "Pantalla",
                "activate": "ACTIVAR DIBUJO",
                "deactivate": "DESACTIVAR DIBUJO",
                "screen_selector": "Seleccionar pantalla",
                "thickness_slider": "Grosor del trazo"
            },
            "vertical": {
                "visibility": "Mostrar/Ocultar Trazos",
                "cursor": "Seleccionar / Mover",
                "expand": "Expandir Panel",
                "pen": "Lápiz",
                "eraser": "Borrador",
                "text": "Texto",
                "spotlight": "Foco",
                "line": "Línea",
                "arrow": "Flecha",
                "rect": "Rectángulo",
                "ellipse": "Elipse",
                "undo": "Deshacer",
                "clear": "Eliminar Todo",
                "screenshot": "Captura de Pantalla"
            },
            "header": {
                "help": "Ayuda",
                "collapse": "Colapsar Panel",
                "expand": "Expandir Panel",
                "minimize_window": "Minimizar a Barra de Tareas",
                "close": "Cerrar",
                "lang_select": "Idioma",
                "lang_tooltip": "Cambiar Idioma / Change Language",
                "help_window_title": "NixPen - Ayuda",
                "help_header_title": "📚 NIXPEN - GUÍA DE USO"
            },
            "actions": {
                "undo": "Deshacer (Ctrl+Z)",
                "redo": "Rehacer (Ctrl+Y)",
                "trash": "Limpiar Todo",
                "clear_screen": "🗑️ Limpiar Pantalla",
                "screenshot": "📸 Capturar Pantalla",
                "help_shortcuts": "❓ Ayuda y Atajos",
                "exit_app": "❌ Cerrar Aplicación",
                "help_hint": "💡 Presiona Ctrl+Shift+H para ayuda",
                "camera": "Captura de Pantalla",
                "visibility": "Ocultar/Mostrar Tinta",
                "section_title": "ACCIONES",
                "btn_clear": "  Limpiar Pantalla",
                "btn_screenshot": "  Captura de Pantalla",
                "btn_help": "  Ayuda y Atajos",
                "btn_exit": "  Cerrar Aplicación"
            },
            "colors": {
                "red": "Rojo",
                "blue": "Azul",
                "green": "Verde",
                "yellow": "Amarillo",
                "black": "Negro",
                "white": "Blanco",
                "orange": "Naranja",
                "purple": "Morado",
                "palette_title": "🎨 COLORES"
            }
        },
        "en": {
            "toolbar": {
                "title_tools": "🛠️ TOOLS",
                "title_bg": "🎨 BOARD",
                "title_shapes": "📐 SHAPES",
                "title_thick": "📏 THICKNESS",
                "tooltip_pen": "Pen (Ctrl+Shift+P)",
                "tooltip_eraser": "Eraser (Ctrl+Shift+E)",
                "tooltip_text": "Text (Ctrl+Shift+T)",
                "tooltip_spot": "Spotlight (Ctrl+Shift+S)",
                "tooltip_white": "Whiteboard (Ctrl+Shift+W)",
                "tooltip_black": "Blackboard (Ctrl+Shift+B)",
                "tooltip_line": "Line",
                "tooltip_arrow": "Arrow",
                "tooltip_rect": "Rectangle",
                "tooltip_ellipse": "Ellipse",
                "screens_title": "🖥️ SCREENS",
                "screen_prefix": "Screen",
                "activate": "ACTIVATE DRAWING",
                "deactivate": "DEACTIVATE DRAWING",
                "screen_selector": "Select screen",
                "thickness_slider": "Stroke thickness"
            },
            "vertical": {
                "visibility": "Toggle Visibility",
                "cursor": "Select / Move",
                "expand": "Expand Panel",
                "pen": "Pencil",
                "eraser": "Eraser",
                "text": "Text",
                "spotlight": "Spotlight",
                "line": "Line",
                "arrow": "Arrow",
                "rect": "Rectangle",
                "ellipse": "Ellipse",
                "undo": "Undo",
                "clear": "Delete All",
                "screenshot": "Screenshot"
            },
            "header": {
                "help": "Help",
                "collapse": "Collapse Panel",
                "expand": "Expand Panel",
                "minimize_window": "Minimize to Taskbar",
                "close": "Close",
                "lang_tooltip": "Change Language / Cambiar Idioma",
                "help_window_title": "NixPen - Help",
                "help_header_title": "📚 NIXPEN - USER GUIDE"
            },
            "actions": {
                "undo": "Undo (Ctrl+Z)",
                "redo": "Redo (Ctrl+Y)",
                "trash": "Clear All",
                "clear_screen": "🗑️ Clear Screen",
                "screenshot": "📸 Screenshot",
                "help_shortcuts": "❓ Help & Shortcuts",
                "exit_app": "❌ Quit App",
                "help_hint": "💡 Press Ctrl+Shift+H for help",
                "camera": "Screenshot",
                "visibility": "Hide/Show Ink",
                "section_title": "ACTIONS",
                "btn_clear": "  Clear Screen",
                "btn_screenshot": "  Screenshot",
                "btn_help": "  Help & Shortcuts",
                "btn_exit": "  Quit App"
            },
            "colors": {
                "red": "Red",
                "blue": "Blue",
                "green": "Green",
                "yellow": "Yellow",
                "black": "Black",
                "white": "White",
                "orange": "Orange",
                "purple": "Purple",
                "palette_title": "🎨 COLORS"
            }
        }
    }

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.current_lang = "es"
        return cls._instance

    def set_language(self, lang_code):
        if lang_code in self.TRANSLATIONS and lang_code != self.current_lang:
            self.current_lang = lang_code
            self.languageChanged.emit(lang_code)

    def toggle_language(self):
        new_lang = "en" if self.current_lang == "es" else "es"
        self.set_language(new_lang)
        return new_lang

    def tr(self, section, key):
        """Traduce una clave dadas la sección y la clave"""
        return self.TRANSLATIONS.get(self.current_lang, {}).get(section, {}).get(key, f"MISSING_{key}")

# Instancia global
i18n = LanguageManager()
