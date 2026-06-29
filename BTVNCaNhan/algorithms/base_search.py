# algorithms/base_search.py
import time

class BaseSearch:
    def __init__(self, initial_state):
        """
        Khởi tạo lớp thuật toán với trạng thái xuất phát ban đầu.
        initial_state: Đối tượng VacuumState lấy từ môi trường hiện tại.
        """
        self.initial_state = initial_state
        self.nodes_expanded = 0  # Bộ đếm số lượng node đã duyệt qua
        self.start_time = 0.0

    def search(self):
        """
        Mọi thuật toán kế thừa (BFS, DFS, A*,...) BẮT BUỘC phải viết đè (override) hàm này.
        Hàm này thực hiện logic tìm kiếm và phải trả về đúng bộ 3 giá trị:
        
        Trả về (Tuple):
            - path (list): Danh sách các đối tượng VacuumState nối tiếp từ trạng thái đầu đến đích.
            - logs (list): Danh sách các chuỗi text (str) ghi lại diễn biến tìm kiếm.
            - stats (dict): Thống kê hiệu năng {"nodes": int, "time_ms": float, "steps": int}
        """
        raise NotImplementedError("Bạn chưa cài đặt hàm search() cho thuật toán này!")

    def reconstruct_path(self, goal_state):
        """
        Hàm bổ trợ: Truy vết ngược từ Trạng thái Đích quay về Trạng thái Đầu 
        bằng cách lần theo thuộc tính 'parent' của từng State.
        """
        path = []
        current = goal_state
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]  # Đảo ngược mảng để thu được lộ trình xuôi: Đầu -> ... -> Đích