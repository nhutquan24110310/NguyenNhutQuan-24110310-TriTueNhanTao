from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI CSP Solver - Map Coloring")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Splitter chia 3 vùng: Bản đồ (giữa), Log (phải), Tree (dưới)
        splitter_horizontal = QSplitter(Qt.Horizontal)
        
        # Các widget placeholder (sẽ thay thế bằng class thực tế sau)
        self.map_widget = QWidget() # Sau này là MapWidget
        self.log_widget = QWidget() # Sau này là LogWidget
        self.tree_widget = QWidget() # Sau này là TreeWidget

        splitter_horizontal.addWidget(self.map_widget)
        splitter_horizontal.addWidget(self.log_widget)
        
        splitter_vertical = QSplitter(Qt.Vertical)
        splitter_vertical.addWidget(splitter_horizontal)
        splitter_vertical.addWidget(self.tree_widget)
        
        layout.addWidget(splitter_vertical)

        # Buttons điều khiển
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("KÍCH HOẠT ROBOT")
        self.random_btn = QPushButton("ĐỔI BẢN ĐỒ NGẪU NHIÊN")
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.random_btn)
        layout.addLayout(btn_layout)