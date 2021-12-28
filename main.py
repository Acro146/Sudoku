import tkinter as tk
from tkinter import OptionMenu, messagebox
from solveBT import SolveWithBT
from solveDE import SolveWithDE
from validation import Validation
from boards import BoardLevels

root = tk.Tk()
root.geometry('730x515')
root.resizable(0, 0)
colors = ["black", "white smoke", "#bcbcbc"]
root.configure(bg = colors[1])

boardList = None

class Interface():
 
    def __init__(self, window):

        self.window = window
        window.title("Sudoku Solver")
        font = ('Arial', 22)
        self.board = [["" for col in range(9)] for row in range(9)]
        self.filledBoard = [[[tk.StringVar(root), "black"] for col in range(9)] for row in range(9)]
        [[self.filledBoard[row][col][0].set("") for col in range(9)] for row in range(9)]

        for row in range(9):
            for col in range(9):
                # Change color of cells depending on position in grid
                if (row < 3 or row > 5) and (col < 3 or col > 5):
                    color = colors[1]
                elif (row >= 3 and row < 6) and (col >=3 and col < 6):
                    color = colors[1]
                else:
                    color = colors[2]
                    
                # Make each cell of grid a entry box and store each user entry into the filledBoard 2D list
                self.board[row][col] = tk.Entry(window, width = 4, font = font, bg = color, fg = self.filledBoard[row][col][1], borderwidth = 4,
                                          highlightthickness = 1, highlightbackground = colors[0], justify='center', relief='flat',
                                          textvariable = self.filledBoard[row][col][0])

                self.board[row][col].bind('<FocusIn>', self.gridChecker)
                self.board[row][col].bind('<Motion>', self.gridChecker)
                self.board[row][col].bind('<KeyRelease>', self.gridChecker)
                self.board[row][col].grid(row = row+1, column = col, padx = (25, 0) if col == 0 else (0, 0), pady = (10, 0) if row == 0 else (0, 0))

        self.menu = tk.StringVar()
        self.menu.set("Select Level")

        dropList = OptionMenu(window, self.menu, *BoardLevels.getNames, command=self.writeBoard)
        dropList.grid(column= 3, columnspan = 3, row=0, pady=2, sticky="ew")

        solveWithBT = tk.Button(window, text = 'Solve with Backtracking', width=20, relief='raised', borderwidth = 1, font = ('Arial', 11, 'bold'), command = self.SolveBT)
        solveWithBT.grid(column= 1, columnspan = 3,row=11, pady=12)

        solveWithDE = tk.Button(window, text = 'Solve with DE', width=12, relief='raised', borderwidth = 1, font = ('Arial', 11, 'bold'), command = self.SolveDE)
        solveWithDE.grid(column= 4, columnspan = 2,row=11, pady=12)

        clear = tk.Button(window, text = 'Clear', width=6, bg = colors[1], relief='raised', borderwidth = 1, font = ('Arial', 11, 'bold'),fg = 'red', command = self.Clear)
        clear.grid(column = 6, columnspan = 2,row=11, pady= 12)
        

    def gridChecker(self, event):
        for row in range(9):
            for col in range(9):
                self.board[row][col].configure(fg = self.filledBoard[row][col][1])
                if self.filledBoard[row][col][0].get() not in ["1","2","3","4","5","6","7","8","9"]:
                    self.filledBoard[row][col][0].set("")

    def writeBoard(self, level):

        if level == "Easy":
            boardList = BoardLevels.easy
        elif level == "Medium":
            boardList = BoardLevels.medium
        elif level == "Hard":
            boardList = BoardLevels.hard
        else:
            boardList = BoardLevels.evil

        for row in range(9):
            for col in range(9):
                self.filledBoard[row][col][1] = "black"
                self.board[row][col].configure(fg = self.filledBoard[row][col][1])

        [[self.filledBoard[row][col][0].set(boardList[row][col]) for col in range(9)] for row in range(9)]


    def validation(self):
        val = Validation(self.filledBoard)
        if (val.EmptyCells()):
            messagebox.showinfo("Error", "There must be at least 17 given numbers")
            return False
        
        val_Board = val.validateBoard()
        if(val_Board[0]):
            messagebox.showinfo("Error", "There is a redundant number in " + val_Board[1] + ": " + str(val_Board[2]) + ".")
            return False
        return True

    def SolveDE(self):
        if(self.validation()):
            solver = SolveWithDE()
            solver.solve(self.filledBoard, self.board)
    
    def SolveBT(self):
        if(self.validation()):
            solver = SolveWithBT()
            solver.solve(self.filledBoard, self.board)

    # Function to clear board (called by clear button) 
    def Clear(self):
        [[self.filledBoard[row][col][0].set("") for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                self.filledBoard[row][col][1] = "black"
        
def main():
    Interface(root)
    root.mainloop()

if __name__ == "__main__":
    main()