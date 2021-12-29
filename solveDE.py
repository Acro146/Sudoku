from datetime import datetime
import numpy as np
from random import randint
from random import random


class SolveWithDE:

    def __init__(self):
        self.org = list()
        self.board = list()
        self.generation = 30000
        self.p_count = 100
        self.filledList = list()
        self.retain=0.10
        

    def replace(self, filledList):
        myList = [["" for col in range(9)] for row in range(9)]
        for row in range(9):
            for col in range(9):
                if filledList[row][col][0].get() == "":
                    myList[row][col] = 0
                else:
                    myList[row][col] = int(filledList[row][col][0].get())
        return np.array(myList)

    def showResult(self, bo):
        for row in range(9):
            for col in range(9):
                if self.org[row][col] == 0:
                    self.filledList[row][col][1] = "green"
                self.board[row][col].configure(fg=self.filledList[row][col][1])
                self.filledList[row][col][0].set(str(bo[row][col]))

    def isSafe(self, p, row, col, value):
        x = row // 3
        y = col // 3
        board = p.copy()
        board[row][col] = 0
        s_board = board[x * 3:(x + 1) * 3, y * 3:(y + 1) * 3].copy().flatten()

        if (value > 0 and value < 10):
            if value not in board[row]:
                if value not in board.T[col]:
                    if value not in s_board:
                        return True

        return False

    def fitness(self, board):
        sum = 0

        for i in range(9):
            for j in range(9):

                if (self.org[i, j] == 0):
                    if (self.isSafe(board, i, j, board[i][j]) == False):
                        sum += 1

        return sum

    def individual(self):
        board = self.org.copy()

        for i in range(9):
            for j in range(9):

                k = 0
                while (board[i][j] == 0 and k != 100):
                    value = randint(1, 9)

                    if (self.isSafe(board, i, j, value)):
                        board[i][j] = value

                    k = k + 1
                if (board[i][j] == 0):
                    board[i][j] = randint(1, 9)

        return board

    def population(self):
        return [self.individual() for x in range(self.p_count)]

    def grade(self, pop):
        total = [self.fitness(x) for x in pop]
        return (sum(total) / len(pop) * 1.0)

    def resolve(self, pop):
        for individual in pop:
            for i in range(9):
                for j in range(9):
                    k = 0
                    while ((individual[i][j] < 1 or individual[i][j] > 9) and k != 100):
                        value = randint(1, 9)

                        if (self.isSafe(individual, i, j, value)):
                            individual[i, j] = value

                        k = k + 1
                    if (individual[i][j] < 1 or individual[i][j] > 9):
                        individual[i, j] = randint(1, 9)

        return pop

    def evolve(self, pop, k, CR=.009):
        next_generation = []

        for individual in pop:
            p1 = randint(0, len(pop) - 1)
            p2 = randint(0, len(pop) - 1)
            p3 = randint(0, len(pop) - 1)

            while (p1 == p2 or p1 == p3 or p2 == p3):
                p1 = randint(0, len(pop) - 1)
                p2 = randint(0, len(pop) - 1)
                p3 = randint(0, len(pop) - 1)

            v1 = np.array(pop[p1])
            v2 = np.array(pop[p2])
            v3 = np.array(pop[p3])

            difference = v2 - v1
            mutate = v3 + 3 * difference
            trial = np.full((9, 9), 0)

            for i in range(9):
                for j in range(9):
                    if (CR > random()):
                        trial[i][j] = mutate[i][j]
                    else:
                        trial[i][j] = individual[i][j]

            f1 = self.fitness(trial)
            f2 = self.fitness(individual)
            if (f1 < f2):
                next_generation.append(trial)
            else:
                next_generation.append(individual)

        if ((k + 1) % 100 == 0):
            print("resolve !!!!!!!!!!!!!!!")
            next_generation = self.resolve(next_generation)
            
        return next_generation

    
    def solve(self, filledList, board):
        self.org = self.replace(filledList)
        self.filledList = filledList
        self.board = board
        self.start = datetime.now()
        print(self.start)
        p1 = self.population()
        m = 81
        fitest = []
        history = []
        for i in range(self.generation):
            if (i % 100 == 0):
                for ind in p1:
                    x = self.fitness(ind)
                    if (x < m):
                        m = x
                        fitest = ind
                print("-----------")
                print(m)
                print("-----------")
                if (m == 0):
                    print(" we end in "+str(i)+" iteration")
                    break
                
            if (i % 1000 == 0):
                print("we in iteration " + str(i))
                if m in history:

                    graded = [(self.fitness(x), x) for x in p1]
                    graded.sort(key=lambda x: x[0])
                    graded = [x[1] for x in graded]
                    retain_length = int(len(graded) * self.retain)
                    parents = graded[:retain_length]
                    
                    p1 = self.population()
                    
                    for s in range(retain_length):
                        p1[randint(0, self.p_count - 1)] = parents[s]
                        history = []
                else:
                    history.append(m)
            p1 = self.evolve(p1,i)
            print(self.grade(p1))

            

                

        stop = datetime.now()
        time = stop - self.start
        print(time)

        

        self.showResult(fitest)