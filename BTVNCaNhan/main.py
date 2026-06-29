# main.py
import sys
import time
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# Import các thành phần từ cấu trúc thư mục modular đã xây dựng
from models.environment import VacuumEnvironment
from models.state import VacuumState
from ui.main_window import MainWindow

class AppController:
    def __init__(self):
        # 1. Khởi tạo lõi dữ liệu bài toán (Model)
        self.env = VacuumEnvironment()
        
        # 2. Khởi tạo giao diện đồ họa (UI) và nạp môi trường vào
        self.window = MainWindow(self.env)
        
        # 3. Kết nối nút bấm trên UI với hàm xử lý của Controller
        self.window.btn_run.clicked.connect(self.start_ai_simulation)
        
        # 4. Quản lý bộ đếm thời gian (Timer) phục vụ việc chạy mô phỏng từng bước
        self.sim_timer = QTimer()
        self.sim_timer.timeout.connect(self.execute_next_simulation_step)
        
        self.simulation_path = []  # Chứa chuỗi các State kết quả của AI
        self.current_step_idx = 0   # Chỉ số bước đang mô phỏng

    def start_ai_simulation(self):
        """Hàm kích hoạt khi người dùng bấm nút 'KÍCH HOẠT ROBOT'"""
        algo_name = self.window.selected_algo
        
        if not algo_name:
            self.window.logger.clear_log()
            self.window.logger.append_log("LỖI: Vui lòng chọn một thuật toán cụ thể ở danh mục bên trái!")
            return
        
        # Tạm dừng bộ mô phỏng cũ nếu đang chạy dở
        self.sim_timer.stop()
        
        self.window.logger.clear_log()
        self.window.logger.append_log(f"Khởi tạo tìm kiếm không gian với thuật toán: {algo_name}...")
        
        # Tạo trạng thái AI ban đầu (Snapshot) dựa trên vị trí robot và bụi thực tế trên map
        initial_state = VacuumState(robot_pos=self.env.robot_pos, grid=self.env.grid)
        
        # Gọi bộ điều phối trung tâm để lấy kết quả thuật toán
        path, logs, stats = self.get_algorithm_result(algo_name, initial_state)
        
        # Hiển thị toàn bộ tiến trình duyệt node của thuật toán lên bảng Log bên phải
        for log_msg in logs:
            self.window.logger.append_log(log_msg)
            
        # Cập nhật các thông số đo đạc hiệu năng xuống bảng kết quả bên dưới
        self.window.result_panel.update_results(
            algo_name=algo_name,
            steps=stats["steps"],
            nodes=stats["nodes"],
            exec_time=stats["time_ms"]
        )
        
        # Nạp lộ trình tìm được vào bộ điều khiển mô phỏng trực quan
        self.simulation_path = path
        self.current_step_idx = 0
        
        # Bật Timer: Cứ mỗi 600ms (0.6 giây) robot sẽ di chuyển hoặc hút bụi 1 lần trên màn hình
        self.sim_timer.start(600)

    def get_algorithm_result(self, algo_name, initial_state):
        """
        NHÀ MÁY ĐIỀU HƯỚNG CHUẨN HÓA - KHỚP 100% VỚI DANH MỤC TRÊN ẢNH
        """
        # Chuẩn hóa chuỗi văn bản nhận về từ UI để so sánh chính xác
        algo_upper = algo_name.upper().strip()
        
        # Tự động trích xuất Heuristic dựa trên lựa chọn cụ thể ở cây danh mục
        h_type = "manhattan" if "MANHATTAN" in algo_upper else "dirty"

        # =========================================================================
        # NHÓM 1: UNINFORMED SEARCH (TÌM KIẾM MÙ)
        # =========================================================================
        if "BFS" in algo_upper:
            from algorithms.uninformed.bfs import BFS
            return BFS(initial_state).search()
            
        elif "DFS" in algo_upper:
            from algorithms.uninformed.dfs import DFS
            return DFS(initial_state).search()
            
        elif "IDS" in algo_upper:
            from algorithms.uninformed.ids import IDS
            return IDS(initial_state).search()
            
        elif "UCS" in algo_upper:
            from algorithms.uninformed.ucs import UCS
            # Phân tách 2 kiểu chi phí dựa theo lựa chọn trên giao diện
            cost = "dirty" if "RÁC" in algo_upper else "step"
            return UCS(initial_state, cost_type=cost).search()

        # =========================================================================
        # NHÓM 2: INFORMED SEARCH (TÌM KIẾM CÓ THÔNG TIN)
        # =========================================================================
        elif "IDA*" in algo_upper:
            from algorithms.informed.idastar import IDAStarSearch
            return IDAStarSearch(initial_state, heuristic_type=h_type).search()

        elif "A*" in algo_upper:
            from algorithms.informed.astar import AStarSearch
            return AStarSearch(initial_state, heuristic_type=h_type).search()

        elif "GREEDY" in algo_upper:
            from algorithms.informed.greedy import GreedySearch
            return GreedySearch(initial_state, heuristic_type=h_type).search()

        # =========================================================================
        # NHÓM 3: LOCAL SEARCH (TÌM KIẾM CỤC BỘ) - ĐÚNG 4 THUẬT TOÁN TRÊN ẢNH
        # =========================================================================
        elif "STOCHASTIC" in algo_upper:
            from algorithms.local.stochastic_hill_climbing import StochasticHillClimbingSearch
            return StochasticHillClimbingSearch(initial_state, heuristic_type=h_type).search()

        elif "BEAM" in algo_upper:
            from algorithms.local.local_beam_search import LocalBeamSearch
            return LocalBeamSearch(initial_state, heuristic_type=h_type, k=3).search()

        elif "ANNEALING" in algo_upper or "SIMULATED" in algo_upper:
            from algorithms.local.simulated_annealing import SimulatedAnnealingSearch
            return SimulatedAnnealingSearch(initial_state, heuristic_type=h_type).search()

        elif "SIMPLE" in algo_upper or "HILL" in algo_upper:
            from algorithms.local.simple_hill_climbing import SimpleHillClimbingSearch
            return SimpleHillClimbingSearch(initial_state, heuristic_type=h_type).search()

