# 1. Kiem tra xem ban co da giong dich den chua
def is_goal(board):
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    return board == goal

# 2. Tim toa do (hang, cot) cua o trong (so 0)
def find_zero(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return row, col
    return -1, -1

# 3. Quyet dinh huong di, bo luat day du cho 4 huong
def choose_action(row, col):
    if col < 2:
        return "RIGHT"
    elif row < 2:
        return "DOWN"
    elif col > 0:
        return "LEFT"
    elif row > 0:
        return "UP"
    return "NONE"

# 4. Doi cho so 0 va so ben canh
def move_zero(board, action, row, col):
    new_row = row
    new_col = col
    
    if action == "RIGHT":
        new_col = col + 1
    elif action == "DOWN":
        new_row = row + 1
    elif action == "LEFT":
        new_col = col - 1
    elif action == "UP":
        new_row = row - 1
        
    if action != "NONE":
        board[row][col] = board[new_row][new_col]
        board[new_row][new_col] = 0

# 5. In ban co ra man hinh
def print_board(board):
    for row in board:
        print(row)
    print("-------------")


# Main
if __name__ == "__main__":
    
    board = [
        [1, 2, 3],
        [5, 6, 4],
        [8, 7, 0]
    ]

    print("STARTING STATE:")
    print_board(board)

    step = 1
    max_steps = 15  # Gioi han so buoc de tranh lap vo han
    
    while not is_goal(board):
        # Kiem tra neu vuot qua gioi han so buoc
        if step > max_steps:
            print("FAILED: Agent is stuck in an infinite loop!")
            break
            
        r, c = find_zero(board)
        action = choose_action(r, c)
        
        # Kiem tra neu khong co luat nao phu hop
        if action == "NONE":
            print("FAILED: No valid move found!")
            break
            
        print(f"STEP {step} - Action: Move {action}")
        move_zero(board, action, r, c)
        step += 1
        
    if is_goal(board):
        print("GOAL REACHED!")