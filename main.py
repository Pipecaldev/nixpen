#!/usr/bin/env python3
"""
Screen Pen - Punto de Entrada
"""
import sys
from PyQt5.QtWidgets import QApplication
from src.ui.windows.control_panel import ControlPanel
from src.core.logging_config import setup_logging
from src.config import STYLESHEET_GLOBAL
import logging

def main():
    log_file = setup_logging()
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET_GLOBAL) # Apply global font/styles
    logging.info(f"Logs guardados en: {log_file}")
    
    # Crear y mostrar panel de control
    window = ControlPanel()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
