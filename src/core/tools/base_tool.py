from abc import ABC, abstractmethod
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint

class Tool(ABC):
    """Clase base abstracta para todas las herramientas de dibujo"""
    
    def __init__(self):
        self.active = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.pen_width = 4
        self.color = QColor(255, 0, 0, 220)

    def set_properties(self, color, width):
        self.color = color
        self.pen_width = width

    @abstractmethod
    def mouse_press(self, event, canvas):
        pass

    @abstractmethod
    def mouse_move(self, event, canvas):
        pass

    @abstractmethod
    def mouse_release(self, event, canvas):
        pass

    def draw_preview(self, painter):
        """Dibuja una previsualización (para formas)"""
        pass
