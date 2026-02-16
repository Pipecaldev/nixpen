from PyQt5.QtWidgets import QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont
import qtawesome as qta
from src.config import *

class UIHelper:
    @staticmethod
    def create_card_section(parent=None):
        """Crea un contenedor estilo 'Tarjeta' con fondo blanco y bordes redondeados"""
        card = QFrame(parent)
        card.setAttribute(Qt.WA_StyledBackground, True)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE_COLOR};
                border: 1px solid {BORDER_COLOR};
                border-radius: {BORDER_RADIUS};
            }}
        """)
        
        # Sombra suave (Opcional, puede ser costoso en rendimiento)
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        
        return card

    @staticmethod
    def create_section_header(text, icon_name=None, font_size=9):
        """Crea un encabezado de sección con icono y texto en mayúsculas"""
        container = QWidget()
        layout = QHBoxLayout(container) # Use HBox for Icon + Text
        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(5)
        
        # Icono (Si existe)
        if icon_name:
            icon_lbl = QLabel()
            icon_pixmap = qta.icon(icon_name, color=PRIMARY_COLOR).pixmap(QSize(14, 14))
            icon_lbl.setPixmap(icon_pixmap)
            icon_lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_lbl)
        
        # Texto
        lbl = QLabel(text.upper())
        font = QFont()
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        font.setPointSize(font_size) 
        lbl.setFont(font)
        
        # Estilo tipo 'text-primary font-semibold text-xs tracking-wider uppercase'
        lbl.setStyleSheet(f"color: {PRIMARY_COLOR};")
        layout.addWidget(lbl)
        
        layout.addStretch() # Push everything to left
            
        return container

    @staticmethod
    def create_icon_button(icon_name, tooltip="", is_checkable=True, size=40, icon_size=20, icon_color=TEXT_PRIMARY, hover_color="#f9fafb", fixed_width=True):
        """Crea un botón cuadrado con icono de FontAwesome/Material Design"""
        btn = QPushButton()
        if fixed_width:
            btn.setFixedSize(size, size)
        else:
            btn.setFixedHeight(size)
            
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(is_checkable)
        btn.setToolTip(tooltip)
        
        # Asignar icono usando qtawesome
        # Color normal: icon_color, Color activo: Azul (PRIMARY_COLOR)
        # Nota: Para acciones destructivas (rojo), tal vez queramos que el active sea rojo también, 
        # pero por ahora mantenemos PRIMARY_COLOR como active estándar o podemos hacerlo configurable.
        icon = qta.icon(icon_name, color=icon_color, color_active=PRIMARY_COLOR)
        btn.setIcon(icon)
        btn.setIconSize(QSize(icon_size, icon_size))
        
        # Estilos base
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {SURFACE_COLOR};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border-color: {PRIMARY_COLOR};
            }}
            QPushButton:checked {{
                background-color: #eff6ff; /* Blue-50 */
                border: 1px solid {PRIMARY_COLOR};
            }}
            QPushButton:pressed {{
                background-color: #dbeafe; /* Blue-100 */
            }}
        """)
        return btn

    @staticmethod
    def create_primary_button(text, icon_name=None):
        """Crea un botón de acción principal (color sólido)"""
        btn = QPushButton(text)
        if icon_name:
            btn.setIcon(qta.icon(icon_name, color="white"))
        
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(36)
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 0 15px;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_HOVER};
            }}
            QPushButton:checked {{
                background-color: #1e40af; /* Blue-800 */
                border: 2px solid #93c5fd; /* Blue-300 ring */
            }}
            QPushButton:pressed {{
                background-color: #1d4ed8; /* Blue-700 */
            }}
        """)
        return btn

    @staticmethod
    def create_danger_button(text, icon_name=None):
        """Crea un botón de peligro (Rojo)"""
        btn = QPushButton(text)
        if icon_name:
            btn.setIcon(qta.icon(icon_name, color="white"))
            
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(36)
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {DANGER_COLOR};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 0 15px;
            }}
            QPushButton:hover {{
                background-color: #dc2626; /* Red-600 */
            }}
            QPushButton:checked {{
                background-color: #991b1b; /* Red-800 */
                border: 2px solid #fca5a5; /* Red-300 ring */
            }}
        """)
        return btn
