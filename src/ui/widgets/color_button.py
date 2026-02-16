from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

class ColorButton(QPushButton):
    """Botón de color personalizado para la paleta (Estilo Gromit-MPX)"""
    def __init__(self, color, name, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(45, 45)
        self.setCursor(Qt.PointingHandCursor)
        
        # Color value for stylesheet
        c = color.name()
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {c};
                border: 1px solid #d1d5db; /* Grey border */
                border-radius: 22px; /* Circle */
            }}
            QPushButton:hover {{
                border: 2px solid #bdc3c7; /* Light gray border on hover */
                transform: scale(1.05);
            }}
            QPushButton:checked {{
                border: 3px solid #2c3e50; /* Dark border when selected */
                 /* Could also add an inner white ring trick if needed, but simple is good */
            }}
        """)
        self.setCheckable(True)
        self.setToolTip(name)
