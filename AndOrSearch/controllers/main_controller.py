# controllers/main_controller.py
import random
import time
from PyQt5.QtCore import QTimer
from models.vacuum_problem import VacuumProblem
from models.and_or_search import and_or_graph_search

class MainController:
    def __init__(self, window):
        self.window = window
        
        # Trạng thái mặc định ban đầu (Khớp với hình ảnh UI mẫu của bạn)
        self.robot_pos = (1, 1)
        self.dirty_cells = set([(0, 1), (0, 2), (1, 2), (2, 2)])
        
        # Đồng bộ giao diện ban đầu
        self.window.grid_canvas.update_grid(self.robot_pos, self.dirty_cells)
        
        # Lắng nghe sự kiện từ các nút bấm trên UI
        self.window.btn_random.clicked.connect(self.randomize_map)
        self.window.btn_start.clicked.connect(self.start_simulation)
        
        # Thiết lập Timer để chạy từng bước mô phỏng (tránh đóng băng UI)
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)
        self.timer_interval = 800  # Tốc độ di chuyển: 800ms / bước
        
        # Các biến quản lý luồng chạy thuật toán
        self.problem = None
        self.current_state = None
        self.current_plan = None
        self.step_count = 0

    def randomize_map(self):
        """Xử lý sự kiện khi bấm nút ĐỔI BẢN ĐỒ NGẪU NHIÊN"""
        self.timer.stop()
        
        # Random vị trí ngẫu nhiên cho Robot
        self.robot_pos = (random.randint(0, 2), random.randint(0, 2))
        
        # Random ngẫu nhiên số lượng ô bẩn (từ 2 đến 5 ô)
        all_cells = [(r, c) for r in range(3) for c in range(3)]
        num_dirty = random.randint(2, 5)
        self.dirty_cells = set(random.sample(all_cells, num_dirty))
        
        # Cập nhật lại màn hình đồ họa và làm sạch Nhật ký
        self.window.grid_canvas.update_grid(self.robot_pos, self.dirty_cells)
        self.window.log_panel.clear_log()
        self.window.log_panel.write_log(">> Đã khởi tạo bản đồ ngẫu nhiên mới.")
        
        # Reset các thông số ở thanh trạng thái bên dưới
        self.window.lbl_algo.setText("Thuật toán: Chưa chọn")
        self.window.lbl_steps.setText("Số bước di chuyển: 0")
        self.window.lbl_nodes.setText("Số Node đã duyệt: 0")
        self.window.lbl_time.setText("Thời gian tính toán: 0.00 ms")

    def start_simulation(self):
        """Xử lý sự kiện khi bấm nút KÍCH HOẠT ROBOT"""
        self.timer.stop()
        self.window.log_panel.clear_log()
        self.window.log_panel.write_log("⚡ Đang khởi chạy thuật toán AND-OR Graph Search...")
        
        # Khởi tạo bài toán từ cấu hình hiện tại trên giao diện
        self.problem = VacuumProblem(self.robot_pos, self.dirty_cells)
        self.current_state = self.problem.initial_state
        
        # Bắt đầu tính toán và đo thời gian thực thi thuật toán cốt lõi
        start_time = time.perf_counter()
        plan = and_or_graph_search(self.problem)
        end_time = time.perf_counter()
        
        elapsed_time_ms = (end_time - start_time) * 1000
        
        # Cập nhật thanh kết quả bên dưới
        self.window.lbl_algo.setText("Thuật toán: AND-OR Search")
        self.window.lbl_time.setText(f"Thời gian tính toán: {elapsed_time_ms:.2f} ms")
        
        if plan == "failure":
            self.window.log_panel.write_log("❌ [THẤT BẠI] Không tìm thấy kế hoạch hành động an toàn cho bản đồ này!")
            self.window.lbl_nodes.setText("Số Node đã duyệt: 0")
            return
            
        # Đếm số lượng nhánh kế hoạch (Node tình huống) đã được sinh ra
        total_nodes = self._count_contingency_nodes(plan)
        self.window.lbl_nodes.setText(f"Số Node đã duyệt: {total_nodes}")
        
        self.window.log_panel.write_log("✔️ [THÀNH CÔNG] Đã xây dựng cây kế hoạch dự phòng thành công.")
        self.window.log_panel.write_log(">> Bắt đầu thực thi mô phỏng trên lưới ô vuông...")
        
        # Lưu trữ kế hoạch tổng thể và kích hoạt Timer chuyển động
        self.current_plan = plan
        self.step_count = 0
        self.window.lbl_steps.setText(f"Số bước di chuyển: {self.step_count}")
        self.timer.start(self.timer_interval)

    def simulation_step(self):
        """Hàm vòng lặp chạy tự động sau mỗi khoảng thời gian được cấu hình"""
        # Kiểm tra điều kiện dừng nếu môi trường sạch hoàn toàn
        if self.problem.goal_test(self.current_state):
            self.window.log_panel.write_log("\n🎉 HOÀN THÀNH: Tất cả các ô đã sạch bụi. Robot dừng hoạt động.")
            self.timer.stop()
            return
            
        if self.current_plan == [] or self.current_plan == "failure":
            self.window.log_panel.write_log("\n🛑 Kết thúc chuỗi hành động hoặc kế hoạch bị gián đoạn.")
            self.timer.stop()
            return
            
        # Tách hành động hiện tại và danh sách các phương án cho trạng thái kế tiếp
        action, next_plans = self.current_plan
        
        # Lấy tất cả kết quả có thể xảy ra từ Model
        possible_results = self.problem.results(self.current_state, action)
        
        # Mô phỏng tính "không định hướng" bằng cách chọn ngẫu nhiên 1 kết quả thực tế xảy ra
        next_state = random.choice(possible_results)
        
        self.step_count += 1
        self.window.lbl_steps.setText(f"Số bước di chuyển: {self.step_count}")
        
        # Phân tích trạng thái để ghi log trực quan
        old_pos, _ = self.current_state
        new_pos, new_dirty = next_state
        
        log_msg = f"[Bước {self.step_count}] Tại {old_pos} -> Chọn [{action}]"
        if action != "SUCK" and old_pos == new_pos:
            log_msg += " ⚠️ (Bánh xe trượt! Giữ nguyên vị trí)"
        elif action == "SUCK" and len(new_dirty) == len(self.current_state[1]):
            log_msg += " ⚠️ (Hút trượt! Bụi văng sang ô kế bên)"
        else:
            log_msg += " -> Thành công."
            
        self.window.log_panel.write_log(log_msg)
        
        # Cập nhật trạng thái thực tế lên màn hình Canvas
        self.current_state = next_state
        self.window.grid_canvas.update_grid(new_pos, new_dirty)
        
        # Đi theo nhánh rẽ tương ứng của trạng thái mới trong cây kế hoạch AND-OR
        self.current_plan = next_plans.get(self.current_state, "failure")

    def _count_contingency_nodes(self, plan):
        """Hàm bổ trợ đếm tổng số nút tình huống trong cây kết quả"""
        if plan == "failure" or plan == []:
            return 1
        if isinstance(plan, list) and len(plan) == 2:
            action, next_plans = plan
            count = 1
            if isinstance(next_plans, dict):
                for s, sub_plan in next_plans.items():
                    count += self._count_contingency_nodes(sub_plan)
            return count
        return 1