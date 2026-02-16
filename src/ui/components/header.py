from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from src.config import *
import qtawesome as qta
from src.core.i18n import i18n

class HeaderComponent(QWidget):
    """Encabezado estilo Gromit-MPX (Solo Botón Verde + Título Centrado + Banderas)"""

    minimize_clicked = pyqtSignal()
    collapse_clicked = pyqtSignal()
    help_clicked = pyqtSignal()
    close_clicked = pyqtSignal() # Kept for compatibility if needed, but not triggered by button
    mouse_pressed = pyqtSignal(object)
    language_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragging = False
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.initUI()
        self.retranslateUi()
        i18n.languageChanged.connect(self.retranslateUi)

    def initUI(self):
        # Estilo del Header
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE_COLOR};
                border-top-left-radius: {BORDER_RADIUS};
                border-top-right-radius: {BORDER_RADIUS};
                border-bottom: 2px solid {BORDER_COLOR}; /* Un poco más grueso */
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)

        # 1. Left: Collapse Button (Green)
        self.btn_collapse = self._create_traffic_light("#22c55e", "#16a34a")
        self.btn_collapse.clicked.connect(self.collapse_clicked.emit)
        layout.addWidget(self.btn_collapse)

        # Spacer Left
        layout.addStretch(1)

        # 2. Center: Title (Black, Larger, Centered)
        self.title_label = QLabel(APP_NAME.upper())
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"""
            color: #000000;
            font-weight: bold;
            font-size: 18px; /* Larger */
            letter-spacing: 2px;
            border: none;
            background: transparent;
            font-family: {FONT_FAMILY};
        """)
        layout.addWidget(self.title_label)

        # Spacer Right
        layout.addStretch(1)

        # 3. Right Icons (Language, Help)
        
        # Language (Text + Flag)
        self.btn_lang = QPushButton() 
        self.btn_lang.setCursor(Qt.PointingHandCursor)
        self.btn_lang.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {BORDER_COLOR};
                border-radius: 6px;
                padding: 4px 8px;
                font-weight: bold;
                color: {TEXT_PRIMARY};
                font-size: 14px;
                font-family: "Ubuntu", "Noto Color Emoji", "Segoe UI Emoji", "Apple Color Emoji", sans-serif;
            }}
            QPushButton:hover {{
                background-color: {BACKGROUND_COLOR};
                border-color: {PRIMARY_COLOR};
            }}
        """)
        self.btn_lang.clicked.connect(self._toggle_language)
        layout.addWidget(self.btn_lang)

        # Help
        self.btn_help = self._create_icon_button("fa5s.question-circle")
        self.btn_help.clicked.connect(self.help_clicked.emit)
        layout.addWidget(self.btn_help)

    def _create_traffic_light(self, color, hover_color):
        btn = QPushButton("−")
        btn.setFixedSize(28, 28)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 14px;
                border: none;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
                line-height: 28px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        return btn

    def _create_icon_button(self, icon_name):
        btn = QPushButton()
        btn.setIcon(qta.icon(icon_name, color=TEXT_SECONDARY, color_active=PRIMARY_COLOR))
        btn.setIconSize(self.btn_collapse.size() * 1.5) # Scale icon relative to buttons
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0,0,0,0.05);
                border-radius: 4px;
            }
        """)
        return btn

    def _toggle_language(self):
        i18n.toggle_language()

    def retranslateUi(self):
        self.btn_collapse.setToolTip(i18n.tr("header", "collapse"))
        self.btn_help.setToolTip(i18n.tr("header", "help"))
        self.btn_lang.setToolTip(i18n.tr("header", "lang_tooltip"))
        
        # Update Language Button Text
        if i18n.current_lang == "es":
            self.btn_lang.setText("ES 🇪🇸")
        else:
            self.btn_lang.setText("US 🇺🇸")

    # Eventos de ratón para arrastrar
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            # Find the top-level widget to move
            self.window_to_move = self.window() 
            self.drag_position = event.globalPos() - self.window_to_move.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.window_to_move.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

