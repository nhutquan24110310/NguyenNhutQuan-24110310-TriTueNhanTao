# algorithms/uninformed/ucs.py
import heapq
import time
from algorithms.base_search import BaseSearch

class UCS(BaseSearch):
    def __init__(self, initial_state, cost_type="step"):
        super().__init__(initial_state)
        self.cost_type = cost_type  # "step" (Theo bước đi) hoặc "dirty" (Theo lượng rác)

    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0
        
        # Biến đếm counter dùng để phân tách thứ tự trong Heap khi hai nút có chi phí g(n) bằng nhau
        counter = 0 
        
        # Hàng đợi ưu tiên Priority Queue: Các phần tử lưu dạng (chi_phí_tích_lũy, số_thứ_tự, đối_tượng_state)
        frontier = []
        heapq.heappush(frontier, (0, counter, self.initial_state))
        
        reached = {self.initial_state: 0} # Lưu trữ {Trạng thái: Chi phí tối ưu nhất đến thời điểm hiện tại}

        logs.append(f"Khởi động UCS [Chế độ: {self.cost_type}] tại ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        while frontier:
            current_cost, _, current_state = heapq.heappop(frontier)

            # Nếu chi phí bốc ra lớn hơn chi phí tối ưu đã được ghi nhận trước đó -> Cắt tỉa ngay
            if current_cost > reached.get(current_state, float('inf')):
                continue

            self.nodes_expanded += 1

            if self.nodes_expanded <= 15:
                logs.append(f"[Node {self.nodes_expanded}] g(n) tích lũy = {current_cost} | Robot tại ({current_state.robot_pos // 3}, {current_state.robot_pos % 3})")

            # Đích được kiểm tra muộn khi lấy ra khỏi Priority Queue để đảm bảo tính tối ưu chi phí thấp nhất
            if current_state.is_goal():
                path = self.reconstruct_path(current_state)
                end_time = time.perf_counter()
                logs.append(f"➔ UCS thành công! Tổng chi phí tối ưu g(n) = {current_cost}")
                return path, logs, {
                    "steps": len(path) - 1,
                    "nodes": self.nodes_expanded,
                    "time_ms": (end_time - self.start_time) * 1000
                }

            for successor in current_state.get_successors():
                # --- PHÂN TÁCH ĐỊNH NGHĨA HÀM CHI PHÍ THEO THIẾT KẾ ---
                if self.cost_type == "step":
                    edge_cost = 1  # Chi phí đồng đều cho mọi hành động
                else:
                    # Theo lượng rác: Ô nhiễm càng nhiều, chi phí vận hành động cơ càng lớn
                    # Chi phí hành động = 1 + số lượng ô rác đang tồn tại trên ma trận
                    edge_cost = 1 + sum(current_state.grid)

                new_cost = current_cost + edge_cost

                if successor not in reached or new_cost < reached[successor]:
                    reached[successor] = new_cost
                    counter += 1
                    heapq.heappush(frontier, (new_cost, counter, successor))

        end_time = time.perf_counter()
        return [], ["UCS thất bại!"], {"steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000}