# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QPushButton
from PyQt5.QtCore import Qt

from ui.components.sidebar_widget import SidebarWidget
from ui.components.grid_widget import GridWidget
from ui.components.log_widget import LogWidget
from ui.components.result_widget import ResultWidget

class MainWindow(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = env  # Nhận dữ liệu môi trường từ main.py truyền vào
        self.selected_algo = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI Vacuum Cleaner 3x3 - Modular GUI")
        self.resize(1250, 750)
        self.setStyleSheet("background-color: #0f172a; color: #f1f5f9;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sử dụng QSplitter để người dùng có thể co kéo kích thước các vùng linh hoạt
        horizontal_splitter = QSplitter(Qt.Horizontal)

        # Vùng 1: Bên trái (Sidebar chọn thuật toán)
        self.sidebar = SidebarWidget()
        self.sidebar.itemClicked.connect(self.on_algo_selected)
        horizontal_splitter.addWidget(self.sidebar)

        # Vùng 2: Ở giữa (Lưới mô phỏng + Nút điều khiển)
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        
        self.grid_view = GridWidget()
        center_layout.addWidget(self.grid_view, alignment=Qt.AlignCenter)
        
        # Thanh điều khiển gồm nút chạy và nút đổi map
        btn_layout = QHBoxLayout()
        self.btn_run = QPushButton("KÍCH HOẠT ROBOT")
        self.btn_reset = QPushButton("ĐỔI BẢN ĐỒ NGẪU NHIÊN")
        
        self.btn_run.setStyleSheet("background-color: #0ea5e9; font-weight: bold; height: 38px; border-radius: 5px; color: white; font-size: 13px;")
        self.btn_reset.setStyleSheet("background-color: #475569; font-weight: bold; height: 38px; border-radius: 5px; color: white; font-size: 13px;")
        
        self.btn_reset.clicked.connect(self.on_reset_clicked)
        
        btn_layout.addWidget(self.btn_run)
        btn_layout.addWidget(self.btn_reset)
        center_layout.addLayout(btn_layout)
        horizontal_splitter.addWidget(center_container)

        # Vùng 3: Bên phải (Bảng log chi tiết)
        self.logger = LogWidget()
        horizontal_splitter.addWidget(self.logger)

        # Thiết lập tỉ lệ bề rộng hiển thị: Trái (220px), Giữa (580px), Phải (400px)
        horizontal_splitter.setSizes([220, 580, 400])
        main_layout.addWidget(horizontal_splitter)

        # Vùng 4: Bên dưới (Bảng thông số kết quả)
        self.result_panel = ResultWidget()
        main_layout.addWidget(self.result_panel)

        # Đồng bộ hóa hiển thị ban đầu từ Model môi trường lên giao diện
        self.sync_model_to_ui()

    def on_algo_selected(self, item, column):
        if item.childCount() == 0:  # Đảm bảo chỉ chọn thuật toán con (Lá của cây)
            self.selected_algo = item.text(0)
            self.logger.append_log(f"Đã chọn thuật toán: {self.selected_algo}")
            self.result_panel.update_results(self.selected_algo, 0, 0, 0.0)

    def on_reset_clicked(self):
        self.env.reset()
        self.sync_model_to_ui()
        self.logger.clear_log()
        self.logger.append_log("Đã tạo ngẫu nhiên một bản đồ rác mới.")

    def sync_model_to_ui(self):
        """Đọc dữ liệu mảng phẳng 9 ô và vị trí robot từ Model để vẽ lại UI"""
        self.grid_view.update_grid(self.env.grid, self.env.robot_pos)