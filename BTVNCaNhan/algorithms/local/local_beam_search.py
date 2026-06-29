# algorithms/local/local_beam_search.py
import time
from algorithms.local.base_local import BaseLocalSearch

class LocalBeamSearch(BaseLocalSearch):
    def __init__(self, initial_state, heuristic_type="manhattan", k=3):
        super().__init__(initial_state, heuristic_type)
        self.k = k

    def search(self):
        start_time = time.perf_counter()
        nodes_expanded = 0
        logs = [f"Khởi chạy Local Beam Search với k = {self.k}..."]
        current_beam = [(self.initial_state, [self.initial_state])]
        
        iteration = 0
        while iteration < 1000:
            iteration += 1
            neighbor_states = []
            
            for state, path in current_beam:
                successors = state.get_successors()
                nodes_expanded += 1
                for succ in successors:
                    neighbor_states.append((succ, path + [succ]))
            
            if not neighbor_states:
                break
                
            for succ, path in neighbor_states:
                if succ.is_goal():
                    end_time = time.perf_counter()
                    logs.append("➔ [Thành công] Tìm thấy đích từ tập chùm lân cận!")
                    return path, logs, {"steps": len(path)-1, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}
            
            neighbor_states.sort(key=lambda x: self.get_value(x[0]), reverse=True)
            current_beam = neighbor_states[:self.k]
            logs.append(f"Vòng lặp {iteration}: Đang giữ {len(current_beam)} nhánh tốt nhất.")

        end_time = time.perf_counter()
        return [], logs, {"steps": 0, "nodes": nodes_expanded, "time_ms": (end_time - start_time)*1000}