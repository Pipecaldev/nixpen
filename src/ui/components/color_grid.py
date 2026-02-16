from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QButtonGroup
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from src.ui.widgets.color_button import ColorButton
from src.config import COLORS
from src.core.i18n import i18n
from src.ui.utils.styles import UIHelper

class ColorGridComponent(QWidget):
    """Grilla de selección de colores (Estilo Gromit-MPX)"""
    
    color_selected = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color_buttons = [] # Store (btn, name_key)
        self.initUI()
        self.retranslateUi()
        i18n.languageChanged.connect(self.retranslateUi)
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Wrap in Card
        self.card = UIHelper.create_card_section()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Etiqueta
        self.colors_label = UIHelper.create_section_header("PALETTE", icon_name="fa5s.palette")
        card_layout.addWidget(self.colors_label)
        
        # Grid Layout for colors
        grid = QGridLayout()
        grid.setSpacing(10)
        
        self.btn_group = QButtonGroup()
        
        row = 0
        col = 0
        max_cols = 4
        
        for i, (color, name_key) in enumerate(COLORS):
            btn = ColorButton(color, "") # Name set dynamically
            btn.clicked.connect(lambda checked, c=color: self.color_selected.emit(c))
            self.btn_group.addButton(btn)
            
            self.color_buttons.append((btn, name_key))
            
            grid.addWidget(btn, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
        # Seleccionar el primero por defecto
        if self.btn_group.buttons():
            self.btn_group.buttons()[0].setChecked(True)
            
        card_layout.addLayout(grid)
        layout.addWidget(self.card)

    def retranslateUi(self):
        # Update header text
        # create_section_header returns a container widget now. 
        # We need to find the child QLabel to update text.
        for child in self.colors_label.findChildren(QLabel):
            if not child.pixmap(): # Text label doesn't have pixmap
                child.setText(i18n.tr("colors", "palette_title").upper())
                break
        
        
        # Update color tooltips
        for btn, key in self.color_buttons:
            btn.setToolTip(i18n.tr("colors", key))
