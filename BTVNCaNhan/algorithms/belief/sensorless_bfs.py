# algorithms/belief/sensorless_bfs.py
import time
import copy
from collections import deque
from algorithms.base_search import BaseSearch

class SensorlessBFSSearch(BaseSearch):
    def __init__(self, initial_state):
        super().__init__(initial_state)
        self.actions = ["SUCK", "UP", "DOWN", "LEFT", "RIGHT"]

    def _normalize(self, state):
        pos = state.robot_pos
        grid = state.grid
        if isinstance(pos, (list, tuple)):
            pos = pos[0] * 3 + pos[1]
        if len(grid) > 0 and isinstance(grid[0], list):
            grid = [val for row in grid for val in row]
        return pos, tuple(grid)

    def _apply_action(self, pos, grid, action):
        r, c = pos // 3, pos % 3
        new_grid, new_pos = list(grid), pos
        if action == "SUCK":
            new_grid[pos] = 0
        elif action == "UP" and r > 0:
            new_pos -= 3
        elif action == "DOWN" and r < 2:
            new_pos += 3
        elif action == "LEFT" and c > 0:
            new_pos -= 1
        elif action == "RIGHT" and c < 2:
            new_pos += 1
        return (new_pos, tuple(new_grid))

    def _convert_to_vacuum_state(self, base_state, current_flat_pos, current_flat_grid):
        new_state = copy.deepcopy(base_state)
        if isinstance(base_state.robot_pos, (list, tuple)):
            new_state.robot_pos = (current_flat_pos // 3, current_flat_pos % 3)
        else:
            new_state.robot_pos = current_flat_pos
            
        if len(base_state.grid) > 0 and isinstance(base_state.grid[0], list):
            new_state.grid = [
                [current_flat_grid[0], current_flat_grid[1], current_flat_grid[2]],
                [current_flat_grid[3], current_flat_grid[4], current_flat_grid[5]],
                [current_flat_grid[6], current_flat_grid[7], current_flat_grid[8]]
            ]
        else:
            new_state.grid = list(current_flat_grid)
        return new_state

    def search(self):
        start_time = time.perf_counter()
        logs = ["🧠 [TƯ DUY AI] KHỞI CHẠY BFS KHÔNG NHÌN THẤY (MÙ HOÀN TOÀN)"]
        
        true_pos, true_grid = self._normalize(self.initial_state)
        
        # Khởi tạo tập hợp niềm tin ban đầu chứa 2 kịch bản (Thực tế vs Tồi tệ nhất) để minh họa sự nghi ngờ
        worst_grid = [1] * 9
        worst_grid[true_pos] = true_grid[true_pos]
        initial_belief = frozenset([(true_pos, true_grid), (true_pos, tuple(worst_grid))])
        
        frontier = deque([(initial_belief, [])])
        explored = {initial_belief}
        nodes_expanded = 0
        plan = []
        
        while frontier:
            curr_belief, action_path = frontier.popleft()
            nodes_expanded += 1
            
            if all(sum(g) == 0 for p, g in curr_belief):
                plan = action_path
                break
                
            if nodes_expanded > 5000:
                logs.append("⚠️ Không gian niềm tin quá lớn. Dừng thuật toán.")
                break
                
            for action in self.actions:
                next_belief = frozenset(self._apply_action(p, g, action) for p, g in curr_belief)
                if next_belief not in explored:
                    explored.add(next_belief)
                    frontier.append((next_belief, action_path + [action]))
                    
        if not plan:
            logs.append("❌ Không tìm thấy chuỗi hành động mù bao vây.")
            return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (time.perf_counter() - start_time) * 1000}
            
        logs.append(f"➔ Đã tính toán xong chuỗi hành động mù tối ưu: {' ➔ '.join(plan)}")
        logs.append("-" * 50)
        logs.append("🤖 [MÔ PHỎNG THỰC THI] ROBOT BẮT ĐẦU DI CHUYỂN MÙ:")
        
        # Khởi tạo lại để chạy thực tế và in LOG song song
        path = [self.initial_state]
        curr_pos, curr_grid = true_pos, true_grid
        curr_vac_state = self.initial_state
        
        # Giả lập lại luồng biến đổi niềm tin thực tế để in ra màn hình
        running_belief = initial_belief
        
        for idx, act in enumerate(plan, 1):
            # 1. Cập nhật thực tế thế giới vật lý
            curr_pos, curr_grid = self._apply_action(curr_pos, curr_grid, act)
            curr_vac_state = self._convert_to_vacuum_state(curr_vac_state, curr_pos, curr_grid)
            path.append(curr_vac_state)
            
            # 2. Cập nhật niềm tin trong "não bộ" robot
            running_belief = frozenset(self._apply_action(p, g, act) for p, g in running_belief)
            
            # 3. Ghi log song song cả hành động vật lý và suy nghĩ niềm tin
            logs.append(f" Bước {idx}: Robot thực hiện hành động ➔ [{act}]")
            logs.append(f"       🧠 [Bộ nhớ niềm tin]: Còn {len(running_belief)} khả năng trạng thái có thể xảy ra.")
            
        end_time = time.perf_counter()
        logs.append("➔ [Thành công] Toàn bộ lưới chắc chắn đã sạch rác!")
        return path, logs, {"steps": len(path) - 1, "nodes": nodes_expanded, "time_ms": (end_time - start_time) * 1000}