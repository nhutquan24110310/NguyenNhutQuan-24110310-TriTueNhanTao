# models/vacuum_problem.py

class VacuumProblem:
    def __init__(self, initial_robot_pos, initial_dirty_cells, grid_size=(3, 3)):
        self.grid_size = grid_size
        self.initial_state = (initial_robot_pos, frozenset(initial_dirty_cells))

    def goal_test(self, state):
        robot_pos, dirty_cells = state
        return len(dirty_cells) == 0

    def actions(self, state):
        """Quy tắc chọn hành động"""
        robot_pos, dirty_cells = state
        
        # Nếu ô hiện tại bẩn -> Bắt buộc phải HÚT
        if robot_pos in dirty_cells:
            return ["SUCK"]
        
        # Nếu ô hiện tại sạch -> Tìm các hướng đi hợp lệ
        valid_moves = []
        r, c = robot_pos
        moves = {"UP": (r - 1, c), "DOWN": (r + 1, c), "LEFT": (r, c - 1), "RIGHT": (r, c + 1)}
        
        for direction, (nr, nc) in moves.items():
            if 0 <= nr < self.grid_size[0] and 0 <= nc < self.grid_size[1]:
                valid_moves.append(direction)
        return valid_moves

    def results(self, state, action):
        """MÔI TRƯỜNG ĐỊNH HƯỚNG (Deterministic) - ĐÃ FIX:
        Mỗi hành động chỉ trả về DUY NHẤT 1 kết quả chính xác 100%.
        """
        robot_pos, dirty_cells = state

        if action == "SUCK":
            # ĐÃ FIX: Hút ô nào sạch đúng ô đó, tuyệt đối không lan sang ô khác
            new_dirty = frozenset(dirty_cells - {robot_pos})
            return [(robot_pos, new_dirty)]
            
        else:
            # Di chuyển chính xác đến ô đích
            r, c = robot_pos
            moves = {"UP": (r-1, c), "DOWN": (r+1, c), "LEFT": (r, c-1), "RIGHT": (r, c+1)}
            target_pos = moves[action]
            return [(target_pos, dirty_cells)]