from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QScrollArea, 
                             QWidget, QDialogButtonBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.config import HELP_HTML_ES, HELP_HTML_EN
from src.core.i18n import i18n

class HelpDialog(QDialog):
    """Ventana de ayuda con atajos de teclado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Asegurar que la ayuda se quede siempre visible encima de todo
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.initUI()
        self.retranslateUi()
        # Conectar para actualizar contenido si cambia el idioma mientras está abierta
        i18n.languageChanged.connect(self.retranslateUi)
    
    def initUI(self):
        self.setMinimumSize(700, 600)
        
        layout = QVBoxLayout()
        
        # Título
        self.title_label = QLabel() # Guardamos referencia
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border-radius: 5px;")
        layout.addWidget(self.title_label)
        
        # Área de scroll para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)
        
        # Contenido de ayuda HTML cargado desde config
        self.help_display = QTextEdit()
        self.help_display.setReadOnly(True)
        self.help_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        content_layout.addWidget(self.help_display)
        
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

    def retranslateUi(self):
        self.setWindowTitle(i18n.tr("header", "help_window_title"))
        self.title_label.setText(i18n.tr("header", "help_header_title"))
        
        current = i18n.current_lang
        html_content = HELP_HTML_ES if current == 'es' else HELP_HTML_EN
        self.help_display.setHtml(html_content)
