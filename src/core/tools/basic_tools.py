from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from src.core.tools.base_tool import Tool

class PenTool(Tool):
    """Herramienta de dibujo libre (Lápiz)"""
    
    def mouse_press(self, event, canvas):
        self.active = True
        self.start_point = event.pos()
        self._draw_point(canvas.pixmap, self.start_point)
        canvas.update()

    def mouse_move(self, event, canvas):
        if self.active:
            current_point = event.pos()
            self._draw_line(canvas.pixmap, self.start_point, current_point)
            self.start_point = current_point
            canvas.update()

    def mouse_release(self, event, canvas):
        self.active = False

    def _draw_point(self, pixmap, point):
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self._setup_painter(painter)
        painter.drawPoint(point)
        painter.end()

    def _draw_line(self, pixmap, p1, p2):
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self._setup_painter(painter)
        painter.drawLine(p1, p2)
        painter.end()

    def _setup_painter(self, painter):
        pen = QPen(self.color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

class EraserTool(Tool):
    """Herramienta de borrador"""
    
    def __init__(self):
        super().__init__()
        self.pen_width = 25 # Grosor por defecto mayor

    def mouse_press(self, event, canvas):
        self.active = True
        self.start_point = event.pos()
        self._erase_line(canvas.pixmap, self.start_point, self.start_point) # Borrar punto
        canvas.update()

    def mouse_move(self, event, canvas):
        if self.active:
            current_point = event.pos()
            self._erase_line(canvas.pixmap, self.start_point, current_point)
            self.start_point = current_point
            canvas.update()

    def mouse_release(self, event, canvas):
        self.active = False

    def _erase_line(self, pixmap, p1, p2):
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setCompositionMode(QPainter.CompositionMode_Clear) # Modo borrar
        
        pen = QPen(Qt.transparent, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawLine(p1, p2)
        painter.end()
