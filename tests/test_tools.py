import math
from PyQt5.QtCore import QPoint, QPointF
from src.core.tools.shape_tools import ArrowTool

def test_arrow_geometry_horizontal():
    """Prueba que la flecha calcula correctamente sus puntos en una línea horizontal"""
    tool = ArrowTool()
    start = QPoint(0, 0)
    end = QPoint(100, 0)
    
    # Calcular cabeza de flecha (espera QPointF)
    p1, p2 = tool._calculate_arrow_points(QPointF(start), QPointF(end))
    
    # Verificaciones básicas de geometría
    # La flecha debe estar "atrás" del punto final
    assert p1.x() < end.x()
    assert p2.x() < end.x()
    
    # Simetría respecto al eje Y (si es horizontal perfecta)
    assert abs(p1.y() + p2.y()) < 0.001

def test_arrow_geometry_vertical():
    """Prueba flecha vertical hacia abajo"""
    tool = ArrowTool()
    start = QPoint(0, 0)
    end = QPoint(0, 100)
    
    p1, p2 = tool._calculate_arrow_points(QPointF(start), QPointF(end))
    
    assert p1.y() < end.y()
    assert p2.y() < end.y()
    # Simetría respecto al eje X
    assert abs(p1.x() + p2.x()) < 0.001
