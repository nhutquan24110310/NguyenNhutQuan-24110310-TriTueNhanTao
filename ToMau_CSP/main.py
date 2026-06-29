import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter, QListWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from core.csp_engine import CSPSolver
from core.map_generator import MapGenerator
from gui.map_widget import MapWidget
from gui.log_widget import LogWidget
from gui.tree_widget import TreeWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI CSP Solver - Đa thuật toán Tô màu Bản đồ Đồng Tháp")
        self.resize(1400, 850)
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # --- GIAO DIỆN CHÍNH LAYOUT ---
        container = QWidget()
        self.setCentralWidget(container)
        root_layout = QHBoxLayout(container)

        # --- TẠO MENU CHỌN THUẬT TOÁN BÊN TRÁI ---
        left_panel = QWidget()
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("background-color: #282a36; border-right: 1px solid #44475a;")
        left_vbox = QVBoxLayout(left_panel)
        
        lbl_menu = QLabel("NHÓM THUẬT TOÁN AI")
        lbl_menu.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl_menu.setStyleSheet("color: #ff79c6; padding: 5px;")
        left_vbox.addWidget(lbl_menu)
        
        self.algo_selector = QListWidget()
        self.algo_selector.setStyleSheet("""
            QListWidget { background-color: #282a36; border: none; color: #f8f8f2; font-size: 13px; }
            QListWidget::item { padding: 12px; border-bottom: 1px solid #44475a; }
            QListWidget::item:selected { background-color: #bd93f9; color: black; font-weight: bold; border-radius: 4px; }
        """)
        self.algo_selector.addItems([
            "1. Backtracking Search",
            "2. Arc Consistency (AC-3)",
            "3. Local Search (Min-Conflicts)"
        ])
        self.algo_selector.setCurrentRow(0) # Mặc định chọn Backtracking
        left_vbox.addWidget(self.algo_selector)
        root_layout.addWidget(left_panel)

        # --- KHU VỰC HIỂN THỊ CHÍNH (BÊN PHẢI) ---
        right_main_widget = QWidget()
        right_layout = QVBoxLayout(right_main_widget)
        
        self.map_widget = MapWidget()
        self.log_widget = LogWidget()
        self.tree_widget = TreeWidget()

        splitter_horizontal = QSplitter(Qt.Horizontal)
        splitter_horizontal.addWidget(self.map_widget)
        splitter_horizontal.addWidget(self.log_widget)
        splitter_horizontal.setSizes([700, 450])
        
        splitter_vertical = QSplitter(Qt.Vertical)
        splitter_vertical.addWidget(splitter_horizontal)
        splitter_vertical.addWidget(self.tree_widget)
        splitter_vertical.setSizes([550, 250])
        
        right_layout.addWidget(splitter_vertical)

        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("KÍCH HOẠT ROBOT GIẢI THUẬT")
        self.start_btn.setStyleSheet("background-color: #50fa7b; color: black; padding: 12px; font-weight: bold; border-radius: 6px; font-size: 13px;")
        btn_layout.addWidget(self.start_btn)
        right_layout.addLayout(btn_layout)
        
        root_layout.addWidget(right_main_widget)

        # --- SỰ KIỆN ---
        self.start_btn.clicked.connect(self.start_solving)
        self.algo_selector.currentRowChanged.connect(self.load_dong_thap_map)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        
        self.solver_generator = None
        self.load_dong_thap_map()

    def load_dong_thap_map(self):
        self.variables, self.domains, self.constraints, self.positions = MapGenerator.get_dong_thap_map()
        self.reset_ui()

    def reset_ui(self):
        self.timer.stop()
        self.map_widget.init_map(self.variables, self.positions, self.constraints)
        self.log_widget.clear()
        self.tree_widget.clear_tree()
        self.start_btn.setEnabled(True)
        
        vars_str = ", ".join(self.variables)
        domains_str = "\n".join([f"    • {k}: {', '.join(v)}" for k, v in self.domains.items()])
        constraints_str = "\n".join([f"    • {k} giáp với: {', '.join(v)}" for k, v in self.constraints.items()])
        
        self.log_widget.add_log(f"=== BÀI TOÁN TÔ MÀU BẢN ĐỒ ĐỒNG THÁP ===")
        self.log_widget.add_log(f"📌 Các Vùng Đất (Variables):\n    [ {vars_str} ]\n")
        self.log_widget.add_log(f"🎨 Miền Màu Sắc (Domains):\n{domains_str}\n")
        self.log_widget.add_log(f"🔗 Biên Giới Giáp Ranh (Constraints):\n{constraints_str}")
        self.log_widget.add_log("========================================\nChọn thuật toán ở cột trái và nhấn nút Kích Hoạt!")

    def start_solving(self):
        algo_idx = self.algo_selector.currentRow()
        solver = CSPSolver(self.variables, self.domains, self.constraints)
        
        if algo_idx == 0:
            self.log_widget.add_log("\n>>> CHẠY THUẬT TOÁN: BACKTRACKING SEARCH...")
            self.solver_generator = solver.backtrack()
        elif algo_idx == 1:
            self.log_widget.add_log("\n>>> CHẠY THUẬT TOÁN: ARC CONSISTENCY (AC-3) + BACKTRACKING...")
            self.solver_generator = solver.ac3_and_search()
        elif algo_idx == 2:
            self.log_widget.add_log("\n>>> CHẠY THUẬT TOÁN: LOCAL SEARCH (MIN-CONFLICTS)...")
            self.solver_generator = solver.min_conflicts()

        self.start_btn.setEnabled(False)
        self.timer.start(350) # Tốc độ chạy mô phỏng ngắt nhịp (350ms)

    def next_step(self):
        try:
            assignment, status, detail = next(self.solver_generator)
            
            # Đồng bộ màu sắc bản đồ dựa theo trạng thái gán hiện tại
            if status in ["MC_INIT", "MC_STEP"]:
                self.map_widget.update_all_colors(assignment)
            
            # --- XỬ LÝ CHUNG CHO TRẠNG THÁI SUCCESS / KẾT THÚC ---
            if status == "SUCCESS":
                self.map_widget.update_all_colors(assignment)
                self.log_widget.add_log("\n🎉 HOÀN THÀNH: ĐÃ TÌM ĐƯỢC PHƯƠNG ÁN TÔ MÀU HỢP LỆ THỎA MÃN!")
                self.tree_widget.add_node("", "", is_success=True)
                self.timer.stop()
                self.start_btn.setEnabled(True)
                return

            # --- TRẠNG THÁI THUẬT TOÁN 1: BACKTRACKING ---
            if status == "ASSIGN":
                var, value = detail
                self.map_widget.update_color(var, value)
                self.log_widget.add_log(f"🟢 Thử gán: {var} = {value}")
                self.tree_widget.add_node(var, value)
                self.tree_widget.increase_depth()
            elif status == "FAIL":
                var, value = detail
                self.log_widget.add_log(f"🟡 Xung đột: {var} = {value}")
                self.tree_widget.add_node(var, value, is_fail=True)
            elif status == "BACKTRACK":
                var, value = detail
                self.map_widget.update_color(var, "Xóa")
                self.log_widget.add_log(f"🔴 Quay lui tại: {var}")
                self.tree_widget.decrease_depth()

            # --- TRẠNG THÁI THUẬT TOÁN 2: AC-3 ---
            elif status == "AC3_START":
                self.log_widget.add_log("⚙️ Đang thực hiện kiểm tra cung nhất quán AC-3...")
                self.tree_widget.add_generic_log("[AC-3] Bắt đầu duyệt hàng đợi cung...")
            elif status == "AC3_PRUNE":
                u, v, removed, remain = detail
                self.log_widget.add_log(f"✂️ AC-3 tỉa màu {removed} khỏi miền của {u} do không nhất quán với {v}")
                self.tree_widget.add_generic_log(f" └─ Tỉa {u}: Loại {removed} -> Còn {remain}")
            elif status == "AC3_DONE":
                self.log_widget.add_log("✅ AC-3 hoàn tất sàng lọc! Tiến hành tìm kiếm lời giải dựa trên miền giá trị thu gọn.")
                self.tree_widget.add_generic_log("\n[AC-3 CHÀO CỜ] Chuyển tiếp sang tìm kiếm nhánh:")
            elif status == "AC3_FAILED":
                self.log_widget.add_log(f"❌ Khủng hoảng! Vùng {detail} bị triệt tiêu hết mọi màu khả thi. AC-3 thất bại.")
                self.timer.stop()
                self.start_btn.setEnabled(True)

            # --- TRẠNG THÁI THUẬT TOÁN 3: MIN-CONFLICTS ---
            elif status == "MC_INIT":
                self.log_widget.add_log("🎲 [Khởi tạo] Phủ màu ngẫu nhiên cho toàn bộ bản đồ.")
                self.tree_widget.add_generic_log("🔄 Khởi tạo trạng thái ban đầu...")
            elif status == "MC_STEP":
                step, var, best_val, num_conflicts = detail
                self.log_widget.add_log(f"Step {step}: Sửa vùng {var} thành màu [{best_val}] để hạ xung đột.")
                self.tree_widget.add_generic_log(f"Bước {step} -> Sửa {var}={best_val} | Số vùng còn xung đột: {num_conflicts}")
            elif status == "MC_FAILED":
                self.log_widget.add_log("❌ Đạt giới hạn Max Steps nhưng Min-Conflicts chưa hội tụ được lời giải!")
                self.timer.stop()
                self.start_btn.setEnabled(True)

        except StopIteration:
            self.log_widget.add_log("\n❌ KẾT THÚC: KHÔNG TÌM THẤY GIẢI PHÁP HỢP LỆ!")
            self.timer.stop()
            self.start_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())