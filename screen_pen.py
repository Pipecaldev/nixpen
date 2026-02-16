#!/usr/bin/env python3
"""
Screen Pen - Herramienta de anotación en pantalla para Linux
Versión con interfaz gráfica completa, control de grosor, selección de pantallas y ayuda
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, QFrame, QButtonGroup,
                             QSlider, QComboBox, QDialog, QTextEdit, QDialogButtonBox,
                             QScrollArea)
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QFont, QRegion

class HelpDialog(QDialog):
    """Ventana de ayuda con atajos de teclado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Asegurar que la ayuda se quede siempre visible encima de todo
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Screen Pen - Ayuda')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setMinimumSize(700, 600) # Aumentado tamaño de ventana de ayuda
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel('📚 SCREEN PEN - GUÍA DE USO')
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border-radius: 5px;")
        layout.addWidget(title)
        
        # Área de scroll para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)
        
        # Contenido de ayuda
        help_text = """
<style>
    body { font-family: Arial, sans-serif; }
    h2 { color: #2c3e50; background-color: #ecf0f1; padding: 10px; border-radius: 5px; }
    h3 { color: #3498db; margin-top: 15px; }
    table { width: 100%; border-collapse: collapse; margin: 10px 0; }
    td { padding: 8px; border-bottom: 1px solid #ddd; }
    .key { background-color: #34495e; color: white; padding: 3px 8px; 
           border-radius: 3px; font-family: monospace; font-weight: bold; }
    .desc { color: #555; }
    .section { margin: 15px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }
</style>

<div class="section">
<h2>🎨 USO BÁSICO</h2>
<p><b>Screen Pen</b> te permite dibujar sobre tu pantalla con una interfaz gráfica fácil de usar.</p>
<ol>
    <li>Selecciona un <b>color</b> haciendo clic en los botones circulares</li>
    <li>Elige entre <b>Lápiz</b> o <b>Borrador</b></li>
    <li>Ajusta el <b>grosor</b> con el control deslizante</li>
    <li>Dibuja con el mouse sobre la pantalla</li>
    <li>Usa <b>Desactivar Dibujo</b> para ocultar el lienzo temporalmente</li>
</ol>
</div>

<div class="section">
<h2>⌨️ ATAJOS DE TECLADO</h2>

<h3>🎨 Colores (Ctrl+Shift + Número)</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+1</span></td><td class="desc">🔴 Rojo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+2</span></td><td class="desc">🔵 Azul</td></tr>
    <tr><td><span class="key">Ctrl+Shift+3</span></td><td class="desc">🟢 Verde</td></tr>
    <tr><td><span class="key">Ctrl+Shift+4</span></td><td class="desc">🟡 Amarillo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+5</span></td><td class="desc">⚫ Negro</td></tr>
    <tr><td><span class="key">Ctrl+Shift+6</span></td><td class="desc">⚪ Blanco</td></tr>
    <tr><td><span class="key">Ctrl+Shift+7</span></td><td class="desc">🟠 Naranja</td></tr>
    <tr><td><span class="key">Ctrl+Shift+8</span></td><td class="desc">🟣 Morado</td></tr>
</table>

<h3>🛠️ Herramientas (Ctrl+Shift + Letra)</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+P</span></td><td class="desc">✏️ Cambiar a Lápiz</td></tr>
    <tr><td><span class="key">Ctrl+Shift+E</span></td><td class="desc">🧹 Cambiar a Borrador</td></tr>
    <tr><td><span class="key">Ctrl+Shift+D</span></td><td class="desc">🔄 Activar/Desactivar Dibujo</td></tr>
    <tr><td><span class="key">Ctrl+Shift+C</span></td><td class="desc">🗑️ Limpiar Pantalla</td></tr>
    <tr><td><span class="key">Ctrl+Shift+H</span></td><td class="desc">❓ Mostrar esta Ayuda</td></tr>
</table>

<h3>📏 Control de Grosor (Ctrl+Shift + Flechas)</h3>
<table>
    <tr><td><span class="key">Ctrl+Shift+↑</span></td><td class="desc">Aumentar grosor</td></tr>
    <tr><td><span class="key">Ctrl+Shift+↓</span></td><td class="desc">Disminuir grosor</td></tr>
</table>

<h3>⚡ Otros Atajos</h3>
<table>
    <tr><td><span class="key">ESC</span></td><td class="desc">Cerrar la aplicación</td></tr>
</table>
</div>

<div class="section">
<h2>🖥️ MULTI-MONITOR</h2>
<p>Si tienes múltiples pantallas, puedes seleccionar en cuál dibujar usando el menú desplegable 
<b>"Pantalla"</b> en el panel de control. El lienzo cambiará automáticamente a la pantalla seleccionada.</p>
</div>

<div class="section">
<h2>📏 CONTROL DE GROSOR</h2>
<p>Usa el control deslizante en el panel para ajustar el grosor del lápiz o borrador en tiempo real.</p>
<ul>
    <li><b>Lápiz:</b> 1-20 pixels</li>
    <li><b>Borrador:</b> 10-50 pixels</li>
</ul>
</div>

<div class="section">
<h2>💡 CONSEJOS</h2>
<ul>
    <li>🎯 El panel de control se puede mover arrastrándolo a cualquier parte</li>
    <li>🔄 Desactiva el dibujo temporalmente para usar tu PC normalmente</li>
    <li>🎨 Al seleccionar un color, automáticamente cambia a lápiz</li>
    <li>⚡ Los atajos de teclado son más rápidos para cambios frecuentes</li>
    <li>🖱️ El lienzo captura eventos del mouse solo cuando está activado</li>
</ul>
</div>

<div class="section">
<h2>🔧 SOLUCIÓN DE PROBLEMAS</h2>
<ul>
    <li><b>No dibuja:</b> Verifica que el dibujo esté activado (verde)</li>
    <li><b>No veo el panel:</b> Busca en la esquina superior derecha</li>
    <li><b>El dock desaparece:</b> Desactiva el dibujo con el botón rojo</li>
    <li><b>Pantalla bloqueada:</b> Presiona ESC para cerrar</li>
</ul>
</div>
"""
        
        help_display = QTextEdit()
        help_display.setHtml(help_text)
        help_display.setReadOnly(True)
        help_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        content_layout.addWidget(help_display)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Botón cerrar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 30px;
                font-size: 13px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(button_box)
        
        self.setLayout(layout)


