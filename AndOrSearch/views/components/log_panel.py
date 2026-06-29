# views/components/log_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tiêu đề Log
        title = QLabel("NHẬT KÝ HOẠT ĐỘNG (LOG)", self)
        title.setStyleSheet("color: #8A99AD; font-weight: bold; font-size: 12px; margin-bottom: 5px;")
        layout.addWidget(title)

        # Khung chứa nội dung văn bản log
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)
        # Giao diện text kiểu console lập trình viên
        self.log_area.setStyleSheet("""
            background-color: #090D16; 
            color: #00FF66; 
            font-family: 'Consolas', 'Monaco', monospace; 
            font-size: 13px; 
            border: 1px solid #1A2333; 
            border-radius: 6px;
            padding: 8px;
        """)
        layout.addWidget(self.log_area)

    def write_log(self, message):
        """Thêm một dòng log mới"""
        self.log_area.append(message)

    def clear_log(self):
        """Xóa sạch bảng log"""
        self.log_area.clear()