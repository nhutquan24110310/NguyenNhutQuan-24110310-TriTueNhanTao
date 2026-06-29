# algorithms/uninformed/bfs.py
from collections import deque
import time
from algorithms.base_search import BaseSearch

class BFS(BaseSearch):
    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0

        # Kiểm tra nếu trạng thái khởi đầu đã sạch sẵn
        if self.initial_state.is_goal():
            end_time = time.perf_counter()
            return [self.initial_state], ["Môi trường sạch sẵn từ đầu!"], {
                "steps": 0, "nodes": 0, "time_ms": (end_time - self.start_time) * 1000
            }

        # Frontier là một hàng đợi Double-ended Queue (FIFO)
        frontier = deque([self.initial_state])
        # Tập reached lưu trữ các đối tượng VacuumState đã duyệt qua
        reached = {self.initial_state}

        logs.append(f"Khởi động BFS từ ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        while frontier:
            current_state = frontier.popleft()
            self.nodes_expanded += 1

            # Ghi log chọn lọc để tránh làm lag giao diện UI khi số node quá lớn
            if self.nodes_expanded <= 15:
                logs.append(f"[Step {self.nodes_expanded}] Duyệt ô ({current_state.robot_pos // 3}, {current_state.robot_pos % 3}) | Rác còn lại: {sum(current_state.grid)}")

            # Phát triển các trạng thái con kế tiếp
            for successor in current_state.get_successors():
                if successor not in reached:
                    # Kiểm tra đích sớm ngay khi sinh nút con (Tối ưu theo Tiếp cận 2 của bạn)
                    if successor.is_goal():
                        path = self.reconstruct_path(successor)
                        end_time = time.perf_counter()
                        logs.append(f"➔ BFS thành công! Tìm thấy đường đi ngắn nhất: {len(path) - 1} bước.")
                        return path, logs, {
                            "steps": len(path) - 1,
                            "nodes": self.nodes_expanded,
                            "time_ms": (end_time - self.start_time) * 1000
                        }
                    reached.add(successor)
                    frontier.append(successor)

        end_time = time.perf_counter()
        return [], ["BFS thất bại: Không tìm thấy giải pháp dọn dẹp!"], {
            "steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000
        }