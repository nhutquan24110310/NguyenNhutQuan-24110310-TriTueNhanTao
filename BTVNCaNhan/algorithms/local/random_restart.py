# algorithms/local/random_restart.py
import time
import random
from algorithms.local.base_local import BaseLocalSearch

class RandomRestartHillClimbingSearch(BaseLocalSearch):
    def __init__(self, initial_state, heuristic_type="manhattan", max_restarts=5):
        super().__init__(initial_state, heuristic_type)
        self.max_restarts = max_restarts

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
        logs = [f"Khởi chạy Random Restart Hill Climbing (MAX_RESTART = {self.max_restarts})..."]
        
        for i in range(1, self.max_restarts + 1):
            logs.append(f"--- Lượt khởi động thứ {i} ---")
            current_state = self.initial_state
            path = [current_state]
            
            while True:
                if current_state.is_goal():
                    end_time = time.perf_counter()
                    logs.append(f"➔ [Thành công] Tìm thấy đích ở lượt chạy thứ {i}!")
                    return path, logs, {"steps": len(path)-1, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
                
                successors = current_state.get_successors()
                if not successors:
                    break
                    
                nodes_expanded += 1
                current_value = self.get_value(current_state)
                better_neighbors = [s for s in successors if self.get_value(s) > current_value]
                
                if not better_neighbors:
                    logs.append(f" Lượt {i} bị kẹt cực đại cục bộ.")
                    break
                else:
                    best_val = max(self.get_value(s) for s in better_neighbors)
                    best_nodes = [s for s in better_neighbors if self.get_value(s) == best_val]
                    current_state = random.choice(best_nodes)
                    path.append(current_state)
                    
        end_time = time.perf_counter()
        logs.append("❌ Thất bại sau các lượt thử khởi động lại.")
        return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}