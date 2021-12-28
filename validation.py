class Validation():

    def __init__(self, filledList):
        self.__filledBoard = filledList

    def EmptyCells(self):
        empty = 0
        for row in range(9):
           for col in range(9):
              if(self.__filledBoard[row][col][0].get() == ""):
                  empty += 1
        return empty > 64

    def __validateRows(self):
        for row in range(9):
            for col1 in range(9):
                for col2 in range(9):
                    if col1 == col2 or self.__filledBoard[row][col1][0].get() == "":
                        continue
                    if self.__filledBoard[row][col1][0].get() == self.__filledBoard[row][col2][0].get():
                        return (True, "Row", row+1)
        return (False, "", 0)

    def __validateColumns(self):
        for col in range(9):
            for row1 in range(9):
                for row2 in range(9):
                    if row1 == row2 or self.__filledBoard[row1][col][0].get() == "":
                        continue
                    if self.__filledBoard[row1][col][0].get() == self.__filledBoard[row2][col][0].get():
                        return (True, "Column", col+1)
        return (False, "", 0)

    def __validateBoxs(self):
        for col in range(0, 9, 3):
            for row in range(0, 9, 3):
                box_x = col // 3
                box_y = row // 3
                for i in range(box_y*3, box_y*3 + 3):
                    for j in range(box_x * 3, box_x*3 + 3):
                        for ii in range(box_y*3, box_y*3 + 3):
                            for jj in range(box_x * 3, box_x*3 + 3):
                                if i == ii or j == jj or self.__filledBoard[i][j][0].get() == "":
                                    continue
                                if self.__filledBoard[i][j][0].get() == self.__filledBoard[ii][jj][0].get():
                                    return (True, "Box", ((box_y * 3) + box_x+1))
        return (False, "", 0)


    def validateBoard(self):

        checkRows = self.__validateRows()
        if(checkRows[0]):
            return checkRows

        checkColumns = self.__validateColumns()
        if(checkColumns[0]):
            return checkColumns
       
        checkBoxs = self.__validateBoxs()
        if(checkBoxs[0]):
            return checkBoxs

        return (False, "", 0)