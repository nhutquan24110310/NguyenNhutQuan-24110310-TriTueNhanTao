# ui/components/log_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        lbl = QLabel("NHẬT KÝ HOẠT ĐỘNG (LOG)")
        lbl.setStyleSheet("font-weight: bold; color: #94a3b8; font-size: 12px;")
        layout.addWidget(lbl)
        
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            background-color: #020617; 
            color: #22c55e; 
            font-family: 'Consolas', monospace; 
            font-size: 12px; 
            border: 1px solid #334155; 
            border-radius: 4px;
            padding: 5px;
        """)
        layout.addWidget(self.txt_log)

    def append_log(self, message):
        self.txt_log.append(f"> {message}")

    def clear_log(self):
        self.txt_log.clear()