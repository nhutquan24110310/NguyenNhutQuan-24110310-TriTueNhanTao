import random

# Du lieu ma tran
matrix = [[1,1,1],
         [1,1,1],
         [1,1,1]]

# Random vi tri ban dau
x = random.randint(0,2)
y = random.randint(0,2)

# Ham in ma tran
def printMatrix():
    for i in range(3):
        for j in range(3):
            if i == x and j == y:
                # in vi tri Agent
                print(f"A({matrix[i][j]})", end="\t")
            else:
                print(matrix[i][j], end="\t\t")
        print()

# Lay vi tri kha thi
def getPossibleMoves(x, y):
    moves = []
    if x > 0:
        moves.append("UP")
    if x < 2:
        moves.append("DOWN")
    if y > 0:
        moves.append("LEFT")
    if y < 2:
        moves.append("RIGHT")
    print(moves)
    return moves

def reflexAgent():
    global x,y
    currentState = matrix[x][y]
    print("vi tri: ",x,y)
    print("Trang thai: ", currentState)

    if currentState == 1:
        print("Rule Matched:")
        print("IF Current Cell is Dirty THEN SUCK")

        print("Action: SUCK")

        matrix[x][y] = 0
    else:
        print("Rule Matched:")
        print("IF Current Cell is Clean THEN RANDOM MOVE")

        # Check con nuoc di nao kha thi hay khong neu khong thi return
        possibleMoves = getPossibleMoves(x, y)
        if not possibleMoves:
            return
        
        move = random.choice(possibleMoves)

        print(f"Huong ngau nhien: {move}")

        # di chuyen
        if move == "UP":
            x -= 1

        elif move == "DOWN":
            x += 1

        elif move == "LEFT":
            y -= 1

        elif move == "RIGHT":
            y += 1

steps = 10
printMatrix()
for i in range(steps):
    print("-------------------------------")
    print("Buoc", i+1)
    reflexAgent()
    printMatrix()