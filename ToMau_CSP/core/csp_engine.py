import random

class CSPSolver:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        # Bản sao để tránh ghi đè làm hỏng miền giá trị gốc
        self.domains = {k: list(v) for k, v in domains.items()}
        self.constraints = constraints
        self.assignment = {}

    def is_consistent(self, var, value):
        for neighbor in self.constraints.get(var, []):
            if neighbor in self.assignment and self.assignment[neighbor] == value:
                return False
        return True

    # --- THUẬT TOÁN 1: BACKTRACKING NGUYÊN BẢN ---
    def backtrack(self):
        if len(self.assignment) == len(self.variables):
            yield self.assignment, "SUCCESS", None
            return

        unassigned = [v for v in self.variables if v not in self.assignment]
        var = unassigned[0]

        for value in self.domains[var]:
            self.assignment[var] = value
            if self.is_consistent(var, value):
                yield self.assignment, "ASSIGN", (var, value)
                yield from self.backtrack()
                if len(self.assignment) == len(self.variables):
                    return
                yield self.assignment, "BACKTRACK", (var, value)
            else:
                yield self.assignment, "FAIL", (var, value)
            del self.assignment[var]

    # --- THUẬT TOÁN 2: TÌM KIẾM SÀNG LỌC AC-3 ---
    def ac3_and_search(self):
        # Khởi tạo hàng đợi tất cả các cung kề cạnh
        queue = []
        for u in self.variables:
            for v in self.constraints.get(u, []):
                queue.append((u, v))

        yield self.assignment, "AC3_START", None

        while queue:
            u, v = queue.pop(0)
            removed_values = []
            
            # Hàm loại bỏ các giá trị không nhất quán (RM-Inconsistent-Values)
            for val_u in list(self.domains[u]):
                # Kiểm tra xem có bất kỳ màu nào của v khác với màu val_u không
                has_support = any(val_v != val_u for val_v in self.domains[v])
                if not has_support:
                    self.domains[u].remove(val_u)
                    removed_values.append(val_u)
            
            if removed_values:
                yield self.assignment, "AC3_PRUNE", (u, v, removed_values, list(self.domains[u]))
                if not self.domains[u]:
                    yield self.assignment, "AC3_FAILED", u
                    return
                # Thêm lại các cung lân cận vào hàng đợi
                for neighbor in self.constraints.get(u, []):
                    if neighbor != v:
                        queue.append((neighbor, u))
        
        yield self.assignment, "AC3_DONE", None
        # Sau khi rút gọn miền khả thi bằng AC-3, tiến hành tìm kiếm lời giải trên miền sạch
        yield from self.backtrack()

    # --- THUẬT TOÁN 3: MIN-CONFLICTS (TỐI THIỂU XUNG ĐỘT) ---
    def min_conflicts(self, max_steps=200):
        self.assignment = {}
        # Bước 1: Khởi tạo một lời giải đầy đủ ngẫu nhiên (Complete Assignment)
        for var in self.variables:
            self.assignment[var] = random.choice(self.domains[var])
        
        yield self.assignment, "MC_INIT", dict(self.assignment)

        for step in range(1, max_steps + 1):
            conflicted_vars = []
            for u in self.variables:
                for v in self.constraints.get(u, []):
                    if self.assignment[u] == self.assignment[v]:
                        if u not in conflicted_vars: conflicted_vars.append(u)
            
            # Nếu không còn vùng nào bị trùng màu cạnh lân cận -> Thành công
            if not conflicted_vars:
                yield self.assignment, "SUCCESS", None
                return
            
            # Chọn ngẫu nhiên một biến bị xung đột
            var = random.choice(conflicted_vars)
            
            # Tìm giá trị màu làm giảm thiểu số xung đột nhất cho biến này
            best_val = self.assignment[var]
            min_c = float('inf')
            
            for val in self.domains[var]:
                old_val = self.assignment[var]
                self.assignment[var] = val
                
                # Đếm số cạnh xung đột cục bộ của biến var
                c = sum(1 for n in self.constraints.get(var, []) if self.assignment[n] == val)
                
                if c < min_c:
                    min_c = c
                    best_val = val
                elif c == min_c and random.random() > 0.5:
                    best_val = val # Phá vỡ thế cân bằng ngẫu nhiên để tránh lặp vô hạn
                
                self.assignment[var] = old_val
            
            self.assignment[var] = best_val
            yield self.assignment, "MC_STEP", (step, var, best_val, len(conflicted_vars))
            
        yield self.assignment, "MC_FAILED", None