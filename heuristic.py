from copy import deepcopy
import time
import pyautogui as gui
import tracemalloc
LAPTOPSCREEN = False

input("Move the mouse to the top left of the grid")
topLeft = gui.position()
input("Move the mouse to the bottom right of the grid")
botRight = gui.position()
gridRows = int(input("How many rows are in the grid: "))
gridCols = int(input("How many cols are in the grid: "))

BLACK = (102, 102, 102, 255)
WHITE = (204, 204, 204, 255)
EMPTY = (255, 255, 255, 255)
val = [[0 for j in range(gridCols)] for i in range(gridRows)]
blackInRow = [0 for i in range(gridRows)]
blackInCol = [0 for i in range(gridCols)]
whiteInRow = [0 for i in range(gridRows)]
whiteInCol = [0 for i in range(gridCols)]
im = gui.screenshot()

cellWidth = (botRight[0]-topLeft[0])/gridCols
cellHeight = (botRight[1]-topLeft[1])/gridRows

def readPixel(x, y):
    if LAPTOPSCREEN:
        x *= 2
        y *= 2
    return im.getpixel((x, y))

def readCellColour(i, j):
    curX = topLeft[0]+cellWidth/2+cellWidth*j
    curY = topLeft[1]+cellHeight/2+cellHeight*i
    cols = []
    for k in range(-int(cellWidth/4), int(cellWidth/4)+1):
        for l in range(-int(cellHeight/4), int(cellHeight/4)+1):
            pixel = readPixel(curX+k, curY+l)
            ind = -1
            for x in range(len(cols)):
                if cols[x][1] == pixel:
                    ind = x
                    break
            if ind == -1:
                ind = len(cols)
                cols.append([0, pixel])
            cols[ind][0] += 1
    cols.sort(reverse=True)
    if len(cols) == 1:
        return 0
    if cols[0][1][0] < 128:
        return 1
    return 2

for i in range(gridRows):
    for j in range(gridCols):
        val[i][j] = readCellColour(i, j)

defVal = []
for x in range(len(val)):
    for y in range(len(val[x])):
        if val[x][y] != 0:
            defVal.append([x,y])

blackInRow = [0 for i in range(len(val))]
whiteInRow = [0 for i in range(len(val))]
blackInCol = [0 for j in range(len(val[0]))]
whiteInCol = [0 for j in range(len(val[0]))]

for i in range(len(val)):
    for j in range(len(val[0])):
        if (val[i][j] == 1):
            blackInRow[i] +=1
            blackInCol[j] +=1
        elif (val[i][j] == 2):
            whiteInRow[i] +=1
            whiteInCol[j] +=1

gridRows = len(val)
gridCols = len(val[0])

def setVal(row, col, c, blackInRow, blackInCol, whiteInRow, whiteInCol):
    val[row][col] = c
    if c == 1:
        blackInRow[row] += 1
        blackInCol[col] += 1
    else:
        whiteInRow[row] += 1
        whiteInCol[col] += 1

def printGrid():
    for i in range(gridRows):
        for j in range(gridCols):
            print(val[i][j], end="")
        print()

def doComplete(board, blackInRow, blackInCol, whiteInRow, whiteInCol):
    ret = False
    for i in range(gridRows):
        for j in range(gridCols):
            if board[i][j] == 0:
                if blackInRow[i] == gridCols/2 or blackInCol[j] == gridRows/2:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif whiteInRow[i] == gridCols/2 or whiteInCol[j] == gridRows/2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    return ret

