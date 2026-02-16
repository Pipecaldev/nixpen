from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QApplication, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect, QStackedLayout)
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer
from PyQt5.QtGui import QIcon, QColor, QKeySequence

from src.config import *
from src.ui.components.header import HeaderComponent
from src.ui.components.toolbar import ToolbarComponent
from src.ui.components.actions import ActionsComponent
from src.ui.components.color_grid import ColorGridComponent
from src.ui.components.vertical_toolbar import VerticalToolbar
from src.ui.widgets.drawing_canvas import DrawingCanvas
from src.ui.windows.help_dialog import HelpDialog
from src.core.utils import get_initial_position

class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.drag_position = None
        self.is_collapsed = False
        self.drawing_enabled = False # Estado inicial: Dibujo desactivado (cursor normal)
        
        self.initUI()
        self.setup_connections()
        self.setup_initial_geometry()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.central_widget = QWidget()
        self.central_widget.setObjectName("ControlPanel")
        self.setCentralWidget(self.central_widget)
        
        # --- Layout Principal (VBox simple) ---
        # Usamos VBox en lugar de Stack para que al ocultar widgets, 
        # el layout realmente ignore su tamaño y permita reducir la ventana.
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        tooltip_bg = "#ecf0f1"
        tooltip_text = "#2c3e50"
        
        # Stylesheet
        self.setStyleSheet(f"""
            QWidget#ControlPanel {{
                background-color: {BACKGROUND_COLOR};
                border-radius: 20px;
                border: 1px solid #333;
            }}
            QToolTip {{
                background-color: {tooltip_bg};
                color: {tooltip_text};
                border: 1px solid #333;
            }}
        """)
        
        # --- MODO 0: VISUALIZACIÓN NORMAL ---
        self.normal_widget = QWidget()
        self.normal_layout = QVBoxLayout(self.normal_widget)
        self.normal_layout.setContentsMargins(0, 0, 0, 0)
        self.normal_layout.setSpacing(0)
        
        # Componentes Normales
        self.header = HeaderComponent()
        self.normal_layout.addWidget(self.header)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(15, 10, 15, 20)
        self.content_layout.setSpacing(15)
        
        self.toolbar = ToolbarComponent()
        self.content_layout.addWidget(self.toolbar)
        
        self.color_grid = ColorGridComponent()
        self.content_layout.addWidget(self.color_grid)
        
        self.actions = ActionsComponent()
        self.content_layout.addWidget(self.actions)
        
        self.normal_layout.addWidget(self.content_widget)
        
        # Añadir al Main Layout
        self.main_layout.addWidget(self.normal_widget)
        
        # --- MODO 1: BARRA VERTICAL ---
        self.vertical_toolbar = VerticalToolbar(self)
        self.vertical_toolbar.hide() # Oculto inicialmente
        # Añadir al Main Layout
        self.main_layout.addWidget(self.vertical_toolbar)
        
        # Canvas (Overlay)
        screen_geometry = QApplication.primaryScreen().geometry()
        self.canvas = DrawingCanvas(screen_geometry)
        self.canvas.hide()

    def setup_connections(self):
        """Conecta señales de componentes a métodos del controlador"""
        # Header
        self.header.collapse_clicked.connect(self.toggle_view)
        self.header.minimize_clicked.connect(self.showMinimized)
        self.header.close_clicked.connect(self.close_app)
        self.header.help_clicked.connect(self.show_help)
        self.header.language_changed.connect(self.update_texts)
        
        # Toolbar
        self.toolbar.tool_changed.connect(self._on_tool_changed)
        self.toolbar.thickness_changed.connect(self.canvas.setPenWidth)
        self.toolbar.board_changed.connect(self.toggle_board)
        self.toolbar.toggle_drawing.connect(self.set_drawing_enabled)
        self.toolbar.screen_changed.connect(self._on_screen_changed)
        
        # Colors
        self.color_grid.color_selected.connect(self._on_color_selected)
        
        # Actions
        self.actions.clear_clicked.connect(self.canvas.clearCanvas)
        self.actions.screenshot_clicked.connect(self.take_screenshot)
        self.actions.help_clicked.connect(self.show_help)
        self.actions.exit_clicked.connect(self.close_app)
        
        # Vertical Toolbar
        self.vertical_toolbar.expand_clicked.connect(self.toggle_view)
        self.vertical_toolbar.tool_selected.connect(self._on_vertical_tool_selected)
        self.vertical_toolbar.action_triggered.connect(self._on_vertical_action_triggered)
        self.vertical_toolbar.color_selected.connect(self._select_color_by_index)

    def setup_initial_geometry(self):
        x, y = get_initial_position(DEFAULT_WIDTH, DEFAULT_WIDTH) # Placeholder height
        self.setGeometry(x, y, DEFAULT_WIDTH, 600) # Altura inicial aprox

    def _on_tool_changed(self, tool_name):
        self.canvas.setTool(tool_name)
        if not self.drawing_enabled and tool_name != 'cursor':
            self.toggle_drawing()

    def _on_color_selected(self, color_code):
        self.canvas.setColor(QColor(color_code))
        self.toolbar.update_icon_colors(color_code)

    def _select_color_by_index(self, index):
        # Selecciona color en color_grid simulando click
        # Esto es un helper para atajos y barra vertical
        buttons = self.color_grid.btn_group.buttons()
        if 0 <= index < len(buttons):
            buttons[index].click()
            # Actualizar UI visualmente si es necesario

    def _on_screen_changed(self, index):
        screens = QApplication.screens()
        if 0 <= index < len(screens):
            screen = screens[index]
            geometry = screen.geometry()
            
            # 1. Mover Canvas
            self.canvas.setGeometry(geometry)
            
            # 2. Mover Panel de Control (Centrado en la nueva pantalla)
            # Calcular posición centrada
            center_point = geometry.center()
            frame_geometry = self.frameGeometry()
            frame_geometry.moveCenter(center_point)
            self.move(frame_geometry.topLeft())
            
            self._update_canvas_mask() # Actualizar máscara en nueva pantalla

    def set_drawing_enabled(self, enabled):
        """Setter explícito para los botones ON/OFF"""
        if self.drawing_enabled != enabled:
            self.toggle_drawing()

    def toggle_drawing(self):
        self.drawing_enabled = not self.drawing_enabled
        
        if self.drawing_enabled:
            # 1. Asegurar configuración para dibujar
            self.canvas.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            
            # Limpiar flag de transparencia de input si existe
            if hasattr(Qt, 'WindowTransparentForInput'):
                flags = self.canvas.windowFlags()
                flags &= ~Qt.WindowTransparentForInput
                self.canvas.setWindowFlags(flags)
            
            self.canvas.show() # MOSTRAR TRAZOS
            
            # Sincronizar botones visualmente
            self.toolbar.btn_draw_on.setChecked(True)
            self.toolbar.btn_draw_off.setChecked(False)
            self._update_canvas_mask() # APLICAR MÁSCARA
        else:
            self.canvas.hide() # OCULTAR TRAZOS (Permite click-through total)
            
            self.canvas.setTool('cursor') # Resetear a cursor
            # Sincronizar botones visualmente
            self.toolbar.btn_draw_on.setChecked(False)
            self.toolbar.btn_draw_off.setChecked(True)
            # No es necesario clearMask si está oculto
            
        # Sincronizar estado visual de Vertical Toolbar
        self._sync_vertical_toolbar_state()

    def toggle_board(self, board_type):
        if board_type == 'none':
            self.canvas.set_background(Qt.transparent)
        elif board_type == 'white':
            self.canvas.set_background(Qt.white)
        elif board_type == 'black':
            self.canvas.set_background(Qt.black)

    def toggle_view(self):
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            # --- MODO BARRA VERTICAL ---
            self.normal_widget.hide()
            self.vertical_toolbar.show()
            self.vertical_toolbar.set_minimized(False)
            
            # Liberar restricciones
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
            
            # Ajustar tamaño explícito basado en el contenido de la barra vertical
            # Usar sizeHint() para la altura y el ancho fijo del toolbar
            toolbar_hint = self.vertical_toolbar.sizeHint()
            target_width = self.vertical_toolbar.width() # Debería ser 100
            target_height = toolbar_hint.height()
            
            # Añadir un pequeño margen de seguridad si es necesario
            self.resize(target_width, target_height)
            self.setFixedSize(target_width, target_height)
             
        else:
            # --- MODO PANEL COMPLETO ---
            self.vertical_toolbar.hide()
            self.normal_widget.show()
            
            # Restaurar restricciones de ancho fijo pero altura dinámica
            self.setFixedWidth(DEFAULT_WIDTH)
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)
            
            # Forzar recálculo de geometría basado en el contenido visible (normal_widget)
            self.normal_widget.adjustSize()
            self.adjustSize()

    # Método _sync_vertical_toolbar_state eliminado/inutilizado por la nueva lógica robusta
    def _sync_vertical_toolbar_state(self):
        pass

    def _on_vertical_tool_selected(self, tool_id):
        if tool_id == 'cursor':
            # Modo cursor: Pausar dibujo (ocultar canvas) pero NO MINIMIZAR la barra
            if self.drawing_enabled:
                self.toggle_drawing()
        else:
            # Herramientas de dibujo: Activar canvas si está apagado
            if not self.drawing_enabled:
                self.toggle_drawing()
            
            # Seleccionar herramienta
            self.canvas.setTool(tool_id)
            self.toolbar.set_tool(tool_id) # Sincronizar toolbar original
            
            # Actualizar botón activo en barra vertical
            self.vertical_toolbar.set_active_tool(tool_id)

    def _on_vertical_action_triggered(self, action_id):
        if action_id == 'visibility':
            # Toggle minimizar/expandir la barra vertical
            is_min = not self.vertical_toolbar.is_minimized
            self.vertical_toolbar.set_minimized(is_min)
            
            if is_min:
                # Fondo transparente y ventana del tamaño del botón
                self.central_widget.setStyleSheet("""
                    QWidget#ControlPanel {
                        background-color: transparent;
                        border: none;
                    }
                """)
                self.setMinimumSize(0, 0)
                self.setMaximumSize(16777215, 16777215)
                self.setFixedSize(58, 58)
            else:
                # Restaurar fondo y tamaño de la barra completa
                self.central_widget.setStyleSheet(f"""
                    QWidget#ControlPanel {{
                        background-color: {BACKGROUND_COLOR};
                        border-radius: 20px;
                        border: 1px solid #333;
                    }}
                """)
                self.setMinimumSize(0, 0)
                self.setMaximumSize(16777215, 16777215)
                toolbar_hint = self.vertical_toolbar.sizeHint()
                target_width = self.vertical_toolbar.width()
                target_height = toolbar_hint.height()
                self.resize(target_width, target_height)
                self.setFixedSize(target_width, target_height)
            
        elif action_id == 'undo':
            self.canvas.undo()
        elif action_id == 'clear':
            self.canvas.clearCanvas()
        elif action_id == 'screenshot':
            self.take_screenshot()

    def take_screenshot(self):
        from PyQt5.QtWidgets import QFileDialog
        from datetime import datetime
        import os
        
        # Ocultar UI
        self.hide()
        if self.is_collapsed:
            self.vertical_toolbar.hide()
        
        QApplication.processEvents()
        
        # Capturar
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        
        # Mostrar UI
        self.show()
        if self.is_collapsed:
            self.vertical_toolbar.show()
            
        # Guardar
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar Captura", 
                                                 f"ScreenPen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                                 "Images (*.png);;All Files (*)", options=options)
        if file_name:
            screenshot.save(file_name)

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec_()

    def close_app(self):
        self.canvas.close()
        self.close()

    def update_texts(self):
        """Actualiza los textos de la interfaz al cambiar idioma"""
        self.header.update_texts()
        self.toolbar.update_texts()
        self.actions.update_texts()
        # TODO: Vertical toolbar update texts if needed

    # --- Eventos de Teclado Globales ---
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        
        # Global shortcuts logic
        if key == Qt.Key_D and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.toggle_drawing()
        elif key == Qt.Key_C and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.canvas.clearCanvas()
        elif key == Qt.Key_H and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.show_help()
        elif key == Qt.Key_Z and modifiers == Qt.ControlModifier:
            self.canvas.undo()
        elif key == Qt.Key_Y and modifiers == Qt.ControlModifier:
            self.canvas.redo()
        elif key == Qt.Key_W and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.canvas.set_background(Qt.white)
        elif key == Qt.Key_B and modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            self.canvas.set_background(Qt.black)
        elif key == Qt.Key_Escape:
            # Ya no cerramos la app con Escape para evitar accidentes
            pass
        
        # Shortcuts para Herramientas (Ctrl+Shift+Letra)
        elif modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            if key == Qt.Key_P: self._on_tool_changed('pen')
            elif key == Qt.Key_E: self._on_tool_changed('eraser')
            elif key == Qt.Key_L: self._on_tool_changed('line')
            elif key == Qt.Key_A: self._on_tool_changed('arrow')
            elif key == Qt.Key_R: self._on_tool_changed('rect')
            elif key == Qt.Key_M: self._on_tool_changed('ellipse')
            elif key == Qt.Key_T: self._on_tool_changed('text')
            elif key == Qt.Key_S: self._on_tool_changed('spotlight')
            
            # Shortcuts para Colores (Ctrl+Shift+Número)
            elif key == Qt.Key_1: self._select_color_by_index(0)
            elif key == Qt.Key_2: self._select_color_by_index(1)
            elif key == Qt.Key_3: self._select_color_by_index(2)
            elif key == Qt.Key_4: self._select_color_by_index(3)
            elif key == Qt.Key_5: self._select_color_by_index(4)
            elif key == Qt.Key_6: self._select_color_by_index(5)
            elif key == Qt.Key_7: self._select_color_by_index(6)

    # --- Lógica de Arrastre ventana principal ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self._update_canvas_mask() # Actualizar máscara al soltar

    def moveEvent(self, event):
        super().moveEvent(event)
        self._update_canvas_mask()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_canvas_mask()

    def _update_canvas_mask(self):
        """
        Crea un 'agujero' en el canvas para permitir interacción con el panel de control
        cuando ambos están superpuestos.
        """
        if not self.drawing_enabled:
            return

        # Solo aplicar máscara si el panel está en la misma pantalla que el canvas
        # Asumimos que self.canvas.geometry() es la pantalla activa
        
        canvas_geo = self.canvas.geometry()
        panel_geo = self.geometry()
        
        # Verificar intersección
        if canvas_geo.intersects(panel_geo):
            # Calcular geometría relativa al canvas (coordenadas globales)
            # El canvas cubre toda la pantalla seleccionada, sus coordenadas son globales
            # QRegion maneja coordenadas globales si se usa con QCursor, pero para setMask
            # en un widget, son relativas al widget.
            # Como DrawingCanvas es full screen, sus 0,0 pueden ser 0,0 global o desplazados.
            # DrawingCanvas es Frameless ysetGeometry se le paso screen.geometry()
            
            # Obtener región de la pantalla completa (relativa al canvas 0,0)
            from PyQt5.QtGui import QRegion, QBitmap
            
            # Región completa del canvas
            full_region = QRegion(0, 0, canvas_geo.width(), canvas_geo.height())
            
            # Región del panel (convertida a coordenadas locales del canvas)
            # Panel global pos: self.pos()
            # Canvas global pos: canvas_geo.topLeft()
            
            local_panel_pos = self.pos() - canvas_geo.topLeft()
            panel_rect = self.rect() # Tamaño del panel
            panel_region = QRegion(local_panel_pos.x(), local_panel_pos.y(), 
                                 panel_rect.width(), panel_rect.height())
            
            # Restar la región del panel (crear agujero)
            masked_region = full_region.subtracted(panel_region)
            
            self.canvas.setMask(masked_region)
        else:
            self.canvas.clearMask()
