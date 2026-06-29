# algorithms/informed/greedy.py
import heapq
import time
from algorithms.base_search import BaseSearch

class GreedySearch(BaseSearch):
    def __init__(self, initial_state, heuristic_type="dirty"):
        super().__init__(initial_state)
        self.heuristic_type = heuristic_type  # "dirty" hoặc "manhattan"

    def get_heuristic(self, state):
        """Hàm tính toán Heuristic h(n) cho Robot hút bụi"""
        grid = state.grid
        r, c = state.robot_pos // 3, state.robot_pos % 3
        dirty_indices = [i for i, val in enumerate(grid) if val == 1]

        if self.heuristic_type == "dirty":
            # Tương tự Misplaced Tiles: Đếm số lượng ô bẩn còn lại
            return len(dirty_indices)
        
        elif self.heuristic_type == "manhattan":
            if not dirty_indices:
                return 0
            # Khoảng cách Manhattan từ vị trí Robot hiện tại tới ô rác gần nhất
            min_dist = min(abs(r - (i // 3)) + abs(c - (i % 3)) for i in dirty_indices)
            return len(dirty_indices) + min_dist
        return 0

    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0

        counter = 0
        frontier = []
        # Lưu định dạng: (h(n), counter, state) giống thiết kế PriorityQueue của bạn
        start_h = self.get_heuristic(self.initial_state)
        heapq.heappush(frontier, (start_h, counter, self.initial_state))

        visited = set()
        logs.append(f"Khởi động Greedy [{self.heuristic_type}] tại ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        while frontier:
            current_h, _, current_state = heapq.heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            self.nodes_expanded += 1

            if self.nodes_expanded <= 15:
                logs.append(f"[Node {self.nodes_expanded}] h(n) = {current_h} | Vị trí: ({current_state.robot_pos // 3}, {current_state.robot_pos % 3})")

            # Kiểm tra Goal khi lấy ra khỏi hàng đợi (Late Goal Test chuẩn slide)
            if current_state.is_goal():
                path = self.reconstruct_path(current_state)
                end_time = time.perf_counter()
                logs.append(f"➔ Greedy Search thành công! Đã tìm thấy đích.")
                return path, logs, {
                    "steps": len(path) - 1,
                    "nodes": self.nodes_expanded,
                    "time_ms": (end_time - self.start_time) * 1000
                }

            for successor in current_state.get_successors():
                if successor not in visited:
                    h = self.get_heuristic(successor)
                    counter += 1
                    heapq.heappush(frontier, (h, counter, successor))

        end_time = time.perf_counter()
        return [], ["Greedy Search thất bại!"], {"steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000}