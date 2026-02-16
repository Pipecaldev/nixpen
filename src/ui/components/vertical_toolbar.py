from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from src.config import *
from src.core.i18n import i18n
import qtawesome as qta

# --- Colores del tema dark (basados en el HTML de referencia) ---
TOOLBAR_BG = "rgba(30, 30, 30, 242)"       # ~0.95 opacity
TOOLBAR_BORDER = "rgba(255, 255, 255, 25)"  # ~0.1 opacity
TOOL_ACTIVE_BG = "#3b82f6"
TOOL_HOVER_BG = "#2563eb"
VISIBILITY_BG = "#2c3e50"
VISIBILITY_HOVER = "#34495e"
UNDO_BG = "#64748b"
UNDO_HOVER = "#475569"
DELETE_BG = "#c0392b"
DELETE_HOVER = "#a93226"
SCREENSHOT_BG = "#8e44ad"
SCREENSHOT_HOVER = "#7d3c98"
EXPAND_BG = "#f39c12"
EXPAND_HOVER = "#d68910"
DIVIDER_COLOR = "rgba(255, 255, 255, 38)"   # ~0.15 opacity
DOT_COLOR = "rgba(255, 255, 255, 100)"


class VerticalToolbar(QWidget):
    """Barra vertical flotante estilo Pro Dark (basada en diseño HTML de referencia)"""
    
    expand_clicked = pyqtSignal()
    tool_selected = pyqtSignal(str)
    action_triggered = pyqtSignal(str)
    color_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragging = False
        self.drag_position = None
        self.is_minimized = False
        self.initUI()
        self.retranslateUi()
        i18n.languageChanged.connect(self.retranslateUi)
        
    def initUI(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("VerticalToolbar")
        self.setFixedWidth(68)
        
        self.setStyleSheet(f"""
            QWidget#VerticalToolbar {{
                background-color: {TOOLBAR_BG};
                border: 1px solid {TOOLBAR_BORDER};
                border-radius: 34px;
            }}
            QToolTip {{
                background-color: #000000;
                color: white;
                border: none;
                padding: 6px 10px;
                font-size: 13px;
                border-radius: 4px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignHCenter)
        
        # ─── 1. GRIP DE ARRASTRE (6 puntos en grid 3x2) ───
        self.grip = self._create_grip()
        layout.addWidget(self.grip, 0, Qt.AlignHCenter)
        
        # ─── 2. BOTÓN VISIBILIDAD (especial: borde blanco) ───
        self.btn_visibility = self._create_action_button(
            "fa5s.eye", VISIBILITY_BG, VISIBILITY_HOVER, 
            border="2px solid white", rounded="16px", size=48
        )
        self.btn_visibility.clicked.connect(lambda: self.action_triggered.emit('visibility'))
        layout.addWidget(self.btn_visibility, 0, Qt.AlignHCenter)
        
        # ─── 3. BOTÓN CURSOR ───
        self.btn_cursor = self._create_action_button(
            "fa5s.mouse-pointer", VISIBILITY_BG, VISIBILITY_HOVER,
            rounded="12px", size=48
        )
        self.btn_cursor.clicked.connect(lambda: self.tool_selected.emit('cursor'))
        layout.addWidget(self.btn_cursor, 0, Qt.AlignHCenter)
        
        # ─── SEPARADOR ───
        layout.addWidget(self._create_divider())
        
        # ─── 4. HERRAMIENTAS DE DIBUJO ───
        self.btn_pen = self._create_tool_button("fa5s.pen", "pen")
        layout.addWidget(self.btn_pen, 0, Qt.AlignHCenter)
        
        self.btn_line = self._create_tool_button("fa5s.slash", "line")
        layout.addWidget(self.btn_line, 0, Qt.AlignHCenter)
        
        self.btn_arrow = self._create_tool_button("fa5s.location-arrow", "arrow")
        layout.addWidget(self.btn_arrow, 0, Qt.AlignHCenter)
        
        self.btn_rect = self._create_tool_button("fa5s.vector-square", "rect")
        layout.addWidget(self.btn_rect, 0, Qt.AlignHCenter)
        
        self.btn_ellipse = self._create_tool_button("fa5s.circle", "ellipse")
        layout.addWidget(self.btn_ellipse, 0, Qt.AlignHCenter)
        
        self.btn_text = self._create_tool_button("fa5s.font", "text")
        layout.addWidget(self.btn_text, 0, Qt.AlignHCenter)
        
        self.btn_spotlight = self._create_tool_button("fa5s.lightbulb", "spotlight")
        layout.addWidget(self.btn_spotlight, 0, Qt.AlignHCenter)
        
        self.btn_eraser = self._create_tool_button("fa5s.eraser", "eraser")
        layout.addWidget(self.btn_eraser, 0, Qt.AlignHCenter)
        
        # ─── SEPARADOR ───
        layout.addWidget(self._create_divider())
        
        # ─── 5. COLORES (Círculos) ───
        self.btn_color1 = self._create_color_button("#ef4444", 0)   # Red
        layout.addWidget(self.btn_color1, 0, Qt.AlignHCenter)
        
        self.btn_color2 = self._create_color_button("#22c55e", 2)   # Green
        layout.addWidget(self.btn_color2, 0, Qt.AlignHCenter)
        
        # ─── SEPARADOR ───
        layout.addWidget(self._create_divider())
        
        # ─── 6. ACCIONES ───
        self.btn_undo = self._create_action_button(
            "fa5s.undo", UNDO_BG, UNDO_HOVER,
            rounded="12px", size=48, border=f"1px solid rgba(255,255,255,13)"
        )
        self.btn_undo.clicked.connect(lambda: self.action_triggered.emit('undo'))
        layout.addWidget(self.btn_undo, 0, Qt.AlignHCenter)
        
        self.btn_clear = self._create_action_button(
            "fa5s.trash", DELETE_BG, DELETE_HOVER,
            rounded="12px", size=48, border=f"1px solid rgba(255,255,255,13)"
        )
        self.btn_clear.clicked.connect(lambda: self.action_triggered.emit('clear'))
        layout.addWidget(self.btn_clear, 0, Qt.AlignHCenter)
        
        self.btn_screenshot = self._create_action_button(
            "fa5s.camera", SCREENSHOT_BG, SCREENSHOT_HOVER,
            rounded="12px", size=48, border=f"1px solid rgba(255,255,255,13)"
        )
        self.btn_screenshot.clicked.connect(lambda: self.action_triggered.emit('screenshot'))
        layout.addWidget(self.btn_screenshot, 0, Qt.AlignHCenter)
        
        # ─── 7. BOTÓN EXPANDIR (circular, naranja, +) ───
        self.btn_expand = QPushButton()
        self.btn_expand.setIcon(qta.icon("fa5s.plus", color="white"))
        self.btn_expand.setIconSize(QSize(24, 24))
        self.btn_expand.setFixedSize(48, 48)
        self.btn_expand.setCursor(Qt.PointingHandCursor)
        self.btn_expand.clicked.connect(self.expand_clicked.emit)
        self.btn_expand.setStyleSheet(f"""
            QPushButton {{
                background-color: {EXPAND_BG};
                border-radius: 24px;
                border: none;
                margin-top: 8px;
            }}
            QPushButton:hover {{
                background-color: {EXPAND_HOVER};
            }}
        """)
        layout.addWidget(self.btn_expand, 0, Qt.AlignHCenter)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Fábricas de widgets
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _create_grip(self):
        """Crea el asa de arrastre con 6 puntos en grid 3x2"""
        container = QWidget()
        container.setFixedSize(48, 24)
        container.setCursor(Qt.SizeAllCursor)
        grid = QGridLayout(container)
        grid.setContentsMargins(12, 4, 12, 4)
        grid.setSpacing(3)
        for row in range(2):
            for col in range(3):
                dot = QLabel()
                dot.setFixedSize(4, 4)
                dot.setStyleSheet(f"""
                    background-color: {DOT_COLOR};
                    border-radius: 2px;
                """)
                grid.addWidget(dot, row, col)
        return container

    def _create_tool_button(self, icon_name, tool_id):
        """Crea un botón de herramienta estilo blue pill"""
        btn = QPushButton()
        btn.setIcon(qta.icon(icon_name, color="white"))
        btn.setIconSize(QSize(22, 22))
        btn.setFixedSize(48, 48)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.tool_selected.emit(tool_id))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {TOOL_ACTIVE_BG};
                border-radius: 12px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {TOOL_HOVER_BG};
            }}
            QPushButton:checked {{
                background-color: {TOOL_HOVER_BG};
                border: 2px solid white;
            }}
        """)
        return btn

    def _create_action_button(self, icon_name, bg, hover_bg, rounded="12px", size=48, border="none"):
        """Crea un botón de acción con colores personalizados"""
        btn = QPushButton()
        btn.setIcon(qta.icon(icon_name, color="white"))
        btn.setIconSize(QSize(22, 22))
        btn.setFixedSize(size, size)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border-radius: {rounded};
                border: {border};
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
        """)
        return btn

    def _create_color_button(self, color_hex, index):
        """Crea un botón circular de color"""
        btn = QPushButton()
        btn.setFixedSize(32, 32)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self.color_selected.emit(index))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_hex};
                border-radius: 16px;
                border: 2px solid transparent;
            }}
            QPushButton:hover {{ 
                border: 2px solid rgba(255, 255, 255, 128);
            }}
        """)
        return btn

    def _create_divider(self):
        """Crea un separador horizontal estilo divider"""
        line = QFrame()
        line.setFixedSize(32, 1)
        line.setStyleSheet(f"background-color: {DIVIDER_COLOR}; border: none;")
        return line

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Traducciones / Tooltips
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def retranslateUi(self):
        """Actualiza tooltips según idioma actual"""
        self.btn_visibility.setToolTip(i18n.tr("vertical", "visibility"))
        self.btn_cursor.setToolTip(i18n.tr("vertical", "cursor"))
        self.btn_pen.setToolTip(i18n.tr("vertical", "pen"))
        self.btn_eraser.setToolTip(i18n.tr("vertical", "eraser"))
        self.btn_text.setToolTip(i18n.tr("vertical", "text"))
        self.btn_spotlight.setToolTip(i18n.tr("vertical", "spotlight"))
        self.btn_line.setToolTip(i18n.tr("vertical", "line"))
        self.btn_arrow.setToolTip(i18n.tr("vertical", "arrow"))
        self.btn_rect.setToolTip(i18n.tr("vertical", "rect"))
        self.btn_ellipse.setToolTip(i18n.tr("vertical", "ellipse"))
        self.btn_undo.setToolTip(i18n.tr("vertical", "undo"))
        self.btn_clear.setToolTip(i18n.tr("vertical", "clear"))
        self.btn_screenshot.setToolTip(i18n.tr("vertical", "screenshot"))
        self.btn_expand.setToolTip(i18n.tr("vertical", "expand"))
        
        # Colores
        self.btn_color1.setToolTip(i18n.tr("colors", "red"))
        self.btn_color2.setToolTip(i18n.tr("colors", "green"))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Estado
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def set_minimized(self, minimized):
        """Simplifica la barra a solo el botón de visibilidad"""
        self.is_minimized = minimized
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            widget = item.widget()
            if widget:
                if widget == self.btn_visibility:
                    continue
                widget.setVisible(not minimized)
        
        if minimized:
            icon = qta.icon("fa5s.eye-slash", color="white")
            self.btn_visibility.setIcon(icon)
            self.layout().setContentsMargins(5, 5, 5, 5)
            self.setStyleSheet(f"""
                QWidget#VerticalToolbar {{
                    background-color: transparent;
                    border: none;
                }}
                QToolTip {{
                    background-color: #000000;
                    color: white;
                    border: none;
                    padding: 6px 10px;
                    font-size: 13px;
                    border-radius: 4px;
                }}
            """)
            self.setFixedSize(58, 58)
        else:
            icon = qta.icon("fa5s.eye", color="white")
            self.btn_visibility.setIcon(icon)
            self.layout().setContentsMargins(10, 12, 10, 12)
            self.setStyleSheet(f"""
                QWidget#VerticalToolbar {{
                    background-color: {TOOLBAR_BG};
                    border: 1px solid {TOOLBAR_BORDER};
                    border-radius: 34px;
                }}
                QToolTip {{
                    background-color: #000000;
                    color: white;
                    border: none;
                    padding: 6px 10px;
                    font-size: 13px;
                    border-radius: 4px;
                }}
            """)
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)
            self.setFixedWidth(68)
            self.adjustSize()
        self.updateGeometry()

    def set_active_tool(self, tool_name):
        """Sincroniza el estado visual del botón activo"""
        tools = {
            'pen': self.btn_pen, 'eraser': self.btn_eraser, 'cursor': self.btn_cursor,
            'text': self.btn_text, 'spotlight': self.btn_spotlight,
            'line': self.btn_line, 'arrow': self.btn_arrow,
            'rect': self.btn_rect, 'ellipse': self.btn_ellipse
        }
        for name, btn in tools.items():
            btn.setChecked(name == tool_name)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Arrastre
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.window().move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