def doThree(board, blackInRow, blackInCol, whiteInRow, whiteInCol):
    # vertical up
    ret = False
    for i in range(2, gridRows):
        for j in range(gridCols):
            if board[i][j] == 0 and board[i-1][j] == board[i-2][j]:
                if board[i-1][j] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif val[i-1][j] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    # vertical down
    for i in range(gridRows-2):
        for j in range(gridCols):
            if board[i][j] == 0 and board[i+1][j] == board[i+2][j]:
                if board[i+1][j] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif board[i+1][j] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    # vertical middle
    for i in range(1, gridRows-1):
        for j in range(gridCols):
            if board[i][j] == 0 and board[i-1][j] == board[i+1][j]:
                if board[i+1][j] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif board[i+1][j] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    # horizontal left
    for i in range(gridRows):
        for j in range(2, gridCols):
            if board[i][j] == 0 and board[i][j-1] == board[i][j-2]:
                if board[i][j-1] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif board[i][j-1] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    # horizontal right
    for i in range(gridRows):
        for j in range(gridCols-2):
            if board[i][j] == 0 and board[i][j+1] == board[i][j+2]:
                if board[i][j+1] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif board[i][j+1] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    # horizontal middle
    for i in range(gridRows):
        for j in range(1, gridCols-1):
            if board[i][j] == 0 and board[i][j-1] == board[i][j+1]:
                if board[i][j+1] == 1:
                    setVal(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
                elif board[i][j+1] == 2:
                    setVal(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    ret = True
    return ret

def doForce(board, blackInRow, blackInCol, whiteInRow, whiteInCol):
    ret = False
    for i in range(gridRows):
        if blackInRow[i] == gridCols/2-1 and whiteInRow[i] < gridCols/2-1:
            for j in range(gridCols-2):
                num = 0
                for k in range(3):
                    if board[i][j+k] == 0 or board[i][j+k] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridCols):
                        if (k < j or k > j+2) and board[i][k] == 0:
                            if satisfy(i, k, 2, board, blackInCol,blackInRow, whiteInCol, whiteInRow):
                                setVal(i, k, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                ret = True
        elif blackInRow[i] < gridCols/2-1 and whiteInRow[i] == gridCols/2-1:
            for j in range(gridCols-2):
                num = 0
                for k in range(3):
                    if board[i][j+k] == 0 or board[i][j+k] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridCols):
                        if (k < j or k > j+2) and board[i][k] == 0:
                            if satisfy(i, k, 1, board, blackInCol,blackInRow, whiteInCol, whiteInRow):
                                setVal(i, k, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                ret = True
    for j in range(gridCols):
        if blackInCol[j] == gridRows/2-1 and whiteInCol[j] < gridRows/2-1:
            for i in range(gridRows-2):
                num = 0
                for k in range(3):
                    if board[i+k][j] == 0 or board[i+k][j] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridRows):
                        if (k < i or k > i+2) and board[k][j] == 0:
                            if satisfy(k, j, 2, board, blackInCol,blackInRow, whiteInCol, whiteInRow):
                                setVal(k, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                ret = True
        elif blackInCol[j] < gridRows/2-1 and whiteInCol[j] == gridRows/2-1:
            for i in range(gridRows-2):
                num = 0
                for k in range(3):
                    if board[i+k][j] == 0 or board[i+k][j] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridRows):
                        if (k < i or k > i+2) and board[k][j] == 0:
                            if satisfy(i, k, 1, board, blackInCol,blackInRow, whiteInCol, whiteInRow):
                                setVal(k, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                ret = True
    return ret

def constraint_checking(board, blackInRow, blackInCol, whiteInRow, whiteInCol):
    while True:
        changed = False
        changed = changed or doComplete(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
        changed = changed or doThree(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
        changed = changed or doForce(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
        if not changed:
            break
    finished = True
    for i in range(gridRows):
        for j in range(gridCols):
            if board[i][j] == 0:
                finished = False
                return finished
    return finished

def check(val):
    for i in range(len(val)):
        for j in range(len(val[0])):
            if val[i][j] == 0:
                return False
    return True

def satisfy(i, j, val, board, blackInCol, blackInRow, whiteInCol, whiteInRow):
    if(j == len(board[0]) - 1):
        row_i = deepcopy(board[i])
        row_i[j] = val
        for index, row in enumerate(board):
            if row == row_i and index != i:
                # print("Hang", i, "giong hang", index)
                row_i[j] = 0
                return False
    if (i == len(board) - 1):
        col_j = [row[j] for row in board]
        col_j[i] = val
        for index, col in enumerate(zip(*board)):
            if list(col) == col_j and index != j:
                # print(col_j)
                # print(col)
                col_j[i] = 0
                # print("Cot", j, "giong cot", index)
                return False

    if val == 1:
        if blackInCol[j] == len(board[i])/2:
            return False
        if blackInRow[i] == len(board[i])/2:
            return False
    else:
        if whiteInCol[j] == len(board[i])/2:
            return False
        if whiteInRow[i] == len(board[i])/2:
            return False
    if i == 0:
        if val == board[i+1][j] ==board[i+2][j]:
            return False
        if j ==0:
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == 1:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == len(board[i]) -2:
            if val == board[i][j - 2] == board[i][j - 1]:
                return False
            if val == board[i][j-1] == board[i][j+1]:
                return False
        elif j == len(board[i]) - 1:
            if val == board[i][j-2] == board[i][j-1]:
                return False
        else:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
            if val == board[i][j - 2] == board[i][j-1]:
                return False
    elif i == 1:
        if val == board[i-1][j] ==board[i+1][j]:
            return False
        elif val == board[i+1][j] == board[i+2][j]:
            return False
        elif j ==0:
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == 1:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == len(board[i]) -2:
            if val == board[i][j - 2] == board[i][j - 1]:
                return False
            if val == board[i][j-1] == board[i][j+1]:
                return False
        elif j == len(board[i]) - 1:
            if val == board[i][j-2] == board[i][j-1]:
                return False
        else:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
            if val == board[i][j - 2] == board[i][j-1]:
                return False
    elif i == len(board)-2:
        if val == board[i-1][j] == board[i+1][j]:
            return False
        if val == board[i-2][j] == board[i-1][j]:
            return False
        if j ==0:
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == 1:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == len(board[i]) -2:
            if val == board[i][j - 2] == board[i][j - 1]:
                return False
            if val == board[i][j-1] == board[i][j+1]:
                return False
        elif j == len(board[i]) - 1:
            if val == board[i][j-2] == board[i][j-1]:
                return False
        else:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
            if val == board[i][j - 2] == board[i][j-1]:
                return False
    elif i == len(board) - 1:
        if val == board[i-2][j] == board[i-1][j]:
            return False
        if j ==0:
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == 1:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == len(board[i]) -2:
            if val == board[i][j - 2] == board[i][j - 1]:
                return False
            if val == board[i][j-1] == board[i][j+1]:
                return False
        elif j == len(board[i]) - 1:
            if val == board[i][j-2] == board[i][j-1]:
                return False
        else:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
            if val == board[i][j - 2] == board[i][j-1]:
                return False
    else:
        if val == board[i-1][j] == board[i+1][j]:
            return False
        if val == board[i+1][j] == board[i+2][j]:
            return False
        if val == board[i-2][j] == board[i-1][j]:
            return False
        if j ==0:
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == 1:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
        elif j == len(board[i]) -2:
            if val == board[i][j - 2] == board[i][j - 1]:
                return False
            if val == board[i][j-1] == board[i][j+1]:
                return False
        elif j == len(board[i]) - 1:
            if val == board[i][j-2] == board[i][j-1]:
                return False
        else:
            if val == board[i][j - 1] == board[i][j+1]:
                return False
            if val == board[i][j+1] == board[i][j+2]:
                return False
            if val == board[i][j - 2] == board[i][j-1]:
                return False
    return True
    
def backtrack(i, j, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol):
    if([i, j] not in defVal):
        for x in range(1, 3):
            if satisfy(i, j, x, board, blackInCol, blackInRow, whiteInCol, whiteInRow):
                board[i][j] = x
                # print(i,j)
                # print(x)
                # for n in range(len(board)):
                #     print(board[n])
                # print()
                if x == 1:
                    blackInCol[j] += 1
                    blackInRow[i] += 1
                else:
                    whiteInCol[j] += 1
                    whiteInRow[i] += 1
                # print(blackInRow, blackInCol, whiteInRow, whiteInCol)
                # input()
                if j == len(board[i])-1:
                    if i == len(board)-1:
                        if check(board):
                            return True
                    else:
                        flag = backtrack(i+1, 0, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        if flag == False:
                            # print("FALSE", i, j, "value", x)
                            if x == 1:
                                blackInCol[j] -= 1
                                blackInRow[i] -= 1
                            else:
                                whiteInCol[j] -= 1
                                whiteInRow[i] -= 1
                            board[i][j] = 0
                            pass
                        else:
                            return True
                else:
                    flag = backtrack(i, j+1, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
                    if flag == False:
                        # print("FALSE", i, j, "value", x)
                        if x == 1:
                            blackInCol[j] -= 1
                            blackInRow[i] -= 1
                        else:
                            whiteInCol[j] -= 1
                            whiteInRow[i] -= 1
                        board[i][j] = 0
                        pass
                    elif flag == True:
                        return True
            else:
                pass
        return False
    else:
        if j == len(board[i]) - 1:
            if i == len(board) - 1:
                if check(board):
                    return True
            else:
                return backtrack(i+1, 0, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
        else:
            return backtrack(i, j+1, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)

if __name__ == "__main__":
    tracemalloc.start()
    startTime = time.time()
    finished = constraint_checking(val, blackInRow, blackInCol, whiteInRow, whiteInCol)
    if not finished:
        defVal = []
        for x in range(len(val)):
            for y in range(len(val[x])):
                if val[x][y] != 0:
                    defVal.append([x,y])
        
        finished = backtrack(0, 0, val, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
    if finished:
        for x in val:
            print(x)

    # for x in val:
    #         print(x)
    executionTime = time.time() - startTime
    print("Execution time is:", executionTime)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()