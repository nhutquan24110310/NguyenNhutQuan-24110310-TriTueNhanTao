# algorithms/local/base_local.py
from algorithms.base_search import BaseSearch

class BaseLocalSearch(BaseSearch):
    """Lớp cơ sở chia sẻ hàm đánh giá cho mọi thuật toán cục bộ"""
    def __init__(self, initial_state, heuristic_type="manhattan"):
        super().__init__(initial_state)
        self.heuristic_type = heuristic_type

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

    def get_value(self, state):
        # Trạng thái càng ít rác/gần rác thì giá trị (Value) càng cao
        return -self.get_heuristic(state)