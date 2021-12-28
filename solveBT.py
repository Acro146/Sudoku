class SolveWithBT():

    boardProperties = list()
#    it = 0
    def solve(self ,filledBoard ,board):    
        self.boardProperties = board
        self.backtrack(filledBoard)
#        print("\n Solved in " + str(self.it) + " iterations") 
    def backtrack(self, filledBoard):
#        self.it += 1
        ceil = self.nextEmpty(filledBoard)
        if not ceil:
            return True
        else:
            row, col = ceil

        for i in range(1, 10):
            if self.valid(filledBoard, i, (row, col)):

                filledBoard[row][col][1] = "green"
                self.boardProperties[row][col].configure(fg = filledBoard[row][col][1])
                filledBoard[row][col][0].set(str(i)) 
                if self.backtrack(filledBoard):
                    return True
                filledBoard[row][col][0].set("")
        return False

    def valid(self, board, num, pos):
        for i in range(9):
            if board[pos[0]][i][0].get() == str(num) and pos[1] != i:
                return False

        for i in range(9):
            if board[i][pos[1]][0].get() == str(num) and pos[0] != i:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if board[i][j][0].get() == str(num) and (i,j) != pos:
                    return False

        return True

    def nextEmpty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j][0].get() == "":
                    return (i, j) 
        return None