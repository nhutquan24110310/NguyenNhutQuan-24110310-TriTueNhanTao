import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Stylesheet giao diện tối hiện đại
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e24;
        }
        QLabel {
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QPushButton {
            background-color: #3a3a43;
            color: white;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            font-weight: bold;
            border: none;
        }
        QPushButton:hover {
            background-color: #4f4f5a;
        }
        QPushButton:pressed {
            background-color: #2d2d35;
        }
        QTextEdit {
            background-color: #121214;
            color: #a9b7c6;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            border: 1px solid #3a3a43;
            border-radius: 6px;
        }
    """)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()