class DrawingCanvas(QWidget):
    """Lienzo transparente para dibujar"""
    def __init__(self, screen_geometry):
        super().__init__()
        self.screen_geometry = screen_geometry
        # IMPORTANTE: No usar WindowTransparentForInput para poder capturar eventos
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowDoesNotAcceptFocus  # No robar el foco
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        # Configurar geometría
        self.setGeometry(screen_geometry)
        
        # Inicializar pixmap
        self.pixmap = QPixmap(screen_geometry.size())
        self.pixmap.fill(Qt.transparent)
        
        self.drawing = False
        self.last_point = QPoint()
        
        # Configuración de herramientas
        self.current_tool = 'pen'
        self.pen_width = 4
        self.eraser_width = 25
        self.current_color = QColor(255, 0, 0, 220)  # Rojo por defecto
        
        # Ocultar al inicio si no se quiere dibujar inmediatamente
        # self.showFullScreen() <-- Se maneja desde el panel ahora
        self.hide()
        
    def setScreenGeometry(self, geometry):
        """Cambia la geometría del canvas a otra pantalla"""
        self.screen_geometry = geometry
        self.setGeometry(geometry)
        
        # Crear nuevo pixmap del tamaño correcto
        new_pixmap = QPixmap(geometry.size())
        new_pixmap.fill(Qt.transparent)
        
        # Copiar contenido antiguo si cabe
        painter = QPainter(new_pixmap)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
        
        self.pixmap = new_pixmap
        self.update()
        
    def mousePressEvent(self, event):
        """Captura el inicio del dibujo"""
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            # Dibujar un punto inicial
            painter = QPainter(self.pixmap)
            painter.setRenderHint(QPainter.Antialiasing, True)
            
            if self.current_tool == 'pen':
                pen = QPen(
                    self.current_color,
                    self.pen_width,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin
                )
                painter.setPen(pen)
                painter.drawPoint(event.pos())
            
            painter.end()
            self.update()
        event.accept()
    
    def mouseMoveEvent(self, event):
        """Captura el movimiento mientras se dibuja"""
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.pixmap)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            
            if self.current_tool == 'pen':
                pen = QPen(
                    self.current_color,
                    self.pen_width,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin
                )
                painter.setPen(pen)
                painter.drawLine(self.last_point, event.pos())
            
            elif self.current_tool == 'eraser':
                # El borrador usa composición para borrar
                painter.setCompositionMode(QPainter.CompositionMode_Clear)
                pen = QPen(
                    Qt.transparent,
                    self.eraser_width,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin
                )
                painter.setPen(pen)
                painter.drawLine(self.last_point, event.pos())
            
            painter.end()
            self.last_point = event.pos()
            self.update()
        event.accept()
    
    def mouseReleaseEvent(self, event):
        """Finaliza el dibujo"""
        if event.button() == Qt.LeftButton:
            self.drawing = False
        event.accept()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPixmap(0, 0, self.pixmap)
    
    def clearCanvas(self):
        """Limpia todo el lienzo"""
        self.pixmap.fill(Qt.transparent)
        self.update()
    
    def setColor(self, color):
        """Cambia el color del lápiz"""
        self.current_color = color
        self.current_tool = 'pen'
    
    def setTool(self, tool):
        """Cambia la herramienta activa"""
        self.current_tool = tool

    def setPenWidth(self, width):
        """Cambia el grosor del lápiz"""
        self.pen_width = width
    
    def setEraserWidth(self, width):
        """Cambia el grosor del borrador"""
        self.eraser_width = width

    def updateMask(self, exclude_rects):
        """
        Define una máscara para el lienzo que excluye ciertas áreas (como el panel).
        Los clics en estas áreas pasarán a través del lienzo.
        """
        full_region = QRegion(0, 0, self.width(), self.height())
        
        for rect in exclude_rects:
            # Convertir coordenadas globales a locales del canvas
            local_rect = self.mapFromGlobal(rect.topLeft())
            qrect = QRect(local_rect.x(), local_rect.y(), rect.width(), rect.height())
            full_region -= QRegion(qrect)
            
        self.setMask(full_region)


