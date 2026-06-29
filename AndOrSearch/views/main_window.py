# views/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStatusBar, QListWidget
from PyQt5.QtCore import Qt
from views.components.grid_canvas import GridCanvas
from views.components.log_panel import LogPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Vacuum Cleaner 3x3 - AND-OR Search Only")
        self.resize(1100, 600)
        
        # Áp dụng theme nền tối tổng thể
        self.setStyleSheet("background-color: #0D1424; color: #FFFFFF;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- 1. SIDEBAR BÊN TRÁI (Chỉ giữ lại AND-OR Search) ---
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #141C2F; border-right: 1px solid #1A2333;")
        sidebar_layout = QVBoxLayout(sidebar)
        
        lbl_group = QLabel("Thuật Toán Kích Hoạt", sidebar)
        lbl_group.setStyleSheet("font-weight: bold; color: #4F637A; font-size: 12px; padding: 5px;")
        sidebar_layout.addWidget(lbl_group)
        
        self.algo_list = QListWidget(sidebar)
        # Đã loại bỏ hoàn toàn các thuật toán un-informed / local search khác
        self.algo_list.addItem("   AND-OR Graph Search")
        self.algo_list.setCurrentRow(0) 
        self.algo_list.setStyleSheet("""
            QListWidget { background-color: transparent; border: none; }
            QListWidget::item { height: 35px; color: #38B6FF; font-weight: bold; }
            QListWidget::item:selected { background-color: #1F2A45; color: #38B6FF; }
        """)
        sidebar_layout.addWidget(self.algo_list)
        main_layout.addWidget(sidebar)

        # --- 2. VÙNG TRUNG TÂM (Grid 3x3 + Nút bấm điều khiển) ---
        center_zone = QWidget()
        center_layout = QVBoxLayout(center_zone)
        center_layout.setAlignment(Qt.AlignCenter)

        self.grid_canvas = GridCanvas(self)
        center_layout.addWidget(self.grid_canvas)
        center_layout.addSpacing(20)

        button_layout = QHBoxLayout()
        self.btn_start = QPushButton("KÍCH HOẠT ROBOT", self)
        self.btn_start.setStyleSheet("""
            QPushButton { background-color: #0091FF; color: white; font-weight: bold; border-radius: 6px; padding: 12px 25px; font-size: 13px; }
            QPushButton:hover { background-color: #1A9CFF; }
        """)
        
        self.btn_random = QPushButton("ĐỔI BẢN ĐỒ NGẪU NHIÊN", self)
        self.btn_random.setStyleSheet("""
            QPushButton { background-color: #3A4454; color: #E1E6EB; font-weight: bold; border-radius: 6px; padding: 12px 25px; font-size: 13px; }
            QPushButton:hover { background-color: #4E5A6E; }
        """)
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_random)
        center_layout.addLayout(button_layout)
        
        main_layout.addWidget(center_zone, stretch=2)

        # --- 3. BẢNG LOG BÊN PHẢI ---
        self.log_panel = LogPanel(self)
        main_layout.addWidget(self.log_panel, stretch=1)

        # --- 4. THANH TRẠNG THÁI / KẾT QUẢ DƯỚI CÙNG ---
        self.status_bar = QStatusBar(self)
        self.status_bar.setStyleSheet("background-color: #0B101D; border-top: 1px solid #1A2333; min-height: 45px;")
        self.setStatusBar(self.status_bar)

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(15, 0, 15, 0)
        
        self.lbl_algo = QLabel("Thuật toán: Chưa chạy", self)
        self.lbl_steps = QLabel("Số bước di chuyển: 0", self)
        self.lbl_nodes = QLabel("Số Node đã duyệt: 0", self)
        self.lbl_time = QLabel("Thời gian tính toán: 0.00 ms", self)
        
        for lbl in [self.lbl_algo, self.lbl_steps, self.lbl_nodes, self.lbl_time]:
            lbl.setStyleSheet("color: #9AA6B5; font-size: 12px;")
            status_layout.addWidget(lbl)
            
        self.status_bar.addPermanentWidget(status_container, 1)