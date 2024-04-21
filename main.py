import pyautogui as gui
from copy import deepcopy

LAPTOPSCREEN = False
# color channel
BLACK = (102, 102, 102, 255)
WHITE = (204, 204, 204, 255)
EMPTY = (255, 255, 255, 255)


class Game():
    def __init__(self):
        input("Move the mouse to the top left of the grid")
        self.topLeft = gui.position()
        input("Move the mouse to the bottom right of the grid")
        self.botRight = gui.position()
        self.gridRows = int(input("How many rows are in the grid: "))
        self.gridCols = int(input("How many cols are in the grid: "))
        self.val = [[0 for j in range(self.gridCols)] for i in range(self.gridRows)]
        self.defaultVal = []
        self.blackInRow = [0 for i in range(self.gridRows)]
        self.blackInCol = [0 for i in range(self.gridCols)]
        self.whiteInRow = [0 for i in range(self.gridRows)]
        self.whiteInCol = [0 for i in range(self.gridCols)]
        self.im = gui.screenshot()
        self.cellWidth = (self.botRight[0]-self.topLeft[0])/self.gridCols
        self.cellHeight = (self.botRight[1]-self.topLeft[1])/self.gridRows
        self.read_init_grid()
    
    def readPixel(self, x, y):
        if LAPTOPSCREEN:
            x*=2
            y*=2
        return self.im.getpixel((x, y))
    
    def readCellColour(self, i, j):
        curX = self.topLeft[0] + self.cellWidth/2 + self.cellWidth*j
        curY = self.topLeft[1] + self.cellHeight/2 + self.cellHeight*i
        cols = []
        for k in range(-int(self.cellWidth/4), int(self.cellWidth/4)+1):
            for l in range(-int(self.cellHeight/4), int(self.cellHeight/4)+1):
                pixel = self.readPixel(curX+k, curY+l)
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
            self.defaultVal.append([i,j])
            return 1
        self.defaultVal.append([i,j])
        return 2
        
    def read_init_grid(self):
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                self.val[i][j] = self.readCellColour(i, j)
        for i in range(self.gridRows):    
            for j in range(self.gridCols):
                if self.val[i][j] == 1:
                    self.blackInRow[i] += 1
                    self.blackInCol[j] += 1
                elif self.val[i][j] == 2:
                    self.whiteInRow[i] += 1
                    self.whiteInCol[j] += 1
    def update_def_val(self):
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                if self.val[i][j] != 0:
                    if [i,j] not in self.defaultVal:
                        self.defaultVal.append([i,j])
    
    def setVal(self, row, col, value):
        self.val[row][col] = value
        x = self.topLeft[0] + self.cellWidth/2 + self.cellWidth*col
        y = self.topLeft[1] + self.cellHeight/2 + self.cellHeight*row
        if value == 1:
            gui.click(x, y)
            self.blackInRow[row] +=1
            self.blackInCol[col] +=1
        else:
            gui.rightClick(x, y)
            self.whiteInRow[row] +=1
            self.whiteInCol[col] +=1

    def unSetVal(self, row, col, value):
        self.val[row][col] = 0
        x = self.topLeft[0] + self.cellWidth/2 + self.cellWidth*col
        y = self.topLeft[1] + self.cellHeight/2 + self.cellHeight*row
        if value == 1:
            gui.rightClick(x, y)
            self.blackInRow[row] -=1
            self.blackInCol[col] -=1
        else:
            gui.click(x, y)
            self.whiteInRow[row] -=1
            self.whiteInCol[col] -=1

    def printGrid(self):
        print(" ", end="")
        for i in range(self.gridRows):
            self.__printLine()
            print("|", end=' ')
            for j in range(self.gridCols):
                print(self.val[i][j], end=" | ")
            print()
        self.__printLine()

    def __printLine(self):
        for i in range((self.gridCols+4)*3):
            print("-", end='')
        print()
    
    def __set_val_heuristic(self, row, col, value, blackInRow, blackInCol, whiteInRow, whiteInCol):
        self.val[row][col] = value
        x = self.topLeft[0] + self.cellWidth/2 + self.cellWidth*col
        y = self.topLeft[1] + self.cellHeight/2 + self.cellHeight*row
        if value == 1:
            gui.click(x, y)
            self.blackInRow[row] +=1
            self.blackInCol[col] +=1
        else:
            gui.rightClick(x, y)
            self.whiteInRow[row] +=1
            self.whiteInCol[col] +=1

    #constraint about max black or white in a row or column
    def constraint1(self, board, blackInRow, blackInCol, whiteInRow, whiteInCol):
        ret = False
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                if board[i][j] == 0:
                    if blackInRow[i] == self.gridCols/2 or blackInCol[j] == self.gridRows/2:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif whiteInRow[i] == self.gridCols/2 or whiteInCol[j] == self.gridRows/2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        return ret
    
    #constraint about two black or white cell next to each other => next cell must be reverse color
    def constraint2(self, board, blackInRow, blackInCol, whiteInRow, whiteInCol):
        # vertical up
        ret = False
        for i in range(2, self.gridRows):
            for j in range(self.gridCols):
                if board[i][j] == 0 and board[i-1][j] == board[i-2][j]:
                    if board[i-1][j] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i-1][j] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        # vertical down
        for i in range(self.gridRows-2):
            for j in range(self.gridCols):
                if board[i][j] == 0 and board[i+1][j] == board[i+2][j]:
                    if board[i+1][j] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i+1][j] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        # vertical middle
        for i in range(1, self.gridRows-1):
            for j in range(self.gridCols):
                if board[i][j] == 0 and board[i-1][j] == board[i+1][j]:
                    if board[i+1][j] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i+1][j] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        # horizontal left
        for i in range(self.gridRows):
            for j in range(2, self.gridCols):
                if board[i][j] == 0 and board[i][j-1] == board[i][j-2]:
                    if board[i][j-1] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i][j-1] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        # horizontal right
        for i in range(self.gridRows):
            for j in range(self.gridCols-2):
                if board[i][j] == 0 and board[i][j+1] == board[i][j+2]:
                    if board[i][j+1] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i][j+1] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        # horizontal middle
        for i in range(self.gridRows):
            for j in range(1, self.gridCols-1):
                if board[i][j] == 0 and board[i][j-1] == board[i][j+1]:
                    if board[i][j+1] == 1:
                        self.__set_val_heuristic(i, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
                    elif board[i][j+1] == 2:
                        self.__set_val_heuristic(i, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                        ret = True
        return ret
    
    def constraint3(self, board, blackInRow, blackInCol, whiteInRow, whiteInCol):
        ret = False
        for i in range(self.gridRows):
            if blackInRow[i] == self.gridCols/2-1 and whiteInRow[i] < self.gridCols/2-1:
                for j in range(self.gridCols - 2):
                    num = 0
                    for k in range(3):
                        if board[i][j+k] == 0 or board[i][j+k] == 2:
                            num += 1
                    if num == 3:
                        for k in range(self.gridCols):
                            if (k < j or k > j+2) and board[i][k] == 0:
                                if self.__satisfy(i, k, 2):
                                    self.__set_val_heuristic(i, k, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                    ret = True
            elif blackInRow[i] < self.gridCols/2-1 and whiteInRow[i] == self.gridCols/2-1:
                for j in range(self.gridCols-2):
                    num = 0
                    for k in range(3):
                        if board[i][j+k] == 0 or board[i][j+k] == 1:
                            num += 1
                    if num == 3:
                        for k in range(self.gridCols):
                            if (k < j or k > j+2) and board[i][k] == 0:
                                if self.__satisfy(i, k, 1):
                                    self.__set_val_heuristic(i, k, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                    ret = True
        for j in range(self.gridCols):
            if blackInCol[j] == self.gridRows/2-1 and whiteInCol[j] < self.gridRows/2-1:
                for i in range(self.gridRows-2):
                    num = 0
                    for k in range(3):
                        if board[i+k][j] == 0 or board[i+k][j] == 2:
                            num += 1
                    if num == 3:
                        for k in range(self.gridRows):
                            if (k < i or k > i+2) and board[k][j] == 0:
                                if self.__satisfy(k, j, 2):
                                    self.__set_val_heuristic(k, j, 2, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                    ret = True
            elif blackInCol[j] < self.gridRows/2-1 and whiteInCol[j] == self.gridRows/2-1:
                for i in range(self.gridRows-2):
                    num = 0
                    for k in range(3):
                        if board[i+k][j] == 0 or board[i+k][j] == 1:
                            num += 1
                    if num == 3:
                        for k in range(self.gridRows):
                            if (k < i or k > i+2) and board[k][j] == 0:
                                if self.__satisfy(i, k, 1):
                                    self.__set_val_heuristic(k, j, 1, blackInRow, blackInCol, whiteInRow, whiteInCol)
                                    ret = True
        return ret
    
    def constraint_checking(self, board, blackInRow, blackInCol, whiteInRow, whiteInCol):
        while True:
            change = False
            change = change or self.constraint1(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
            change = change or self.constraint2(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
            change = change or self.constraint3(board, blackInRow, blackInCol, whiteInRow, whiteInCol)
            if not change:
                break
        finished = True
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                if board[i][j] == 0:
                    finished = False
                    return finished
        return finished
            
    def __satisfy(self, i, j, x):
        if (j == self.gridCols - 1):
            row_i = deepcopy(self.val[i])
            row_i[j] = x
            for index, row in enumerate(self.val):
                if row == row_i and index != i:
                    row_i[j] = 0
                    return False
        if i == self.gridRows - 1:
            col_j = [row[j] for row in self.val]
            col_j[i] = x
            for index, col in enumerate(zip(*self.val)):
                if list(col) == col_j and index != j:
                    col_j[i] = 0
                    return False
        if x == 1:
            if self.blackInCol[j] == self.gridCols/2:
                return False
            if self.blackInRow[i] == self.gridCols/2:
                return False
        else:
            if self.whiteInCol[j] == self.gridCols/2:
                return False
            if self.whiteInRow[i] == self.gridCols/2:
                return False
        if i == 0:
            if x== self.val[i+1][j] ==self.val[i+2][j]:
                return False
            if j ==0:
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == 1:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == self.gridCols -2:
                if x == self.val[i][j - 2] == self.val[i][j - 1]:
                    return False
                if x == self.val[i][j-1] == self.val[i][j+1]:
                    return False
            elif j == self.gridCols - 1:
                if x == self.val[i][j-2] == self.val[i][j-1]:
                    return False
            else:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
                if x == self.val[i][j - 2] == self.val[i][j-1]:
                    return False
        elif i == 1:
            if x == self.val[i-1][j] ==self.val[i+1][j]:
                return False
            elif x == self.val[i+1][j] == self.val[i+2][j]:
                return False
            elif j ==0:
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == 1:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == self.gridCols -2:
                if x == self.val[i][j - 2] == self.val[i][j - 1]:
                    return False
                if x == self.val[i][j-1] == self.val[i][j+1]:
                    return False
            elif j == self.gridCols - 1:
                if x == self.val[i][j-2] == self.val[i][j-1]:
                    return False
            else:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
                if x == self.val[i][j - 2] == self.val[i][j-1]:
                    return False
        elif i == self.gridRows - 2:
            if x == self.val[i-1][j] == self.val[i+1][j]:
                return False
            if x == self.val[i-2][j] == self.val[i-1][j]:
                return False
            if j ==0:
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == 1:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == self.gridCols -2:
                if x == self.val[i][j - 2] == self.val[i][j - 1]:
                    return False
                if x == self.val[i][j-1] == self.val[i][j+1]:
                    return False
            elif j == self.gridCols - 1:
                if x == self.val[i][j-2] == self.val[i][j-1]:
                    return False
            else:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
                if x == self.val[i][j - 2] == self.val[i][j-1]:
                    return False
        elif i == self.gridRows - 1:
            if x == self.val[i-2][j] == self.val[i-1][j]:
                return False
            if j ==0:
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == 1:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == self.gridCols -2:
                if x == self.val[i][j - 2] == self.val[i][j - 1]:
                    return False
                if x == self.val[i][j-1] == self.val[i][j+1]:
                    return False
            elif j == self.gridCols - 1:
                if x == self.val[i][j-2] == self.val[i][j-1]:
                    return False
            else:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
                if x == self.val[i][j - 2] == self.val[i][j-1]:
                    return False
        else:
            if x == self.val[i-1][j] == self.val[i+1][j]:
                return False
            if x == self.val[i+1][j] == self.val[i+2][j]:
                return False
            if x == self.val[i-2][j] == self.val[i-1][j]:
                return False
            if j ==0:
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == 1:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
            elif j == self.gridCols -2:
                if x == self.val[i][j - 2] == self.val[i][j - 1]:
                    return False
                if x == self.val[i][j-1] == self.val[i][j+1]:
                    return False
            elif j == self.gridCols - 1:
                if x == self.val[i][j-2] == self.val[i][j-1]:
                    return False
            else:
                if x == self.val[i][j - 1] == self.val[i][j+1]:
                    return False
                if x == self.val[i][j+1] == self.val[i][j+2]:
                    return False
                if x == self.val[i][j - 2] == self.val[i][j-1]:
                    return False
        return True

    def __check(self):
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                if self.val[i][j] == 0:
                    return False
        return True

    def __backtrack(self, i, j):
        if([i, j] not in self.defaultVal):
            for x in range(1, 3):
                if self.__satisfy(i, j, x):
                    self.setVal(i, j, x)
                    if j == self.gridCols - 1:
                        if i == self.gridRows -1:
                            if self.__check():
                                return True
                        else:
                            flag = self.__backtrack(i+1, 0)
                            if flag == False:
                                self.unSetVal(i, j, x)
                                pass
                            else:
                                return True
                    else:
                        flag = self.__backtrack(i, j+1)
                        if flag == False:
                            self.unSetVal(i,j,x)
                        else:
                            return True
                else:
                    pass
            return False
        else:
            if j == self.gridCols - 1:
                if i == self.gridRows - 1:
                    if self.__check():
                        return True
                else:
                    return self.__backtrack(i+1, 0)
            else:
                return self.__backtrack(i, j+1)


    def dfs_solve(self):
        # self.check_constrain()
        # self.update_def_val()
        self.__backtrack(0,0)

    def heuristic_solve(self):
        finished = self.constraint_checking(self.val, self.blackInRow, self.blackInCol, self.whiteInRow, self.whiteInCol)
        if not finished:
            self.defaultVal = []
            for x in range(self.gridRows):
                for y in range(self.gridCols):
                    if self.val[x][y] != 0:
                        self.defaultVal.append([x,y])
            finished = self.__backtrack(0,0)
            return finished

if __name__ == "__main__":

    board = Game()
    # board.dfs_solve()
    board.heuristic_solve()
    board.printGrid()