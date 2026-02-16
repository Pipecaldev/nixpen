from PyQt5.QtGui import QPainter, QPen, QPainterPath, QBrush
from PyQt5.QtCore import Qt, QRect, QLineF, QPoint, QPointF
from src.core.tools.base_tool import Tool
from abc import abstractmethod
import math

class ShapeTool(Tool):
    """Clase base para herramientas de formas geométricas (con previsualización)"""
    
    def mouse_press(self, event, canvas):
        self.active = True
        self.start_point = event.pos()
        self.end_point = event.pos()
        canvas.update() # Trigger repaint for preview

    def mouse_move(self, event, canvas):
        if self.active:
            self.end_point = event.pos()
            canvas.update() # Update preview

    def mouse_release(self, event, canvas):
        if self.active:
            self.active = False
            self.end_point = event.pos()
            # Commit shape to pixmap
            self._draw_shape(canvas.pixmap)
            canvas.save_state() # Guardar estado para Undo
            canvas.update()

    def draw_preview(self, painter):
        """Dibuja la forma temporalmente en el canvas (sobre el pixmap)"""
        if self.active:
            self._setup_painter(painter)
            self._draw_geometry(painter)

    def _draw_shape(self, pixmap):
        """Dibuja la forma permanentemente en el pixmap"""
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self._setup_painter(painter)
        self._draw_geometry(painter)
        painter.end()

    def _setup_painter(self, painter):
        pen = QPen(self.color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

    @abstractmethod
    def _draw_geometry(self, painter):
        pass

class LineTool(ShapeTool):
    def _draw_geometry(self, painter):
        painter.drawLine(self.start_point, self.end_point)

class RectTool(ShapeTool):
    def _draw_geometry(self, painter):
        rect = QRect(self.start_point, self.end_point).normalized()
        painter.drawRect(rect)

class EllipseTool(ShapeTool):
    def _draw_geometry(self, painter):
        rect = QRect(self.start_point, self.end_point).normalized()
        painter.drawEllipse(rect)

class ArrowTool(ShapeTool):
    def _draw_geometry(self, painter):
        # Usar coordenadas flotantes para precisión
        start = QPointF(self.start_point)
        end = QPointF(self.end_point)
        
        # 1. Dibujar línea principal
        line = QLineF(start, end)
        painter.drawLine(line)
        
        # 2. Calcular puntos de la cabeza
        p1, p2 = self._calculate_arrow_points(start, end)
        
        # 3. Dibujar cabeza rellena
        path = QPainterPath()
        path.moveTo(end)
        path.lineTo(p1)
        path.lineTo(p2)
        path.lineTo(end)
        
        # Usar Brush para rellenar
        painter.fillPath(path, QBrush(self.color))

    def _calculate_arrow_points(self, start, end):
        """Calcula los dos puntos traseros de la cabeza de la flecha"""
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        
        # Tamaño dinámico basado en grosor, pero con mínimo visible
        arrow_size = max(15, self.pen_width * 3.5)
        arrow_angle = math.radians(25) # 25 grados para una flecha más aguda
        
        p1 = end - QPointF(arrow_size * math.cos(angle - arrow_angle),
                           arrow_size * math.sin(angle - arrow_angle))
        p2 = end - QPointF(arrow_size * math.cos(angle + arrow_angle),
                           arrow_size * math.sin(angle + arrow_angle))
        return p1, p2
