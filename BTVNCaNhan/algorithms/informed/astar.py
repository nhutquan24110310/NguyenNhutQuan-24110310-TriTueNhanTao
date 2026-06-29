# algorithms/informed/astar.py
import heapq
import time
from algorithms.base_search import BaseSearch

class AStarSearch(BaseSearch):
    def __init__(self, initial_state, heuristic_type="dirty"):
        super().__init__(initial_state)
        self.heuristic_type = heuristic_type  # "dirty" hoặc "manhattan"

    def get_heuristic(self, state):
        grid = state.grid
        r, c = state.robot_pos // 3, state.robot_pos % 3
        dirty_indices = [i for i, val in enumerate(grid) if val == 1]

        if self.heuristic_type == "dirty":
            return len(dirty_indices)
        elif self.heuristic_type == "manhattan":
            if not dirty_indices:
                return 0
            min_dist = min(abs(r - (i // 3)) + abs(c - (i % 3)) for i in dirty_indices)
            return len(dirty_indices) + min_dist
        return 0

    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0

        counter = 0
        frontier = []
        
        # Thiết lập chi phí gCost ban đầu
        g_cost = {self.initial_state: 0}
        start_h = self.get_heuristic(self.initial_state)
        
        # Hàng đợi lưu dạng: (f(n), g(n), counter, state) nhằm tối ưu sắp xếp theo f(n) trước, g(n) sau
        heapq.heappush(frontier, (start_h, 0, counter, self.initial_state))

        visited = set()
        logs.append(f"Khởi động A* [{self.heuristic_type}] tại ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        while frontier:
            current_f, current_g, _, current_state = heapq.heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            self.nodes_expanded += 1

            if self.nodes_expanded <= 15:
                logs.append(f"[Node {self.nodes_expanded}] f(n)={current_f} | g(n)={current_g} | h(n)={current_f - current_g}")

            # Đạt mục tiêu dọn sạch sàn
            if current_state.is_goal():
                path = self.reconstruct_path(current_state)
                end_time = time.perf_counter()
                logs.append(f"➔ A* Search thành công hoàn hảo! Tổng bước đi: {len(path) - 1}")
                return path, logs, {
                    "steps": len(path) - 1,
                    "nodes": self.nodes_expanded,
                    "time_ms": (end_time - self.start_time) * 1000
                }

            for successor in current_state.get_successors():
                # Mỗi hành động di chuyển hoặc hút bụi tốn 1 chi phí g(n)
                new_g = current_g + 1

                # Nếu tìm thấy đường đi tới trạng thái này ngắn hơn hoặc trạng thái này hoàn toàn mới
                if successor not in g_cost or new_g < g_cost[successor]:
                    g_cost[successor] = new_g
                    h = self.get_heuristic(successor)
                    f = new_g + h
                    counter += 1
                    heapq.heappush(frontier, (f, new_g, counter, successor))

        end_time = time.perf_counter()
        return [], ["A* Search không tìm được đường đi!"], {"steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000}