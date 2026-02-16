from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from src.core.i18n import i18n
from src.ui.utils.styles import UIHelper, DANGER_COLOR
import qtawesome as qta

class ActionsComponent(QWidget):
    """Botones de acción (limpiar, ayuda, salir) - Estilo Gromit-MPX"""
    
    clear_clicked = pyqtSignal()
    help_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()
    screenshot_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.retranslateUi()
        i18n.languageChanged.connect(self.retranslateUi)
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Card Wrapper
        self.card = UIHelper.create_card_section()
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        self.header_label = UIHelper.create_section_header("ACTIONS")
        card_layout.addWidget(self.header_label)
        
        # Actions Grid -> VBox for single column
        actions_layout = QVBoxLayout() # Use VBox for vertical stack
        actions_layout.setSpacing(10)
        
        # Create Buttons (Icon based for compactness and style)
        # fixed_width=False to expand to 100%
        # User requested specific texts and styles: 14px, Black text
        
        btn_style = """
            QPushButton {
                text-align: left;
                padding-left: 15px;
                font-size: 18px;
                font-weight: bold;
                color: black;
            }
        """
        
        # Helper to apply extra style
        def apply_custom_style(btn):
            btn.setStyleSheet(btn.styleSheet() + btn_style)

        # 1. Limpiar Pantalla
        self.btn_clear = UIHelper.create_icon_button("fa5s.trash", "Limpiar Pantalla", icon_color=DANGER_COLOR, hover_color="#fee2e2", fixed_width=False)
        self.btn_clear.setText("  Limpiar Pantalla") # Add spaces for icon separation
        apply_custom_style(self.btn_clear)
        self.btn_clear.clicked.connect(self.clear_clicked.emit)
        
        # 2. Captura de Pantalla
        self.btn_screenshot = UIHelper.create_icon_button("fa5s.camera", "Captura de Pantalla", fixed_width=False)
        self.btn_screenshot.setText("  Captura de Pantalla")
        apply_custom_style(self.btn_screenshot)
        self.btn_screenshot.clicked.connect(self.screenshot_clicked.emit)
        
        # 3. Ayuda y Atajos
        self.btn_help = UIHelper.create_icon_button("fa5s.question-circle", "Ayuda y Atajos", fixed_width=False)
        self.btn_help.setText("  Ayuda y Atajos")
        apply_custom_style(self.btn_help)
        self.btn_help.clicked.connect(self.help_clicked.emit)
        
        # 4. Cerrar App
        self.btn_exit = UIHelper.create_icon_button("fa5s.sign-out-alt", "Cerrar App", icon_color=DANGER_COLOR, hover_color="#fee2e2", fixed_width=False)
        self.btn_exit.setText("  Cerrar App")
        apply_custom_style(self.btn_exit)
        self.btn_exit.clicked.connect(self.exit_clicked.emit)
        
        actions_layout.addWidget(self.btn_clear)
        actions_layout.addWidget(self.btn_screenshot)
        actions_layout.addWidget(self.btn_help)
        actions_layout.addWidget(self.btn_exit)
        
        card_layout.addLayout(actions_layout)
        layout.addWidget(self.card)
        
        # Spacer before footer
        layout.addStretch()
        
        # Github Logo (Footer) - 100px Icon Only
        self.btn_github = QPushButton()
        self.btn_github.setCursor(Qt.PointingHandCursor)
        self.btn_github.setFlat(True)
        # Icon
        icon =  qta.icon("fa5b.github", color="black")
        self.btn_github.setIcon(icon)
        self.btn_github.setIconSize(QSize(100, 100))
        self.btn_github.setFixedHeight(110) # slightly larger than icon
        self.btn_github.setStyleSheet("border: none; background: transparent;")
        
        self.btn_github.clicked.connect(self._open_github)
        
        # Center the github button
        github_layout = QHBoxLayout()
        github_layout.addStretch()
        github_layout.addWidget(self.btn_github)
        github_layout.addStretch()
        
        layout.addLayout(github_layout)
        
        # Version label debajo del GitHub icon
        self.version_label = QLabel("NixPen v1.0.0\nGPLv3 License")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 14px;
                font-weight: normal;
                margin-top: 0px;
                padding: 0px;
            }
        """)
        layout.addWidget(self.version_label)

    def _open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/PipeCalDev/ScreenPenVf") # Placeholder or real link

    def retranslateUi(self):
        # Update header text (finding QLabel child)
        for child in self.header_label.findChildren(QLabel):
            if not child.pixmap():
                child.setText(i18n.tr("actions", "section_title").upper())
                break
        
        # Update button visible texts
        self.btn_clear.setText(i18n.tr("actions", "btn_clear"))
        self.btn_screenshot.setText(i18n.tr("actions", "btn_screenshot"))
        self.btn_help.setText(i18n.tr("actions", "btn_help"))
        self.btn_exit.setText(i18n.tr("actions", "btn_exit"))
        
        # Update tooltips
        self.btn_clear.setToolTip(i18n.tr("actions", "clear_screen"))
        self.btn_screenshot.setToolTip(i18n.tr("actions", "screenshot"))
        self.btn_help.setToolTip(i18n.tr("actions", "help_shortcuts"))
        self.btn_exit.setToolTip(i18n.tr("actions", "exit_app"))
        
        # No info label anymore
        # self.info_label.setText(i18n.tr("actions", "help_hint"))

    update_texts = retranslateUi
