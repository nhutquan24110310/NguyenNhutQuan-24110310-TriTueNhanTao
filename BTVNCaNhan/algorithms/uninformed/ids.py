# algorithms/uninformed/ids.py
import time
from algorithms.base_search import BaseSearch

class IDS(BaseSearch):
    def search(self):
        self.start_time = time.perf_counter()
        logs = []
        self.nodes_expanded = 0
        
        # Giới hạn độ sâu tối đa để tránh vòng lặp vô hạn (Môi trường 3x3 cấu hình tối đa khoảng 30 độ sâu)
        max_limit = 40
        logs.append(f"Khởi động IDS từ ô: {self.initial_state.robot_pos // 3, self.initial_state.robot_pos % 3}")

        for depth in range(max_limit):
            logs.append(f"--- Thử nghiệm tìm kiếm với Độ sâu Giới hạn = {depth} ---")
            
            # Khởi tạo Stack lưu cặp giá trị: (Trạng thái, Độ sâu hiện tại của trạng thái đó)
            frontier = [(self.initial_state, 0)]
            reached = {} # Lưu {trạng thái: độ sâu nhỏ nhất từng đạt tới} nhằm loại bỏ nhánh lặp trùng

            while frontier:
                current_state, curr_depth = frontier.pop()

                if current_state.is_goal():
                    path = self.reconstruct_path(current_state)
                    end_time = time.perf_counter()
                    logs.append(f"➔ IDS thành công ở tầng sâu {depth}!")
                    return path, logs, {
                        "steps": len(path) - 1,
                        "nodes": self.nodes_expanded,
                        "time_ms": (end_time - self.start_time) * 1000
                    }

                # Nếu chưa vượt quá giới hạn tầng sâu hiện tại, tiếp tục bung nhánh con
                if curr_depth < depth:
                    self.nodes_expanded += 1
                    
                    if current_state in reached and reached[current_state] <= curr_depth:
                        continue
                    reached[current_state] = curr_depth

                    for successor in reversed(current_state.get_successors()):
                        frontier.append((successor, curr_depth + 1))

        end_time = time.perf_counter()
        return [], ["IDS vượt quá giới hạn độ sâu tối đa!"], {
            "steps": 0, "nodes": self.nodes_expanded, "time_ms": (end_time - self.start_time) * 1000
        }