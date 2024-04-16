import pyautogui as gui

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
            return 1
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
    
    def constraint1(self):
        ret = False
        for i in range(self.gridRows):
            for j in range(self.gridCols):
                if self.val[i][j] == 0:
                    if self.blackInRow[i] == self.gridCols/2 or self.blackInCol[j] == self.gridRows/2:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.whiteInRow[i] == self.gridCols/2 or self.whiteInCol[j] == self.gridRows/2:
                        self.setVal(i, j, 1)
                        ret = True
        return ret
    
    def constraint2(self):
        # vertical up
        ret = False
        for i in range(2, self.gridRows):
            for j in range(self.gridCols):
                if self.val[i][j] == 0 and self.val[i-1][j] == self.val[i-2][j]:
                    if self.val[i-1][j] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i-1][j] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        # vertical down
        for i in range(self.gridRows-2):
            for j in range(self.gridCols):
                if self.val[i][j] == 0 and self.val[i+1][j] == self.val[i+2][j]:
                    if self.val[i+1][j] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i+1][j] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        # vertical middle
        for i in range(1, self.gridRows-1):
            for j in range(self.gridCols):
                if self.val[i][j] == 0 and self.val[i-1][j] == self.val[i+1][j]:
                    if self.val[i+1][j] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i+1][j] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        # horizontal left
        for i in range(self.gridRows):
            for j in range(2, self.gridCols):
                if self.val[i][j] == 0 and self.val[i][j-1] == self.val[i][j-2]:
                    if self.val[i][j-1] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i][j-1] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        # horizontal right
        for i in range(self.gridRows):
            for j in range(self.gridCols-2):
                if self.val[i][j] == 0 and self.val[i][j+1] == self.val[i][j+2]:
                    if self.val[i][j+1] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i][j+1] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        # horizontal middle
        for i in range(self.gridRows):
            for j in range(1, self.gridCols-1):
                if self.val[i][j] == 0 and self.val[i][j-1] == self.val[i][j+1]:
                    if self.val[i][j+1] == 1:
                        self.setVal(i, j, 2)
                        ret = True
                    elif self.val[i][j+1] == 2:
                        self.setVal(i, j, 1)
                        ret = True
        return ret


    def dfs_solve(self):
        self.constraint2()
        return

if __name__ == "__main__":

    board = Game()
    board.dfs_solve()
    board.printGrid()