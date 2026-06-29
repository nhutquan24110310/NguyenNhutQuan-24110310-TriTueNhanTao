# models/state.py

class VacuumState:
    def __init__(self, robot_pos, grid, parent=None, action=None, cost=0):
        self.robot_pos = robot_pos     # Vị trí robot trong trạng thái này (0-8)
        self.grid = tuple(grid)        # Chuyển thành tuple (để dữ liệu không bị sửa và có thể dùng set() lưu visited)
        self.parent = parent           # Trạng thái cha dẫn đến trạng thái này (dùng để truy vết đường đi)
        self.action = action           # Hành động dẫn đến trạng thái này ('UP', 'DOWN', 'LEFT', 'RIGHT', 'SUCK')
        self.cost = cost               # Giá trị g(n): số bước đi từ trạng thái khởi đầu

    def is_goal(self):
        """Đích đến là khi TẤT CẢ các ô trong lưới đều sạch (tổng số rác bằng 0)"""
        return sum(self.grid) == 0

    def get_successors(self):
        """
        Hàm sinh con (Successor Function): 
        Từ trạng thái này, robot có thể làm gì tiếp theo? Trả về danh sách các trạng thái hợp lệ kế tiếp.
        """
        successors = []
        r, c = self.robot_pos // 3, self.robot_pos % 3

        # 1. Hành động HÚT BỤI (SUCK): Chỉ thực hiện nếu ô hiện tại đang bẩn
        if self.grid[self.robot_pos] == 1:
            new_grid = list(self.grid)
            new_grid[self.robot_pos] = 0  # Hút sạch bẩn tại ô này
            successors.append(VacuumState(
                robot_pos=self.robot_pos,
                grid=new_grid,
                parent=self,
                action="SUCK",
                cost=self.cost + 1
            ))

        # 2. Các hành động DI CHUYỂN (Lên, Xuống, Trái, Phải)
        directions = {
            "UP": (r - 1, c),
            "DOWN": (r + 1, c),
            "LEFT": (r, c - 1),
            "RIGHT": (r, c + 1)
        }

        for move, (nr, nc) in directions.items():
            # Kiểm tra xem di chuyển có vượt ra khỏi lưới 3x3 không
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_pos = nr * 3 + nc
                successors.append(VacuumState(
                    robot_pos=new_pos,
                    grid=self.grid, # Giữ nguyên trạng thái rác cũ
                    parent=self,
                    action=move,
                    cost=self.cost + 1
                ))

        return successors

    # --- Các hàm bổ trợ để thuật toán AI so sánh và lưu trữ Node tránh lặp vô hạn ---
    def __eq__(self, other):
        """Hai trạng thái bằng nhau nếu vị trí robot và ma trận rác giống hệt nhau"""
        if not isinstance(other, VacuumState):
            return False
        return self.robot_pos == other.robot_pos and self.grid == other.grid

    def __hash__(self):
        """Hàm băm giúp thuật toán đưa trạng thái vào set (Visited Set) cực nhanh"""
        return hash((self.robot_pos, self.grid))