# algorithms/belief/partially_observable.py
import time
import copy
from algorithms.belief.sensorless_bfs import SensorlessBFSSearch

class PartiallyObservableBFSSearch(SensorlessBFSSearch):
    def __init__(self, initial_state):
        super().__init__(initial_state)
        self.nodes_expanded = 0

    def _or_search(self, belief, path_history):
        self.nodes_expanded += 1
        if self.nodes_expanded > 5000: return None
        if all(sum(g) == 0 for p, g in belief): return []
        if belief in path_history: return None
            
        for action in self.actions:
            plan = self._and_search(action, belief, path_history + [belief])
            if plan is not None: return [action, plan]
        return None

    def _and_search(self, action, belief, path_history):
        predicted = frozenset(self._apply_action(p, g, action) for p, g in belief)
        percept_groups = {}
        for p, g in predicted:
            percept = (p, g[p])
            if percept not in percept_groups: percept_groups[percept] = set()
            percept_groups[percept].add((p, g))
            
        conditional_plan = {}
        for percept, next_states in percept_groups.items():
            results = self._or_search(frozenset(next_states), path_history)
            if results is None: return None
            conditional_plan[percept] = results
        return conditional_plan

    def search(self):
        start_time = time.perf_counter()
        logs = ["🧠 [TƯ DUY AI] KHỞI CHẠY AND-OR SEARCH (NHÌN THẤY 1 PHẦN)"]
        
        true_pos, true_grid = self._normalize(self.initial_state)
        worst_grid = [1] * 9
        worst_grid[true_pos] = true_grid[true_pos]
        initial_belief = frozenset([(true_pos, true_grid), (true_pos, tuple(worst_grid))])
        
        self.nodes_expanded = 0
        conditional_plan = self._or_search(initial_belief, [])
        
        if conditional_plan is None:
            logs.append("❌ Không tìm thấy cây quyết định an toàn.")
            return [], logs, {"steps": 0, "nodes": self.nodes_expanded, "time_ms": (time.perf_counter() - start_time) * 1000}
            
        logs.append("➔ Đã dựng xong Cây quyết định thông minh dựa trên cảm biến.")
        logs.append("-" * 50)
        logs.append("🤖 [MÔ PHỎNG THỰC THI] ROBOT VỪA ĐI VỪA BẬT CẢM BIẾN CỤC BỘ:")
        
        path = [self.initial_state]
        curr_pos, curr_grid = true_pos, true_grid
        curr_vac_state = self.initial_state
        curr_node = conditional_plan
        step_count = 0
        
        while curr_node:
            step_count += 1
            action, branches = curr_node[0], curr_node[1]
            
            # 1. Robot di chuyển trong thực tế
            curr_pos, curr_grid = self._apply_action(curr_pos, curr_grid, action)
            curr_vac_state = self._convert_to_vacuum_state(curr_vac_state, curr_pos, curr_grid)
            path.append(curr_vac_state)
            
            logs.append(f" Bước {step_count}: Robot hành động ➔ [{action}]")
            
            if sum(curr_grid) == 0:
                logs.append("       🎉 [Thành công] Cảm biến báo môi trường thực tế đã sạch hoàn toàn!")
                break
                
            # 2. Đọc cảm biến thật (Chỉ thấy ô đang đứng)
            actual_percept = (curr_pos, curr_grid[curr_pos])
            status_str = "BẨN ❌" if curr_grid[curr_pos] == 1 else "SẠCH "
            logs.append(f"       📡 [Cảm biến dưới chân]: Ô hiện tại đang {status_str}")
            
            # 3. Rẽ nhánh tư duy
            if actual_percept in branches:
                curr_node = branches[actual_percept]
                logs.append("       🧠 [Bộ não]: Đã lọc bỏ các giả thuyết sai, rẽ sang nhánh kế hoạch phù hợp.")
            else:
                logs.append("⚠️ Cảm biến lỗi hoặc nằm ngoài cây tính toán. Dừng.")
                break
                
        end_time = time.perf_counter()
        return path, logs, {"steps": len(path) - 1, "nodes": self.nodes_expanded, "time_ms": (end_time - start_time) * 1000}