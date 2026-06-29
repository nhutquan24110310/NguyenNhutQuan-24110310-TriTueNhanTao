# algorithms/local/simulated_annealing.py
import time
import random
import math
from algorithms.local.base_local import BaseLocalSearch

class SimulatedAnnealingSearch(BaseLocalSearch):
    def search(self):
        start_time = time.perf_counter()
        nodes_expanded = 0
        logs = ["Khởi chạy Simulated Annealing (Tôi luyện thép)..."]
        
        current_state = self.initial_state
        path = [current_state]
        
        # Cấu hình các tham số nhiệt động lực học ban đầu
        T = 100.0
        cooling_rate = 0.95
        min_T = 0.001
        max_iterations = 1000
        iteration = 0
        
        while T > min_T and iteration < max_iterations:
            iteration += 1
            
            if current_state.is_goal():
                end_time = time.perf_counter()
                logs.append("➔ [Thành công] Tìm thấy trạng thái đích hoàn hảo bằng Simulated Annealing!")
                return path, logs, {"steps": len(path)-1, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
            successors = current_state.get_successors()
            if not successors:
                break
                
            nodes_expanded += 1
            # Thuật toán chọn ngẫu nhiên một trạng thái lân cận (không bắt buộc phải tốt hơn)
            next_state = random.choice(successors)
            
            current_value = self.get_value(current_state)
            next_value = self.get_value(next_state)
            
            # Tính độ chênh lệch chất lượng trạng thái
            delta_e = next_value - current_value
            
            if delta_e > 0:
                # Nếu trạng thái mới tốt hơn, chấp nhận ngay lập tức
                current_state = next_state
                path.append(current_state)
            else:
                # Nếu xấu hơn, tính xác suất chấp nhận dựa trên nhiệt độ T hiện tại
                probability = math.exp(delta_e / T)
                if random.random() < probability:
                    current_state = next_state
                    path.append(current_state)
                    logs.append(f"Bước {iteration}: Chấp nhận trạng thái xấu hơn với P = {probability:.4f} (T = {T:.2f})")
            
            # Hạ nhiệt dần theo thời gian
            T *= cooling_rate
            
        # Kiểm tra điều kiện dừng an toàn cuối cùng
        if current_state.is_goal():
            end_time = time.perf_counter()
            return path, logs, {"steps": len(path)-1, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
        end_time = time.perf_counter()
        logs.append("⚠️ Hệ thống đã nguội (Cool Down) hoàn toàn nhưng bị kẹt tại chỗ.")
        return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}