# =========================================================================
        # NHÓM 3: LOCAL SEARCH (TÌM KIẾM CỤC BỘ)
        # =========================================================================
        elif "STOCHASTIC" in algo_upper:
            from algorithms.local.stochastic_hill_climbing import StochasticHillClimbingSearch
            return StochasticHillClimbingSearch(initial_state, heuristic_type=h_type).search()

        elif "BEAM" in algo_upper:
            from algorithms.local.local_beam_search import LocalBeamSearch
            return LocalBeamSearch(initial_state, heuristic_type=h_type, k=3).search()

        elif "ANNEALING" in algo_upper or "SIMULATED" in algo_upper:
            from algorithms.local.simulated_annealing import SimulatedAnnealingSearch
            return SimulatedAnnealingSearch(initial_state, heuristic_type=h_type).search()

        elif "SIMPLE" in algo_upper or "HILL" in algo_upper:
            from algorithms.local.simple_hill_climbing import SimpleHillClimbingSearch
            return SimpleHillClimbingSearch(initial_state, heuristic_type=h_type).search()

   # =========================================================================
        # NHÓM 3: LOCAL SEARCH (TÌM KIẾM CỤC BỘ)
        # =========================================================================
        elif "STOCHASTIC" in algo_upper:
            from algorithms.local.stochastic_hill_climbing import StochasticHillClimbingSearch
            return StochasticHillClimbingSearch(initial_state, heuristic_type=h_type).search()
        elif "BEAM" in algo_upper:
            from algorithms.local.local_beam_search import LocalBeamSearch
            return LocalBeamSearch(initial_state, heuristic_type=h_type, k=3).search()
        elif "ANNEALING" in algo_upper or "SIMULATED" in algo_upper:
            from algorithms.local.simulated_annealing import SimulatedAnnealingSearch
            return SimulatedAnnealingSearch(initial_state, heuristic_type=h_type).search()
        elif "SIMPLE" in algo_upper or "HILL" in algo_upper:
            from algorithms.local.simple_hill_climbing import SimpleHillClimbingSearch
            return SimpleHillClimbingSearch(initial_state, heuristic_type=h_type).search()

        # =========================================================================
        # NHÓM 4: BELIEF STATE SEARCH (MÔI TRƯỜNG THIẾU THÔNG TIN) <--- CHÈN VÀO ĐÂY
        # =========================================================================
        elif "KHÔNG NHÌN THẤY" in algo_upper or "SENSORLESS" in algo_upper:
            from algorithms.belief.sensorless_bfs import SensorlessBFSSearch
            return SensorlessBFSSearch(initial_state).search()
            
        elif "THẤY 1 PHẦN" in algo_upper or "PARTIALLY" in algo_upper:
            from algorithms.belief.partially_observable import PartiallyObservableBFSSearch
            return PartiallyObservableBFSSearch(initial_state).search()

        # =========================================================================
        # TRƯỜNG HỢP DỰ PHÒNG AN TOÀN
        # =========================================================================
        else:
            mock_logs = [
                f"⚠️ Hệ thống không nhận diện được tên thuật toán: '{algo_name}'",
                "Đang trả về trạng thái rỗng để bảo vệ an toàn cho giao diện ứng dụng."
            ]
            return [], mock_logs, {"steps": 0, "nodes": 0, "time_ms": 0}
        
    def execute_next_simulation_step(self):
        """Hàm chạy lặp lại liên tục theo chu kỳ của Timer để cập nhật UI theo từng bước"""
        if self.current_step_idx < len(self.simulation_path):
            # Lấy trạng thái tại bước hiện tại ra
            state = self.simulation_path[self.current_step_idx]
            
            # Đồng bộ hóa dữ liệu môi trường thực tế chạy trên máy trùng khớp với State của AI
            self.env.robot_pos = state.robot_pos
            self.env.grid = list(state.grid)
            
            # Ra lệnh cho UI vẽ lại toàn bộ lưới dựa trên dữ liệu mới cập nhật
            self.window.sync_model_to_ui()
            
            self.window.logger.append_log(
                f"Mô phỏng bước {self.current_step_idx}: Robot dịch chuyển đến ô [{state.robot_pos // 3}, {state.robot_pos % 3}]"
            )
            self.current_step_idx += 1
        else:
            # Đã đi hết chuỗi kết quả, dừng Timer lại
            self.sim_timer.stop()
            self.window.logger.append_log("✨ HÀNH TRÌNH MÔ PHỎNG KẾT THÚC THÀNH CÔNG! ✨")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.window.show()
    sys.exit(app.exec_())