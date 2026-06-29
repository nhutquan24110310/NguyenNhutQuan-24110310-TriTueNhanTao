# algorithms/informed/idastar.py
import time
from algorithms.base_search import BaseSearch

class IDAStarSearch(BaseSearch):
    def __init__(self, initial_state, heuristic_type="dirty"):
        super().__init__(initial_state)
        self.heuristic_type = heuristic_type  # "dirty" hoặc "manhattan"

    def get_heuristic(self, state):
        """Hàm tính Heuristic h(n) tương tự như A* và Greedy"""
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
        self.nodes_expanded = 0
        logs = []

        # Ngưỡng f-bound ban đầu chính bằng h(start)
        threshold = self.get_heuristic(self.initial_state)
        logs.append(f"Khởi động IDA* [{self.heuristic_type}] tại ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        # Khởi tạo mảng path dùng để kiểm tra vòng lặp trên nhánh đang duyệt (Tránh tốn bộ nhớ lưu tập Closed)
        path = [self.initial_state]

        while True:
            logs.append(f"--- Thử nghiệm với Ngưỡng f-bound = {threshold} ---")
            
            # Gọi hàm duyệt sâu giới hạn bởi f-bound
            result = self._dfs_bound(path, 0, threshold, logs)
            
            # Nếu kết quả trả về là một list tức là đã tìm thấy đường đi đến đích
            if isinstance(result, list):
                end_time = time.perf_counter()
                logs.append(f"➔ IDA* Search thành công! Tìm thấy lời giải tối ưu.")
                return result, logs, {
                    "steps": len(result) - 1,
                    "nodes": self.nodes_expanded,
                    "time_ms": (end_time - self.start_time) * 1000
                }
            
            # Nếu ngưỡng tiếp theo là vô hạn tức là đã duyệt hết không gian mà không có đích
            if result == float('inf'):
                end_time = time.perf_counter()
                return [], ["IDA* Search thất bại: Không tìm thấy giải pháp!"], {
                    "steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000
                }
                
            # Cập nhật ngưỡng f-bound mới bằng giá trị nhỏ nhất vượt ngưỡng cũ
            threshold = result

    def _dfs_bound(self, path, g, threshold, logs):
        """Hàm bổ trợ duyệt sâu kết hợp cắt tỉa theo f-bound"""
        current_node = path[-1]
        f = g + self.get_heuristic(current_node)

        # Nếu chi phí f vượt quá ngưỡng hiện tại -> cắt tỉa nhánh này và trả về giá trị f đó
        if f > threshold:
            return f
            
        # Kiểm tra mục tiêu dọn sạch sàn
        if current_node.is_goal():
            return list(path)

        min_val = float('inf')
        self.nodes_expanded += 1

        if self.nodes_expanded <= 15:
            logs.append(f"[Node {self.nodes_expanded}] f(n)={f} | g(n)={g} | Vị trí: ({current_node.robot_pos // 3}, {current_node.robot_pos % 3})")

        # Duyệt các trạng thái con kế tiếp
        for successor in current_node.get_successors():
            if successor not in path:  # Kiểm tra tránh trùng lặp vòng lặp trên nhánh hiện tại
                path.append(successor)
                
                # Gọi đệ quy đào sâu tiếp tục với g tăng thêm 1
                result = self._dfs_bound(path, g + 1, threshold, logs)
                
                if isinstance(result, list):
                    return result
                    
                if result < min_val:
                    min_val = result
                    
                path.pop()  # Backtrack phục hồi trạng thái nhánh
                
        return min_val