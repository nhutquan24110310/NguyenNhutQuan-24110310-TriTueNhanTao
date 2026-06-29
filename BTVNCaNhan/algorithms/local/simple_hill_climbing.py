# algorithms/local/simple_hill_climbing.py
import time
from algorithms.local.base_local import BaseLocalSearch

class SimpleHillClimbingSearch(BaseLocalSearch):
    def get_value(self, state):
        grid = state.grid
        if len(grid) > 0 and isinstance(grid[0], list):
            flat_grid = [val for row in grid for val in row]
        else:
            flat_grid = grid

        if isinstance(state.robot_pos, int):
            r, c = state.robot_pos // 3, state.robot_pos % 3
        else:
            r, c = state.robot_pos[0], state.robot_pos[1]

        dirty_indices = [i for i, val in enumerate(flat_grid) if val == 1]
        if not dirty_indices:
            return 0

        min_dist = min(abs(r - (i // 3)) + abs(c - (i % 3)) for i in dirty_indices)
        # Sửa lỗi: Nhân 10 vào số lượng rác để hành động SUCK luôn mang lại giá trị cao hơn
        return -(10 * len(dirty_indices) + min_dist)

    def search(self):
        start_time = time.perf_counter()
        nodes_expanded = 0
        logs = ["Khởi chạy Simple Hill Climbing (Đã sửa thuật toán Heuristic trọng số)..."]
        
        current_state = self.initial_state
        path = [current_state]
        
        while True:
            if current_state.is_goal():
                end_time = time.perf_counter()
                logs.append("➔ [Thành công] Tìm thấy trạng thái đích hoàn hảo!")
                return path, logs, {"steps": len(path)-1, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
            successors = current_state.get_successors()
            if not successors:
                break
                
            nodes_expanded += 1
            current_value = self.get_value(current_state)
            next_state = None
            
            for succ in successors:
                if self.get_value(succ) > current_value:
                    next_state = succ
                    break
            
            if next_state is None:
                end_time = time.perf_counter()
                if isinstance(current_state.robot_pos, int):
                    rx, ry = current_state.robot_pos // 3, current_state.robot_pos % 3
                else:
                    rx, ry = current_state.robot_pos[0], current_state.robot_pos[1]
                logs.append(f"⚠️ Kẹt ở Cực đại cục bộ tại ô ({rx}, {ry}).")
                return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
            current_state = next_state
            path.append(current_state)