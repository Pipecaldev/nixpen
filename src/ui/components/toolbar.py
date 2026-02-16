from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QApplication, QLabel, QButtonGroup, QSlider
from PyQt5.QtCore import Qt, pyqtSignal
from src.core.i18n import i18n
from src.ui.utils.styles import UIHelper, PRIMARY_COLOR, TEXT_PRIMARY
import qtawesome as qta

class ToolbarComponent(QWidget):
    """Barra de herramientas rediseñada estilo Gromit-MPX"""
    
    tool_changed = pyqtSignal(str)
    board_changed = pyqtSignal(str)
    thickness_changed = pyqtSignal(int)
    toggle_drawing = pyqtSignal(bool)
    screen_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.retranslateUi()
        i18n.languageChanged.connect(self.retranslateUi)
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(15)

        # 1. DISPLAY SECTION
        # No Card - Direct Layout
        display_layout = QVBoxLayout()
        display_layout.setContentsMargins(5, 5, 5, 5) # Reduced margins
        display_layout.setSpacing(8)
        
        self.lbl_display = UIHelper.create_section_header("DISPLAY", font_size=8)
        display_layout.addWidget(self.lbl_display)
        
        # Screen Combo
        self.screen_combo = QComboBox()
        self.screen_combo.setCursor(Qt.PointingHandCursor)
        self.screen_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 6px 10px;
                background-color: #f9fafb;
                color: black;
                font-size: 18px;
                font-weight: bold;
                min-height: 36px;
            }}
            QComboBox::drop-down {{ border: 0px; }}
            QComboBox QAbstractItemView {{
                font-size: 18px;
                font-weight: bold;
            }}
        """)
        self._populate_screens()
        self.screen_combo.currentIndexChanged.connect(self.screen_changed.emit)
        display_layout.addWidget(self.screen_combo)

        # Toggle Buttons (Active / Inactive) - Vertical Stack
        toggle_layout = QVBoxLayout()
        toggle_layout.setSpacing(5)
        
        # Create buttons using UIHelper but customize font size/padding manually for small space
        self.btn_draw_on = UIHelper.create_primary_button("ACTIVATE") 
        self.btn_draw_on.setCheckable(True)
        self.btn_draw_on.clicked.connect(lambda: self.toggle_drawing.emit(True))
        # Custom Font for small single line. Increased padding/height via Style/Size
        self.btn_draw_on.setFixedHeight(40) # Taller
        self.btn_draw_on.setStyleSheet(self.btn_draw_on.styleSheet() + "font-size: 10px; padding: 0 5px; QPushButton:checked { border: 2px solid black; }")
        
        self.btn_draw_off = UIHelper.create_danger_button("DEACTIVATE")
        self.btn_draw_off.setCheckable(True)
        self.btn_draw_off.clicked.connect(lambda: self.toggle_drawing.emit(False))
        self.btn_draw_off.setFixedHeight(40) # Taller
        # Custom Font for small single line
        self.btn_draw_off.setStyleSheet(self.btn_draw_off.styleSheet() + "font-size: 10px; padding: 0 5px; QPushButton:checked { border: 2px solid black; }")
        
        # Logic for toggle buttons styling (custom checkable behavior)
        self.draw_group = QButtonGroup()
        self.draw_group.addButton(self.btn_draw_on)
        self.draw_group.addButton(self.btn_draw_off)
        self.btn_draw_off.setChecked(True)
        
        toggle_layout.addWidget(self.btn_draw_on)
        toggle_layout.addWidget(self.btn_draw_off)
        display_layout.addLayout(toggle_layout)
        
        layout.addLayout(display_layout)

        # 2. TOOLS SECTION
        # No Card - Direct Layout
        tools_layout = QVBoxLayout()
        tools_layout.setContentsMargins(5, 5, 5, 5)
        tools_layout.setSpacing(8)
        
        self.lbl_tools = UIHelper.create_section_header("TOOLS", font_size=8)
        tools_layout.addWidget(self.lbl_tools)
        
        tools_grid = QGridLayout()
        tools_grid.setSpacing(5)
        # Use fixed_width=False to allow expanding, Size=50 for height
        self.pen_btn = UIHelper.create_icon_button("fa5s.pen", "Pen", size=50, icon_size=18, fixed_width=False)
        self.eraser_btn = UIHelper.create_icon_button("fa5s.eraser", "Eraser", size=50, icon_size=18, fixed_width=False)
        self.text_btn = UIHelper.create_icon_button("fa5s.font", "Text", size=50, icon_size=18, fixed_width=False)
        self.spotlight_btn = UIHelper.create_icon_button("fa5s.lightbulb", "Spotlight", size=50, icon_size=18, fixed_width=False)
        
        self._connect_tool(self.pen_btn, 'pen')
        self._connect_tool(self.eraser_btn, 'eraser')
        self._connect_tool(self.text_btn, 'text')
        self._connect_tool(self.spotlight_btn, 'spotlight')
        
        tools_grid.addWidget(self.pen_btn, 0, 0)
        tools_grid.addWidget(self.eraser_btn, 0, 1)
        tools_grid.addWidget(self.text_btn, 1, 0)
        tools_grid.addWidget(self.spotlight_btn, 1, 1)
        tools_layout.addLayout(tools_grid)
        
        layout.addLayout(tools_layout)
        
        # Tool Group
        self.tool_group = QButtonGroup()
        self.tool_group.addButton(self.pen_btn)
        self.tool_group.addButton(self.eraser_btn)
        self.tool_group.addButton(self.text_btn)
        self.tool_group.addButton(self.spotlight_btn)

        # 3. CANVAS & SHAPES
        # Canvas
        # No Card - Direct Layout
        canvas_layout = QVBoxLayout()
        canvas_layout.setContentsMargins(5, 5, 5, 5)
        canvas_layout.setSpacing(8)
        
        self.lbl_canvas = UIHelper.create_section_header("CANVAS", font_size=8)
        canvas_layout.addWidget(self.lbl_canvas)
        
        canvas_grid = QHBoxLayout()
        canvas_grid.setSpacing(5)
        # Increased size to 50 for taller buttons
        self.whiteboard_btn = UIHelper.create_icon_button("fa5s.chalkboard", "Whiteboard", size=50, icon_size=20, fixed_width=False)
        self.blackboard_btn = UIHelper.create_icon_button("fa5s.square", "Blackboard", size=50, icon_size=20, fixed_width=False)
        # Blackboard icon should be black
        self.blackboard_btn.setIcon(qta.icon("fa5s.square", color="black", color_active="black"))
        
        self.whiteboard_btn.clicked.connect(lambda: self.board_changed.emit('white'))
        self.blackboard_btn.clicked.connect(lambda: self.board_changed.emit('black'))
        
        self.tool_group.addButton(self.whiteboard_btn)
        self.tool_group.addButton(self.blackboard_btn)
        
        canvas_grid.addWidget(self.whiteboard_btn)
        canvas_grid.addWidget(self.blackboard_btn)
        canvas_layout.addLayout(canvas_grid)
        layout.addLayout(canvas_layout)

        # Shapes
        # No Card - Direct Layout
        shapes_layout = QVBoxLayout()
        shapes_layout.setContentsMargins(5, 5, 5, 5)
        shapes_layout.setSpacing(8)
        
        self.lbl_shapes = UIHelper.create_section_header("SHAPES", font_size=8)
        shapes_layout.addWidget(self.lbl_shapes)
        
        shapes_grid = QGridLayout()
        shapes_grid.setSpacing(5)
        # Increased size to 50 for taller buttons
        self.line_btn = UIHelper.create_icon_button("fa5s.slash", "Line", size=50, icon_size=18, fixed_width=False)
        self.arrow_btn = UIHelper.create_icon_button("fa5s.location-arrow", "Arrow", size=50, icon_size=18, fixed_width=False)
        self.rect_btn = UIHelper.create_icon_button("fa5s.vector-square", "Rectangle", size=50, icon_size=18, fixed_width=False)
        self.ellipse_btn = UIHelper.create_icon_button("fa5s.circle", "Ellipse", size=50, icon_size=18, fixed_width=False)
        
        self._connect_tool(self.line_btn, 'line')
        self._connect_tool(self.arrow_btn, 'arrow')
        self._connect_tool(self.rect_btn, 'rect')
        self._connect_tool(self.ellipse_btn, 'ellipse')
        
        self.tool_group.addButton(self.line_btn)
        self.tool_group.addButton(self.arrow_btn)
        self.tool_group.addButton(self.rect_btn)
        self.tool_group.addButton(self.ellipse_btn)
        
        shapes_grid.addWidget(self.line_btn, 0, 0)
        shapes_grid.addWidget(self.arrow_btn, 0, 1)
        shapes_grid.addWidget(self.rect_btn, 1, 0)
        shapes_grid.addWidget(self.ellipse_btn, 1, 1)
        shapes_layout.addLayout(shapes_grid)
        layout.addLayout(shapes_layout)

        # 4. STROKE
        # Label Title outside card
        stroke_layout = QVBoxLayout()
        stroke_layout.setContentsMargins(5, 5, 5, 5)
        stroke_layout.setSpacing(8)
        
        self.lbl_stroke = UIHelper.create_section_header("STROKE", font_size=8)
        stroke_layout.addWidget(self.lbl_stroke)
        
        # Card specifically for the slider content
        slider_card = UIHelper.create_card_section()
        slider_layout = QVBoxLayout(slider_card)
        slider_layout.setContentsMargins(10, 5, 10, 5) # Compact margins
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(4)
        self.slider.setCursor(Qt.PointingHandCursor)
        self.slider.valueChanged.connect(self._on_thickness_change)
        # Estilo Slider Minimalista
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 1px solid #e5e7eb;
                background: #f3f4f6;
                height: 6px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {PRIMARY_COLOR};
                border: 2px solid white;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 9px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
        """)
        
        slider_layout.addWidget(self.slider)
        stroke_layout.addWidget(slider_card) # Add card to section layout
        
        self.value_label = QLabel("4 px")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(f"color: {TEXT_PRIMARY}; font-weight: bold; font-size: 12px;")
        stroke_layout.addWidget(self.value_label)
        
        layout.addLayout(stroke_layout)
        
        # Spacer
        layout.addStretch()
        
        # Set default
        self.pen_btn.setChecked(True)

    def _connect_tool(self, btn, tool_id):
        btn.clicked.connect(lambda: self.tool_changed.emit(tool_id))

    def _populate_screens(self):
        screens = QApplication.screens()
        current_index = self.screen_combo.currentIndex()
        self.screen_combo.clear()
        
        prefix = i18n.tr("toolbar", "screen_prefix")
        
        for i, screen in enumerate(screens):
            geo = screen.geometry()
            self.screen_combo.addItem(f"{prefix} {i+1} ({geo.width()}x{geo.height()})")
            
        if current_index >= 0 and current_index < self.screen_combo.count():
            self.screen_combo.setCurrentIndex(current_index)

    def _on_thickness_change(self, value):
        self.value_label.setText(f"{value} px")
        self.thickness_changed.emit(value)

    def set_tool(self, tool_name):
        mapping = {
            'pen': self.pen_btn, 'eraser': self.eraser_btn,
            'text': self.text_btn, 'spotlight': self.spotlight_btn,
            'line': self.line_btn, 'arrow': self.arrow_btn,
            'rect': self.rect_btn, 'ellipse': self.ellipse_btn
        }
        if tool_name in mapping:
            mapping[tool_name].setChecked(True)

    def retranslateUi(self):
        # Helper to update text in header containers
        def update_header_text(container, text):
            # Find the QLabel child that is not the icon (icon has pixmap)
            for child in container.findChildren(QLabel):
                if not child.pixmap(): 
                    child.setText(text.upper())
                    break
        
        # Update headers
        update_header_text(self.lbl_display, i18n.tr("toolbar", "screens_title"))
        update_header_text(self.lbl_tools, i18n.tr("toolbar", "title_tools"))
        update_header_text(self.lbl_canvas, i18n.tr("toolbar", "title_bg"))
        update_header_text(self.lbl_shapes, i18n.tr("toolbar", "title_shapes"))
        update_header_text(self.lbl_stroke, i18n.tr("toolbar", "title_thick"))
        
        self.btn_draw_on.setText(i18n.tr("toolbar", "activate"))
        self.btn_draw_off.setText(i18n.tr("toolbar", "deactivate"))
        
        # Repopulate screens to update "Pantalla"/"Screen" prefix
        self._populate_screens()
        
        # Tooltips 
        self.pen_btn.setToolTip(i18n.tr("toolbar", "tooltip_pen"))
        self.eraser_btn.setToolTip(i18n.tr("toolbar", "tooltip_eraser"))
        self.text_btn.setToolTip(i18n.tr("toolbar", "tooltip_text"))
        self.spotlight_btn.setToolTip(i18n.tr("toolbar", "tooltip_spot"))
        
        self.line_btn.setToolTip(i18n.tr("toolbar", "tooltip_line"))
        self.arrow_btn.setToolTip(i18n.tr("toolbar", "tooltip_arrow"))
        self.rect_btn.setToolTip(i18n.tr("toolbar", "tooltip_rect"))
        self.ellipse_btn.setToolTip(i18n.tr("toolbar", "tooltip_ellipse"))
        
        self.whiteboard_btn.setToolTip(i18n.tr("toolbar", "tooltip_white"))
        self.blackboard_btn.setToolTip(i18n.tr("toolbar", "tooltip_black"))
        
        # Tooltips adicionales
        self.screen_combo.setToolTip(i18n.tr("toolbar", "screen_selector"))
        self.btn_draw_on.setToolTip(i18n.tr("toolbar", "activate"))
        self.btn_draw_off.setToolTip(i18n.tr("toolbar", "deactivate"))
        self.slider.setToolTip(i18n.tr("toolbar", "thickness_slider"))

    update_texts = retranslateUi

