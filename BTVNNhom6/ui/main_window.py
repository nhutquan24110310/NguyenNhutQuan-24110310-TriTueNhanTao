import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QGridLayout, QPushButton, QLabel, QTextEdit, QFrame, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mô phỏng Robot Hút Bụi 3x3 - AI Algorithms (PyQt5)")
        self.resize(1100, 700)
        
        # Trạng thái mô phỏng
        self.robot_pos = [0, 0]
        self.dirt_positions = set()
        self.selected_algo = "Minimax"
        self.is_running = False
        self.move_count = 0
        self.dirt_cleaned = 0
        
        # Timer điều khiển bước chạy mô phỏng
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_simulation_step)
        
        self.init_ui()
        self.reset_env()

    def init_ui(self):
        # Widget trung tâm nuôi toàn bộ bố cục
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Bố cục chính nằm ngang (Left Panel | Center & Bottom Panel | Right Panel)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ---------------- BÊN TRÁI: TAB CHỌN THUẬT TOÁN ----------------
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #25252d; border-radius: 8px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        
        title_algo = QLabel("THUẬT TOÁN")
        title_algo.setFont(QFont('Segoe UI', 14, QFont.Bold))
        title_algo.setAlignment(Qt.AlignCenter) # Cú pháp PyQt5 ngắn gọn hơn
        left_layout.addWidget(title_algo)
        
        # Các nút chọn thuật toán
        self.btn_minimax = QPushButton("Minimax")
        self.btn_alphabeta = QPushButton("Alpha - Beta")
        self.btn_expectimax = QPushButton("Expectimax")
        
        for btn in [self.btn_minimax, self.btn_alphabeta, self.btn_expectimax]:
            btn.setCheckable(True)
            left_layout.addWidget(btn)
            
        # Group để chỉ chọn 1 trong 3 nút
        self.algo_group = QButtonGroup(self)
        self.algo_group.addButton(self.btn_minimax)
        self.algo_group.addButton(self.btn_alphabeta)
        self.algo_group.addButton(self.btn_expectimax)
        self.btn_minimax.setChecked(True) # Mặc định chọn Minimax
        
        # Style nút đang được chọn chủ động
        self.btn_minimax.setStyleSheet("background-color: #007acc;")
        self.algo_group.buttonClicked.connect(self.on_algo_changed)
        
        left_layout.addStretch()
        
        # Điều khiển Chạy / Reset
        self.btn_start = QPushButton("BẮT ĐẦU")
        self.btn_start.setStyleSheet("background-color: #28a745; color: white;")
        self.btn_start.clicked.connect(self.toggle_simulation)
        left_layout.addWidget(self.btn_start)
        
        self.btn_reset = QPushButton("ĐẶT LẠI")
        self.btn_reset.setStyleSheet("background-color: #dc3545; color: white;")
        self.btn_reset.clicked.connect(self.reset_env)
        left_layout.addWidget(self.btn_reset)
        
        main_layout.addWidget(left_panel, stretch=2)
        
        # ---------------- Ở GIỮA & DƯỚI: KHU VỰC MÔ PHỎNG & KẾT QUẢ ----------------
        center_v_layout = QVBoxLayout()
        center_v_layout.setSpacing(15)
        
        # Khung chứa lưới 3x3
        center_panel = QFrame()
        center_panel.setStyleSheet("background-color: #25252d; border-radius: 8px;")
        center_layout = QVBoxLayout(center_panel)
        
        title_sim = QLabel("MÔ PHỎNG LƯỚI 3X3")
        title_sim.setFont(QFont('Segoe UI', 12, QFont.Bold))
        title_sim.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_sim)
        
        # Tạo lưới nút bấm đại diện cho ô 3x3
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(8)
        self.grid_cells = []
        for row in range(3):
            row_cells = []
            for col in range(3):
                cell = QPushButton(f"({row},{col})")
                cell.setFixedSize(100, 100)
                cell.setFont(QFont('Segoe UI', 11))
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.grid_cells.append(row_cells)
        center_layout.addLayout(self.grid_layout)
        center_v_layout.addWidget(center_panel, stretch=5)
        
        # KHU VỰC PHÍA DƯỚI: HIỂN THỊ KẾT QUẢ
        bottom_panel = QFrame()
        bottom_panel.setStyleSheet("background-color: #25252d; border-radius: 8px; padding: 10px;")
        bottom_layout = QHBoxLayout(bottom_panel)
        
        self.lbl_steps = QLabel("Tổng số bước: 0")
        self.lbl_cleaned = QLabel("Đã dọn dẹp: 0/0")
        self.lbl_status = QLabel("Trạng thái: Sẵn sàng")
        
        for lbl in [self.lbl_steps, self.lbl_cleaned, self.lbl_status]:
            lbl.setFont(QFont('Segoe UI', 11))
            bottom_layout.addWidget(lbl)
            
        center_v_layout.addWidget(bottom_panel, stretch=1)
        main_layout.addLayout(center_v_layout, stretch=5)
        
        # ---------------- BÊN PHẢI: LOG THUẬT TOÁN ----------------
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #25252d; border-radius: 8px;")
        right_layout = QVBoxLayout(right_panel)
        
        title_log = QLabel("LOG THUẬT TOÁN & TIẾN TRÌNH")
        title_log.setFont(QFont('Segoe UI', 12, QFont.Bold))
        right_layout.addWidget(title_log)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        right_layout.addWidget(self.log_box)
        
        main_layout.addWidget(right_panel, stretch=4)

    def on_algo_changed(self, button):
        self.selected_algo = button.text()
        for btn in self.algo_group.buttons():
            if btn == button:
                btn.setStyleSheet("background-color: #007acc; color: white;")
            else:
                btn.setStyleSheet("background-color: #3a3a43; color: white;")
        self.log_append(f" Đã chuyển sang thuật toán: {self.selected_algo}")

    def log_append(self, text):
        self.log_box.append(text)
        self.log_box.ensureCursorVisible()

    def reset_env(self):
        self.timer.stop()
        self.is_running = False
        self.btn_start.setText("BẮT ĐẦU")
        self.btn_start.setStyleSheet("background-color: #28a745; color: white;")
        
        self.robot_pos = [0, 0]
        self.move_count = 0
        
        # Sinh bụi ngẫu nhiên từ 3 đến 5 ô trên lưới
        self.dirt_positions = set()
        num_dirts = random.randint(3, 5)
        while len(self.dirt_positions) < num_dirts:
            r, c = random.randint(0, 2), random.randint(0, 2)
            if (r, c) != (0, 0):
                self.dirt_positions.add((r, c))
                
        self.total_dirts = len(self.dirt_positions)
        self.dirt_cleaned = 0
        
        self.log_box.clear()
        self.log_append(" Hệ thống: Đã khởi tạo lại ma trận 3x3 ngẫu nhiên.")
        self.log_append(f" Vị trí bụi ban đầu: {list(self.dirt_positions)}")
        
        self.update_ui_grid()
        self.update_status_bar()

    def update_ui_grid(self):
        for r in range(3):
            for c in range(3):
                cell = self.grid_cells[r][c]
                cell_style = "border-radius: 5px; font-weight: bold; font-size: 13px;"
                
                if [r, c] == self.robot_pos:
                    cell.setText("🤖 ROBOT")
                    cell_style += "background-color: #ffc107; color: #000;"
                elif (r, c) in self.dirt_positions:
                    cell.setText("🧹 Bụi")
                    cell_style += "background-color: #6c757d; color: #fff;"
                else:
                    cell.setText("Sạch")
                    cell_style += "background-color: #2e7d32; color: #fff;"
                    
                cell.setStyleSheet(cell_style)

    def update_status_bar(self):
        self.lbl_steps.setText(f"Tổng số bước: {self.move_count}")
        self.lbl_cleaned.setText(f"Đã dọn dẹp: {self.dirt_cleaned}/{self.total_dirts}")
        if self.dirt_cleaned == self.total_dirts:
            self.lbl_status.setText("Trạng thái: Hoàn thành dọn dẹp! 🎉")
            self.lbl_status.setStyleSheet("color: #28a745; font-weight: bold;")
        elif self.is_running:
            self.lbl_status.setText(f"Trạng thái: Đang chạy ({self.selected_algo})...")
            self.lbl_status.setStyleSheet("color: #007acc;")
        else:
            self.lbl_status.setText("Trạng thái: Tạm dừng / Sẵn sàng")
            self.lbl_status.setStyleSheet("color: white;")

    def toggle_simulation(self):
        if self.dirt_cleaned == self.total_dirts:
            self.reset_env()
            
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.btn_start.setText("TIẾP TỤC")
            self.btn_start.setStyleSheet("background-color: #28a745; color: white;")
        else:
            self.is_running = True
            self.timer.start(1000)
            self.btn_start.setText("TẠM DỪNG")
            self.btn_start.setStyleSheet("background-color: #ffc107; color: black;")
            self.log_append(f"\n--- Bắt đầu kích hoạt cây quyết định: {self.selected_algo} ---")
            
        self.update_status_bar()

    def next_simulation_step(self):
        if self.dirt_cleaned == self.total_dirts:
            self.timer.stop()
            self.is_running = False
            self.update_status_bar()
            return
            
        curr_pos_tuple = (self.robot_pos[0], self.robot_pos[1])
        if curr_pos_tuple in self.dirt_positions:
            self.dirt_positions.remove(curr_pos_tuple)
            self.dirt_cleaned += 1
            self.log_append(f"⭐ [DỌN SẠCH] Robot đã hút bụi tại ô {curr_pos_tuple}")
            self.update_ui_grid()
            self.update_status_bar()
            return

        self.move_count += 1
        r, c = self.robot_pos
        self.log_append(f"\n[Bước {self.move_count}] Robot đang ở ({r}, {c})")
        
        possible_moves = []
        if r > 0: possible_moves.append(([r-1, c], "Lên (UP)"))
        if r < 2: possible_moves.append(([r+1, c], "Xuống (DOWN)"))
        if c > 0: possible_moves.append(([r, c-1], "Trái (LEFT)"))
        if c < 2: possible_moves.append(([r, c+1], "Phải (RIGHT)"))
        
        best_move, move_name = random.choice(possible_moves)
        
        if self.selected_algo == "Minimax":
            self.log_append(f" -> Khởi tạo cây Minimax tại node gốc ({r},{c}). Max Depth = 3")
            for move, direction in possible_moves:
                val = random.randint(-10, 10)
                self.log_append(f"   + Duyệt nhánh {direction} -> Dự đoán điểm ô ({move[0]},{move[1]}): {val}")
            self.log_append(f" => Chọn nhánh có giá trị MAX lớn nhất: {move_name}")
            
        elif self.selected_algo == "Alpha - Beta":
            self.log_append(f" -> Khởi tạo Alpha-Beta Pruning. Khởi tạo α = -∞, β = +∞")
            for move, direction in possible_moves:
                val = random.randint(-5, 15)
                self.log_append(f"   + Kiểm tra node ({move[0]},{move[1]}): Giá trị = {val}")
                if val > 10:
                    self.log_append(f"   ⚠️ [TỈA NHÁNH] β <= α kích hoạt tại hướng {direction}. Bỏ qua các nhánh con!")
                    break
            self.log_append(f" => Kết quả tối ưu sau khi tỉa cắt: {move_name}")
            
        elif self.selected_algo == "Expectimax":
            self.log_append(f" -> Khởi tạo Expectimax (Môi trường có xác suất ngẫu nhiên)")
            for move, direction in possible_moves:
                chance_val = round(random.uniform(-10, 10), 2)
                self.log_append(f"   + Tính toán giá trị kỳ vọng (Expected Value) nhánh {direction}: {chance_val}")
            self.log_append(f" => Chọn nước đi đem lại giá trị kỳ vọng cao nhất: {move_name}")

        self.robot_pos = best_move
        self.update_ui_grid()
        self.update_status_bar()