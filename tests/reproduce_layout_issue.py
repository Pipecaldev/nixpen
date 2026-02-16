import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.ui.windows.control_panel import ControlPanel
    print("Import successful")
except Exception as e:
    print(f"Import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

def debug_layout():
    try:
        app = QApplication(sys.argv)
        window = ControlPanel()
        window.show()
        
        print(f"Initial Size: {window.size()}")
        
        def on_toggle():
            try:
                print("\n--- Toggling View to Vertical ---")
                window.toggle_view()
                
                app.processEvents()
                
                print(f"Collapsed: {window.is_collapsed}")
                print(f"Window Size: {window.size()}")
                
                v_toolbar = window.vertical_toolbar
                print(f"Vertical Toolbar Visible: {v_toolbar.isVisible()}")
                print(f"Vertical Toolbar Size: {v_toolbar.size()}")
                print(f"Vertical Toolbar SizeHint: {v_toolbar.sizeHint()}")
                
                # Check actual buttons
                layout = v_toolbar.layout()
                count = layout.count()
                print(f"Items in Toolbar Layout: {count}")
                
                hint = v_toolbar.sizeHint()
                if hint.height() < 800:
                    print("WARNING: Vertical Toolbar SizeHint is suspiciously small (< 800px)")
                else:
                    print("Vertical Toolbar SizeHint seems reasonable")

            except Exception as e:
                print(f"Error during toggle: {e}")
                traceback.print_exc()
            finally:
                QTimer.singleShot(500, app.quit)

        QTimer.singleShot(1000, on_toggle)
        app.exec_()
        print("Test finished")
        
    except Exception as e:
        print(f"Test crashed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_layout()
