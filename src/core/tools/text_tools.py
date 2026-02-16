from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QColor
from .base_tool import Tool

class TextTool(Tool):
    def __init__(self):
        super().__init__()
        self.current_input = None

    def mouse_press(self, event, canvas):
        if event.button() == Qt.LeftButton:
            # Si ya hay un input activo, confirmamos el texto anterior
            if self.current_input:
                self._commit_text(canvas)
                return

            # Crear nuevo input en la posición del click
            self._create_input(event.pos(), canvas)

    def mouse_move(self, event, canvas):
        pass

    def mouse_release(self, event, canvas):
        pass

    def _create_input(self, pos, canvas):
        # 1. Habilitar foco temporalmente en el canvas
        self.original_flags = canvas.windowFlags()
        # Quitamos WindowDoesNotAcceptFocus para permitir escribir
        canvas.setWindowFlags(self.original_flags & ~Qt.WindowDoesNotAcceptFocus)
        canvas.show() # setWindowFlags oculta la ventana, hay que mostrarla de nuevo
        
        self.current_input = QLineEdit(canvas)
        self.current_input.move(pos)
        self.current_input.setPlaceholderText("Escribe aquí...")
        
        # Estilo transparente para integrarse con el canvas
        font_size = max(12, self.pen_width * 3) # Escalar fuente con grosor
        font = QFont('Arial', font_size)
        self.current_input.setFont(font)
        
        # Color del texto (convertir QColor a string rgb)
        c = self.color
        rgb = f"rgb({c.red()}, {c.green()}, {c.blue()})"
        
        self.current_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: rgba(255, 255, 255, 200);
                border: 1px dashed #ccc;
                color: {rgb};
                border-radius: 4px;
                padding: 2px;
            }}
        """)
        
        self.current_input.returnPressed.connect(lambda: self._commit_text(canvas))
        self.current_input.show()
        self.current_input.setFocus()
        canvas.activateWindow() # Importante para traer el foco
        
        # Ajustar tamaño al contenido
        self.current_input.textChanged.connect(self._adjust_size)
        self._adjust_size()

    def _adjust_size(self):
        if self.current_input:
            width = self.current_input.fontMetrics().boundingRect(self.current_input.text() + "  ").width()
            width = max(150, width) # Ancho mínimo
            self.current_input.resize(width, self.current_input.height())

    def _commit_text(self, canvas):
        if not self.current_input:
            return

        text = self.current_input.text()
        if text.strip():
            # Delegar el pintado al canvas para manejar undo/redo
            canvas.draw_text_content(
                text, 
                self.current_input.pos(), 
                self.current_input.font(), 
                self.color
            )
        
        self.current_input.deleteLater()
        self.current_input = None
        
        # 2. Restaurar flags originales (volver a ser click-through para foco)
        if hasattr(self, 'original_flags'):
            canvas.setWindowFlags(self.original_flags)
            canvas.show()
