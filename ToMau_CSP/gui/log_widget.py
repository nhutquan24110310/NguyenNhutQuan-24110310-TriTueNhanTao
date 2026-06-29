from PyQt5.QtWidgets import QTextEdit

class LogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setPlaceholderText("Nhật ký hoạt động sẽ hiện ở đây...")
        self.setStyleSheet("background-color: #282a36; color: #f8f8f2;")

    def add_log(self, message):
        self.append(message)