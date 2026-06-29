# algorithms/local/stochastic_hill_climbing.py
import time
import random
from algorithms.local.base_local import BaseLocalSearch

class StochasticHillClimbingSearch(BaseLocalSearch):
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
        return -(10 * len(dirty_indices) + min_dist)

    def search(self):
        start_time = time.perf_counter()
        nodes_expanded = 0
        logs = ["Khởi chạy Stochastic Hill Climbing (Đã sửa thuật toán Heuristic trọng số)..."]
        
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
            better_neighbors = [s for s in successors if self.get_value(s) > current_value]
            
            if not better_neighbors:
                end_time = time.perf_counter()
                logs.append(f"⚠️ Tập lân cận tốt hơn rỗng. Kẹt ở Cực đại cục bộ.")
                return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
            next_state = random.choice(better_neighbors)
            current_state = next_state
            path.append(current_state)