class ColorButton(QPushButton):
    """Botón de color personalizado"""
    def __init__(self, color, name, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(50, 50)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color.name()};
                border: 3px solid #555;
                border-radius: 25px;
            }}
            QPushButton:hover {{
                border: 3px solid #fff;
            }}
            QPushButton:checked {{
                border: 4px solid #00ff00;
            }}
        """)
        self.setCheckable(True)
        self.setToolTip(name)


class ControlPanel(QMainWindow):
    """Panel de control con interfaz gráfica"""
    def __init__(self):
        super().__init__()
        
        # Detectar pantallas disponibles
        self.screens = QApplication.screens()
        self.current_screen_index = 0
        
        # Crear canvas en la pantalla principal
        self.canvas = DrawingCanvas(self.screens[0].geometry())
        self.drawing_enabled = False # Desactivado por defecto
        
        # Diccionario de colores
        self.color_list = [
            (QColor(255, 0, 0, 220), 'Rojo'),
            (QColor(0, 100, 255, 220), 'Azul'),
            (QColor(0, 200, 0, 220), 'Verde'),
            (QColor(255, 255, 0, 220), 'Amarillo'),
            (QColor(0, 0, 0, 220), 'Negro'),
            (QColor(255, 255, 255, 220), 'Blanco'),
            (QColor(255, 140, 0, 220), 'Naranja'),
            (QColor(160, 32, 240, 220), 'Morado'),
        ]
        
        self.initUI()
        
    def initUI(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        central_widget.setLayout(self.main_layout)
        
        # Aumentar ancho base y configurar geometría inicial
        self.expanded_width = 400 # Aumentado de 350 a 400
        self.setFixedWidth(self.expanded_width)
        
        # Estilos generales aumentados
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px; /* Aumentado de 16px */
            }
            QToolTip {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #7f8c8d;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)
        
        # --- CABECERA (Siempre visible) ---
        header_widget = QWidget()
        header_widget.setFixedHeight(40)
        header_widget.setStyleSheet("background-color: #2c3e50; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(15, 0, 15, 0)

        # Título
        title_label = QLabel("🎨 ScreenPen")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px; background: transparent;")
        
        # Botón Colapsar/Expandir
        self.btn_collapse = QPushButton("−")
        self.btn_collapse.setFixedSize(24, 24)
        self.btn_collapse.setToolTip("Minimizar/Expandir Panel")
        self.btn_collapse.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #4e6a85; }
        """)
        self.btn_collapse.clicked.connect(self.toggleView)

        # Botón Cerrar
        self.btn_close_header = QPushButton("×")
        self.btn_close_header.setFixedSize(24, 24)
        self.btn_close_header.setToolTip("Cerrar Aplicación")
        self.btn_close_header.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #e74c3c; }
        """)
        self.btn_close_header.clicked.connect(self.closeApp)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_collapse)
        header_layout.addSpacing(5)
        header_layout.addWidget(self.btn_close_header)
        
        self.main_layout.addWidget(header_widget)

        # --- CONTENIDO (Ocultable) ---
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        """)
        
        # Layout del contenido
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Mover el resto de widgets a 'layout' en lugar de 'main_layout'
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Selector de pantalla (si hay más de una)
        if len(self.screens) > 1:
            screen_label = QLabel('🖥️ PANTALLA')
            screen_label.setStyleSheet("font-weight: bold; font-size: 13px;")
            layout.addWidget(screen_label)
            
            self.screen_combo = QComboBox()
            for i, screen in enumerate(self.screens):
                geometry = screen.geometry()
                self.screen_combo.addItem(f"Pantalla {i+1} ({geometry.width()}x{geometry.height()})")
            self.screen_combo.currentIndexChanged.connect(self.changeScreen)
            self.screen_combo.setStyleSheet("""
                QComboBox {
                    padding: 8px;
                    font-size: 12px;
                    border: 2px solid #3498db;
                    border-radius: 4px;
                    background-color: white;
                }
            """)
            layout.addWidget(self.screen_combo)
        
        # Estado inicial (Desactivado)
        self.status_label = QLabel('⏸️ DIBUJO DESACTIVADO')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #95a5a6;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Botón toggle dibujo
        self.toggle_btn = QPushButton('✅ Activar Dibujo')
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 18px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggleDrawing)
        layout.addWidget(self.toggle_btn)
        
        # Herramientas
        tools_label = QLabel('🛠️ HERRAMIENTAS')
        tools_label.setStyleSheet("font-weight: bold; font-size: 15px;")
        layout.addWidget(tools_label)
        
        tools_layout = QHBoxLayout()
        
        self.pen_btn = QPushButton('✏️ Lápiz')
        self.pen_btn.setCheckable(True)
        self.pen_btn.setChecked(True)
        self.pen_btn.setCursor(Qt.PointingHandCursor)
        self.pen_btn.clicked.connect(lambda: self.setTool('pen'))
        
        self.eraser_btn = QPushButton('🧹 Borrador')
        self.eraser_btn.setCheckable(True)
        self.eraser_btn.setCursor(Qt.PointingHandCursor)
        self.eraser_btn.clicked.connect(lambda: self.setTool('eraser'))
        
        # Grupo de botones para herramientas
        self.tool_group = QButtonGroup()
        self.tool_group.addButton(self.pen_btn)
        self.tool_group.addButton(self.eraser_btn)
        
        for btn in [self.pen_btn, self.eraser_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 14px;
                    font-size: 15px;
                    border: 2px solid #3498db;
                    border-radius: 6px;
                    background-color: white;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                }
            """)
        
        tools_layout.addWidget(self.pen_btn)
        tools_layout.addWidget(self.eraser_btn)
        layout.addLayout(tools_layout)
        
        # Control de grosor
        thickness_label = QLabel('📏 GROSOR')
        thickness_label.setStyleSheet("font-weight: bold; font-size: 13px; margin-top: 5px;")
        layout.addWidget(thickness_label)
        
        thickness_layout = QHBoxLayout()
        
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setMinimum(1)
        self.thickness_slider.setMaximum(20)
        self.thickness_slider.setValue(4)
        self.thickness_slider.setTickPosition(QSlider.TicksBelow)
        self.thickness_slider.setTickInterval(5)
        self.thickness_slider.setCursor(Qt.PointingHandCursor)
        self.thickness_slider.valueChanged.connect(self.changeThickness)
        self.thickness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 2px solid #2980b9;
                width: 24px;
                height: 24px;
                margin: -5px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }
        """)
        
        self.thickness_label = QLabel('4 px')
        self.thickness_label.setMinimumWidth(60)
        self.thickness_label.setAlignment(Qt.AlignCenter)
        self.thickness_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        thickness_layout.addWidget(self.thickness_slider)
        thickness_layout.addWidget(self.thickness_label)
        layout.addLayout(thickness_layout)
        
        # Colores
        colors_label = QLabel('🎨 COLORES')
        colors_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        layout.addWidget(colors_label)
        
        # Grid de colores
        colors_layout1 = QHBoxLayout()
        colors_layout2 = QHBoxLayout()
        
        self.color_buttons = []
        self.color_group = QButtonGroup()
        
        for i, (color, name) in enumerate(self.color_list):
            btn = ColorButton(color, name)
            btn.clicked.connect(lambda checked, c=color: self.setColor(c))
            self.color_group.addButton(btn)
            self.color_buttons.append(btn)
            
            if i < 4:
                colors_layout1.addWidget(btn)
            else:
                colors_layout2.addWidget(btn)
        
        # Marcar rojo como seleccionado
        self.color_buttons[0].setChecked(True)
        
        layout.addLayout(colors_layout1)
        layout.addLayout(colors_layout2)
        
        # Separador
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line2)
        
        # Botón limpiar
        clear_btn = QPushButton('🗑️ Limpiar Pantalla')
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        clear_btn.clicked.connect(self.clearScreen)
        layout.addWidget(clear_btn)
        
        # Botón ayuda
        help_btn = QPushButton('❓ Ayuda y Atajos')
        help_btn.setCursor(Qt.PointingHandCursor)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        help_btn.clicked.connect(self.showHelp)
        layout.addWidget(help_btn)
        
        # Botón salir
        exit_btn = QPushButton('❌ Cerrar Aplicación')
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        exit_btn.clicked.connect(self.closeApp)
        layout.addWidget(exit_btn)
        
        # Instrucciones
        info_label = QLabel('💡 Presiona Ctrl+Shift+H para ayuda')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 13px;
                padding: 12px;
            }
        """)
        layout.addWidget(info_label)
        
        # Estilo final
        self.main_layout.addWidget(self.content_widget)
        
        # Configuracion de ventana
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Panel colapsado más grande
        self.collapsed_width = 250
        self.collapsed_height = 60
        
        # Estado inicial
        self.is_collapsed = False
        # self.expanded_width ya definido arriba
        
        # Posicionamiento inicial inteligente
        screens = QApplication.screens()
        if len(screens) > 1:
            geo = screens[1].geometry()
            self.move(geo.x() + geo.width() - self.expanded_width - 20, geo.y() + 50)
        else:
            geo = screens[0].geometry()
            self.move(geo.x() + geo.width() - self.expanded_width - 20, geo.y() + 50)
        
        self.show()
    
    def keyPressEvent(self, event):
        """Maneja los atajos de teclado globales"""
        key = event.key()
        modifiers = event.modifiers()
        
        # Ctrl+Shift+D: Toggle dibujo
        if key == Qt.Key_D and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.toggleDrawing()
        
        # Ctrl+Shift+C: Limpiar pantalla
        elif key == Qt.Key_C and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.clearScreen()
        
        # Ctrl+Shift+E: Borrador
        elif key == Qt.Key_E and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.eraser_btn.setChecked(True)
            self.setTool('eraser')
        
        # Ctrl+Shift+P: Lápiz
        elif key == Qt.Key_P and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.pen_btn.setChecked(True)
            self.setTool('pen')
        
        # Ctrl+Shift+H: Ayuda
        elif key == Qt.Key_H and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.showHelp()
        
        # Ctrl+Shift+Arriba: Aumentar grosor
        elif key == Qt.Key_Up and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            current = self.thickness_slider.value()
            self.thickness_slider.setValue(min(current + 1, 20))
        
        # Ctrl+Shift+Abajo: Disminuir grosor
        elif key == Qt.Key_Down and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            current = self.thickness_slider.value()
            self.thickness_slider.setValue(max(current - 1, 1))
        
        # Atajos de colores (Ctrl+Shift+número)
        elif modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            color_keys = {
                Qt.Key_1: 0, Qt.Key_2: 1, Qt.Key_3: 2, Qt.Key_4: 3,
                Qt.Key_5: 4, Qt.Key_6: 5, Qt.Key_7: 6, Qt.Key_8: 7,
            }
            
            if key in color_keys:
                index = color_keys[key]
                self.color_buttons[index].setChecked(True)
                self.setColor(self.color_list[index][0])
        
        # ESC: Salir
        elif key == Qt.Key_Escape:
            self.closeApp()
    
    def changeScreen(self, index):
        """Cambia el canvas a la pantalla seleccionada"""
        self.current_screen_index = index
        screen_geometry = self.screens[index].geometry()
        self.canvas.setScreenGeometry(screen_geometry)
        
        # Lógica de posicionamiento inverso:
        # El panel debe ir a una pantalla DIFERENTE a la que se está dibujando
        target_panel_screen = 0
        
        if len(self.screens) > 1:
            # Si seleccionamos la pantalla 0, movemos panel a la 1
            # Si seleccionamos la pantalla 1 (o mayor), movemos panel a la 0
            if index == 0:
                target_panel_screen = 1
            else:
                target_panel_screen = 0
        else:
            # Si solo hay 1 pantalla, se queda en la 0
            target_panel_screen = 0
            
        panel_geo = self.screens[target_panel_screen].geometry()
        
        # Mover el panel a la esquina superior derecha de la pantalla OJETIVO del panel
        self.move(panel_geo.x() + panel_geo.width() - self.width() - 20, 
                  panel_geo.y() + 50)
        
        # Asegurar que el canvas esté visible
        if self.drawing_enabled:
            self.canvas.show()
            self.canvas.raise_()
            self.raise_()
    
    def changeThickness(self, value):
        """Cambia el grosor de la herramienta actual"""
        self.thickness_label.setText(f'{value} px')
        
        if self.canvas.current_tool == 'pen':
            self.canvas.setPenWidth(value)
        else:
            # Para el borrador, usar un rango diferente (más grande)
            eraser_value = int(value * 2.5)  # Convierte 1-20 a 2.5-50
            self.canvas.setEraserWidth(eraser_value)
    
    def setTool(self, tool):
        """Cambia la herramienta activa"""
        self.canvas.setTool(tool)
        
        # Ajustar el rango del slider según la herramienta
        if tool == 'pen':
            self.thickness_slider.setMaximum(20)
            current_pen_width = self.canvas.pen_width
            self.thickness_slider.setValue(current_pen_width)
        else:  # eraser
            self.thickness_slider.setMaximum(20)
            # Calcular valor inverso del eraser
            current_eraser_value = int(self.canvas.eraser_width / 2.5)
            self.thickness_slider.setValue(current_eraser_value)
        
        # Asegurar que el canvas esté al frente
        if self.drawing_enabled:
            self.canvas.raise_()
            self.raise_()
    
    def toggleDrawing(self):
        """Activa/desactiva el modo dibujo"""
        self.drawing_enabled = not self.drawing_enabled
        
        if self.drawing_enabled:
            self.canvas.show()
            self.canvas.raise_()
            # self.canvas.activateWindow()  <-- ELIMINADO: Esto robaba el foco
            
            # Asegurar que el panel quede encima
            self.raise_()
            self.activateWindow()
            
            # Actualizar máscara inicial
            self.updateCanvasMask()
            
            self.status_label.setText('✅ DIBUJO ACTIVADO')
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #2ecc71;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            self.toggle_btn.setText('🚫 Desactivar Dibujo')
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
        else:
            self.canvas.hide()
            self.status_label.setText('⏸️ DIBUJO DESACTIVADO')
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #95a5a6;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            self.toggle_btn.setText('✅ Activar Dibujo')
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
            """)
    
    def setColor(self, color):
        """Cambia el color del lápiz"""
        self.canvas.setColor(color)
        # Cambiar a lápiz automáticamente
        self.pen_btn.setChecked(True)
        self.canvas.setTool('pen')
        # Asegurar que el canvas esté al frente
        if self.drawing_enabled:
            self.canvas.raise_()
            self.raise_()
    
    def clearScreen(self):
        """Limpia toda la pantalla"""
        self.canvas.clearCanvas()
    
    def showHelp(self):
        """Muestra la ventana de ayuda"""
        # Usar variable de instancia para mantener referencia
        self.help_window = HelpDialog(self)
        self.help_window.show()
        self.help_window.raise_()
        self.help_window.activateWindow()
    
    def closeApp(self):
        """Cierra la aplicación"""
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.close()
        self.close()
        QApplication.quit()

    def toggleView(self):
        """Alterna entre vista expandida y colapsada (mini)"""
        if self.is_collapsed:
            # EXPANDIR
            self.content_widget.setVisible(True)
            self.setFixedWidth(self.expanded_width)
            self.btn_collapse.setText("−")
            self.is_collapsed = False
        else:
            # COLAPSAR
            self.content_widget.setVisible(False)
            self.setFixedWidth(250) # Aumentado a 250
            self.resize(250, 60)    # Aumentado altura a 60
            self.btn_collapse.setText("□") 
            self.is_collapsed = True
        
        # Actualizar máscara inmediatamente después de cambiar tamaño
        self.updateCanvasMask()

    def updateCanvasMask(self):
        """Informa al canvas sobre la posición actual del panel para que no bloquee los clics"""
        if hasattr(self, 'canvas') and self.canvas:
            rects = [self.geometry()]
            
            # También excluir la ventana de ayuda si existe y es visible
            if hasattr(self, 'help_window') and self.help_window and self.help_window.isVisible():
                rects.append(self.help_window.geometry())
                
            self.canvas.updateMask(rects)


    def mousePressEvent(self, event):
        """Permite mover la ventana al hacer clic y arrastrar"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Mueve la ventana si se está arrastrando"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            # updateCanvasMask ya se llama en moveEvent, que se dispara al mover

    def moveEvent(self, event):
        """Se activa al mover el panel"""
        super().moveEvent(event)
        self.updateCanvasMask()

    def resizeEvent(self, event):
        """Se activa al redimensionar el panel"""
        super().resizeEvent(event)
        self.updateCanvasMask()


def main():
    # Verificar dependencias
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        print("\n❌ ERROR: PyQt5 no está instalado")
        print("\n📦 Para instalar las dependencias, ejecuta:")
        print("   sudo apt-get update")
        print("   sudo apt-get install python3-pyqt5")
        print("\n   O con pip:")
        print("   pip3 install PyQt5")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("  SCREEN PEN - Herramienta de Anotación con GUI")
    print("="*60)
    print("\n✨ Panel de control abierto en la esquina superior derecha")
    print("🖥️  Soporte multi-monitor detectado")
    print("📏 Control de grosor incluido")
    print("❓ Presiona Ctrl+Shift+H para ver la ayuda")
    print("🎨 ¡Disfruta dibujando sobre tu pantalla!")
    print("="*60 + "\n")
    
    app = QApplication(sys.argv)
    window = ControlPanel()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
