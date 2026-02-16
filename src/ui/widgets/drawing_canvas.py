from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPixmap, QRegion, QColor

from src.core.tools.basic_tools import PenTool, EraserTool
from src.core.tools.shape_tools import LineTool, RectTool, EllipseTool, ArrowTool
from src.core.tools.text_tools import TextTool
from src.core.tools.spotlight_tool import SpotlightTool

class DrawingCanvas(QWidget):
    """Lienzo transparente optimizado con patrón Command y Herramientas"""
    
    def __init__(self, screen_geometry):
        super().__init__()
        self.screen_geometry = screen_geometry
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setGeometry(screen_geometry)
        
        # Estado Gráfico
        self.pixmap = QPixmap(screen_geometry.size())
        self.pixmap.fill(Qt.transparent)
        
        # Sistema de Herramientas
        self.tools = {
            'pen': PenTool(),
            'eraser': EraserTool(),
            'line': LineTool(),
            'rect': RectTool(),
            'ellipse': EllipseTool(),
            'arrow': ArrowTool(),
            'text': TextTool(),
            'spotlight': SpotlightTool()
        }
        self.current_tool = self.tools['pen']
        
        # Sistema Undo/Redo
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 20
        
        # Propiedades activas
        self.active_color = QColor(255, 0, 0, 220)
        self.active_width = 4
        self.background_color = Qt.transparent
        
        self.hide()
        
    def save_state(self):
        """Guarda el estado actual para Undo"""
        if len(self.undo_stack) >= self.max_history:
            self.undo_stack.pop(0)
        self.undo_stack.append(self.pixmap.copy())
        self.redo_stack.clear() # Limpiar redo al hacer nueva acción

    def undo(self):
        """Deshacer última acción"""
        if not self.undo_stack:
            return
            
        # Guardar estado actual en redo antes de deshacer
        self.redo_stack.append(self.pixmap.copy())
        
        # Recuperar estado anterior
        prev_pixmap = self.undo_stack.pop()
        self.pixmap = prev_pixmap
        self.update()

    def redo(self):
        """Rehacer acción deshecha"""
        if not self.redo_stack:
            return
            
        # Guardar estado actual en undo
        self.undo_stack.append(self.pixmap.copy())
        
        # Recuperar estado siguiente
        next_pixmap = self.redo_stack.pop()
        self.pixmap = next_pixmap
        self.update()

    def setTool(self, tool_name):
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]
            self.current_tool.set_properties(self.active_color, self.active_width)

    def setColor(self, color):
        self.active_color = color
        self.current_tool.set_properties(color, self.active_width)
        # Normalmente cambiar color cambia a lápiz, pero si estamos en una forma, quizás queramos mantenerla
        # Por simplicidad y UX común, si era borrador, cambiamos a lápiz. Si era forma, mantenemos forma.
        if isinstance(self.current_tool, EraserTool):
            self.setTool('pen')
    
    def setPenWidth(self, width):
        self.active_width = width
        self.current_tool.set_properties(self.active_color, width)
        # Actualizar también borrador si es necesario, o mantener lógica separada
        self.tools['eraser'].set_properties(Qt.transparent, width * 3) # Borrador más grande

    def clearCanvas(self):
        self.save_state() # Guardar antes de borrar
        self.pixmap.fill(Qt.transparent)
        self.background_color = Qt.transparent # Resetear fondo también al limpiar
        # Limpiar cualquier input de texto activo (QLineEdit del TextTool)
        text_tool = self.tools.get('text')
        if text_tool and text_tool.current_input:
            text_tool.current_input.deleteLater()
            text_tool.current_input = None
            # Restaurar flags originales del canvas
            if hasattr(text_tool, 'original_flags'):
                self.setWindowFlags(text_tool.original_flags)
                self.show()
        self.update()

    def set_background(self, color):
        """Cambia el color de fondo (transparente, blanco, negro)"""
        # Si ya es el mismo color y no es transparente, volver a transparente (toggle)
        if self.background_color == color and color != Qt.transparent:
            self.background_color = Qt.transparent
        else:
            self.background_color = color
        self.update()

    # --- Eventos ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_state() # Guardar estado antes de iniciar trazo (para undo del trazo completo)
            self.current_tool.mouse_press(event, self)
        event.accept()
    
    def mouseMoveEvent(self, event):
        self.current_tool.mouse_move(event, self)
        event.accept()
    
    def mouseReleaseEvent(self, event):
        self.current_tool.mouse_release(event, self)
        event.accept()
    
    def save_screenshot(self, filepath):
        """Captura el contenido actual y lo guarda en la ruta especificada"""
        if not filepath:
            return False
            
        # Creamos una imagen que combine el fondo y los dibujos
        capture = QPixmap(self.size())
        capture.fill(Qt.transparent)
        
        painter = QPainter(capture)
        # Pintamos el fondo actual (pizarra o transparente)
        painter.fillRect(self.rect(), self.background_color)
        # Pintamos los trazos
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        
        return capture.save(filepath)

    def draw_text_content(self, text, pos, font, color):
        """Dibuja texto permanentemente en el canvas y guarda estado para undo"""
        self.save_state()
        
        painter = QPainter(self.pixmap)
        painter.setFont(font)
        painter.setPen(color)
        # Ajuste vertical para que coincida visualmente con el QLineEdit
        # QLineEdit dibuja el texto centrado verticalmente o con baseline, 
        # drawText usa la esquina superior izquierda o baseline.
        # Ajustamos un poco:
        metrics = painter.fontMetrics()
        text_pos = pos + QPoint(4, metrics.ascent() + 2) 
        
        painter.drawText(text_pos, text)
        painter.end()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        # 1. Dibujar Fondo (Pizarra)
        painter.fillRect(self.rect(), self.background_color)
        
        # 2. Dibujar Trazos
        painter.drawPixmap(0, 0, self.pixmap)
        
        # Dibujar preview de la herramienta (si tiene)
        self.current_tool.draw_preview(painter)

    # --- Screenshot ---
    def get_screenshot(self):
        """Retorna una imagen combinada del fondo (si fuera posible capturarlo) y el dibujo"""
        # Nota: En PyQt5 capturar la pantalla debajo de una ventana transparente es complejo cross-platform.
        # Por ahora devolvemos solo el dibujo. Para full screenshot, se necesitaría grabWindow del root.
        return self.pixmap.copy()

    # --- Auxiliares ---
    def setScreenGeometry(self, geometry):
        self.setGeometry(geometry)
        new_pixmap = QPixmap(geometry.size())
        new_pixmap.fill(Qt.transparent)
        painter = QPainter(new_pixmap)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        self.pixmap = new_pixmap
        self.update()

    def updateMask(self, exclude_rects):
        full_region = QRegion(0, 0, self.width(), self.height())
        for rect in exclude_rects:
            local_rect = self.mapFromGlobal(rect.topLeft())
            qrect = QRect(local_rect.x(), local_rect.y(), rect.width(), rect.height())
            full_region -= QRegion(qrect)
        self.setMask(full_region)
