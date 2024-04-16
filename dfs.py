val = [[0,2,2,0,2,0,1,1,0,0],
       [1,0,0,1,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,0,2],
       [0,1,2,0,0,1,0,0,0,0],
       [0,0,0,0,0,1,0,0,1,1],
       [0,2,1,0,0,0,2,0,2,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,1,0,0,0,0,2,0,0],
       [0,2,0,1,1,0,1,0,0,1],
       [0,0,0,0,1,0,0,0,0,0]]

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

def check(val):
    for i in range(len(val)):
        for j in range(len(val[0])):
            if val[i][j] == 0:
                return False
    return True

def satisfy(i, j, val, board, blackInCol, blackInRow, whiteInCol, whiteInRow):
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
                    # print(board[n])
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
            if i == len(board):
                if check(board):
                    return True
            else:
                return backtrack(i+1, 0, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
        else:
            return backtrack(i, j+1, board, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)

if __name__ == "__main__":
    # print(blackInRow, blackInCol, whiteInRow, whiteInCol)
    backtrack(0, 0, val, defVal, blackInRow, blackInCol, whiteInRow, whiteInCol)
    for i in range(len(val)):
        print(val[i])