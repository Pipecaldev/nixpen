from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint
from .base_tool import Tool

class SpotlightTool(Tool):
    def __init__(self):
        super().__init__()
        self.cursor_pos = QPoint(-100, -100) # Inicialmente fuera de pantalla
        self.spot_radius = 100 # Radio del foco
        self.overlay_color = QColor(0, 0, 0, 200) # Fondo oscuro semitransparente

    def set_properties(self, color, width):
        # Spotlight ignora color y width del usuario, usa sus propios valores
        pass

    def mouse_press(self, event, canvas):
        pass

    def mouse_move(self, event, canvas):
        self.cursor_pos = event.pos()
        canvas.update() # Forzar repintado para mover el foco

    def mouse_release(self, event, canvas):
        pass

    def draw_preview(self, painter):
        """Dibuja el efecto de foco directamente en el canvas (overlay)"""
        # 1. Guardar estado del painter
        painter.save()
        
        # 2. Definir region oscura (Todo menos el círculo)
        # Eliminamos el fillRect previo que causaba que el centro tuviera opacidad.
        pass
        
        # 3. "Recortar" el agujero del foco
        # Usamos CompositionMode_Clear o DestinationOut para hacer el agujero transparente
        # Pero como estamos pintando sobre el widget (que ya tiene fondo transparente u opaco),
        # DestinationOut borraría el widget haciendo "hueco" en la ventana. 
        # Queremos borrar SOLO el overlay oscuro que acabamos de pintar.
        
        # ESTRATEGIA: Pintar el overlay oscuro Y LUEGO pintar el circulo "borrando" el overlay.
        # Esto es complejo en un solo paso sobre el widget.
        # Mejor estrategia: Usar un gradiente radial o dibujar un path (Rectangulo grande - Circulo pequeño).
        
        # Opción Path (Más nítida):
        from PyQt5.QtGui import QPainterPath
        
        path = QPainterPath()
        path.addRect(0, 0, painter.device().width(), painter.device().height())
        
        spot = QPainterPath()
        spot.addEllipse(self.cursor_pos, self.spot_radius, self.spot_radius)
        
        # Restar el círculo al rectángulo completo
        overlay_path = path.subtracted(spot)
        
        # Pintar ese camino complejo (Todo menos el círculo)
        # Nota: Antes pintamos el rect completo, eso estaba mal si queremos usar path.
        # Limpiamos lo que hicimos en el paso 2 (si lo hicimos) o simplemente pintamos el path ahora.
        # Como draw_preview se llama DESPUÉS de pintar el pixmap, lo que pintemos aquí va ENCIMA.
        
        painter.setBrush(self.overlay_color)
        painter.setPen(Qt.NoPen)
        # IMPORTANTE: Aseguramos que el modo de composición sea normal para pintar SEMI-transparencia sobre lo existente
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        
        painter.drawPath(overlay_path)
        
        # Opcional: Dibujar un borde al círculo para resaltarlo
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(self.cursor_pos, self.spot_radius, self.spot_radius)
        
        painter.restore()
