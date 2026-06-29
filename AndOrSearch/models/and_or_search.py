# models/and_or_search.py

def and_or_graph_search(problem):
    """Bắt đầu thuật toán AND-OR Search"""
    return or_search(problem.initial_state, problem, [])

def or_search(state, problem, path):
    # if state ∈ problem.goal_test
    if problem.goal_test(state):
        return []  # Kế hoạch rỗng (đã đạt mục tiêu)
        
    # if state ∈ path: return failure (tránh lặp)
    if state in path:
        return "failure"
        
    # for each action in problem.actions(state)
    for action in problem.actions(state):
        result_states = problem.results(state, action)
        
        # plan = AND_SEARCH(result_states, problem, path + [state])
        plan = and_search(result_states, problem, path + [state])
        
        if plan != "failure":
            return [action, plan]
            
    return "failure"

def and_search(states, problem, path):
    plans = {}  # empty mapping: lưu kế hoạch cho từng state
    
    for s in states:
        plan_s = or_search(s, problem, path)
        if plan_s == "failure":
            return "failure"
        plans[s] = plan_s
        
    return plans