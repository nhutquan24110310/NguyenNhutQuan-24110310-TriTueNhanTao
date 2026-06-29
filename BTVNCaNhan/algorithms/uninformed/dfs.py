# algorithms/uninformed/dfs.py
import time
from algorithms.base_search import BaseSearch

class DFS(BaseSearch):
    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0

        # Frontier đóng vai trò là một Stack (LIFO)
        frontier = [self.initial_state]
        reached = set()

        logs.append(f"Khởi động DFS từ ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        while frontier:
            current_state = frontier.pop()

            # Bỏ qua nếu trạng thái này đã được mở rộng trước đó
            if current_state in reached:
                continue

            reached.add(current_state)
            self.nodes_expanded += 1

            if self.nodes_expanded <= 15:
                logs.append(f"[Node {self.nodes_expanded}] Đang đào sâu tại ô ({current_state.robot_pos // 3}, {current_state.robot_pos % 3})")

            # Kiểm tra mục tiêu muộn khi lấy ra khỏi Stack (Chuẩn Graph-Search DFS)
            if current_state.is_goal():
                path = self.reconstruct_path(current_state)
                end_time = time.perf_counter()
                logs.append(f"➔ DFS thành công! Tìm ra giải pháp sau khi duyệt {self.nodes_expanded} nodes.")
                return path, logs, {
                    "steps": len(path) - 1,
                    "nodes": self.nodes_expanded,
                    "time_ms": (end_time - self.start_time) * 1000
                }

            # Thêm các nút con vào stack theo thứ tự đảo ngược để giữ đúng chiều duyệt
            for successor in reversed(current_state.get_successors()):
                if successor not in reached:
                    frontier.append(successor)

        end_time = time.perf_counter()
        return [], ["DFS thất bại!"], {"steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000}