from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint

def get_screen_geometry():
    """Obtiene la geometría de la pantalla principal"""
    return QApplication.primaryScreen().geometry()

def get_secondary_screen_geometry():
    """Obtiene la geometría del monitor secundario si existe, sino None"""
    screens = QApplication.screens()
    if len(screens) > 1:
        return screens[1].geometry()
    return None

def get_initial_position(width, height):
    """
    Calcula la posición inicial (x, y) para centrar la ventana
    en el monitor secundario (si existe) o en el principal.
    """
    secondary_geo = get_secondary_screen_geometry()
    
    if secondary_geo:
        # Centrar en monitor secundario
        screen_x = secondary_geo.x()
        screen_y = secondary_geo.y()
        screen_w = secondary_geo.width()
        screen_h = secondary_geo.height()
    else:
        # Centrar en monitor principal
        primary_geo = get_screen_geometry()
        screen_x = primary_geo.x()
        screen_y = primary_geo.y()
        screen_w = primary_geo.width()
        screen_h = primary_geo.height()
        
    x = screen_x + (screen_w - width) // 2
    y = screen_y + (screen_h - height) // 2
    
    return x, y
