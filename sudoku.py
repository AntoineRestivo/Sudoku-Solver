from z3 import *
import random
from random import sample
import numpy as np
import copy

class sudoku:

    def __init__(self):
        self.base = 3
        self.side = 3**2
        G = [[Int('a_%s_%s' % (i+1, j+1)) for j in range(self.side)]
            for i in range(self.side)]
        self.G = G

    def pattern(self, r, c):
        return (self.base*(r%self.base)+r//self.base+c)%self.side

    def shuffle(self, s):
        return sample(s,len(s))

    def grid(self):
        rBase = range(self.base)
        rows  = [ g*self.base + r for g in self.shuffle(rBase) for r in self.shuffle(rBase) ]
        cols  = [ g*self.base + c for g in self.shuffle(rBase) for c in self.shuffle(rBase) ]
        nums  = self.shuffle(range(1,self.base*self.base+1))
        return [[nums[self.pattern(r,c)] for c in cols] for r in rows]

    def elimVar(self):
        Gi = self.grid()
        G = self.G
        nbIter = random.randint(20, 50)
        index1 = []
        index2 = []

        for i in range(nbIter):
            index1.append(random.randint(0, 8))
            index2.append(random.randint(0, 8))

        Gi[self.base+1][self.base+1] = ' '
        for i in range(len(index1)):
            Gi[index1[i]][index2[i]] = ' '
            Gi[index2[i]][index1[i]] = ' '

        Gf = copy.deepcopy(Gi)
        for i in range(self.side):
            for j in range(self.side):
                if Gi[i][j] == ' ':
                    Gf[i][j] = 0

        for i in range(len(Gi)):
            for j in range(len(Gi)):
                if Gi[i][j] == ' ':
                    Gi[i][j] = G[i][j]

        return Gi, Gf

    def rules(self, grid, Gf):
        solution = copy.deepcopy(Gf)
        s = Solver()

        for i in range(len(grid)):
            for j in range(len(grid)):
                if type(grid[i][j]) == z3.z3.ArithRef:
                    for k in range(len(grid)):
                        if k != j:
                            s.add(grid[i][j] != grid[i][k])
                        if k!= i:
                            s.add(grid[i][j] != grid[k][j])
                    s.add(1 <= grid[i][j])
                    s.add(grid[i][j] <= 9)

        if s.check() == sat:
            for i in range(len(Gf)):
                for j in range(len(Gf)):
                    if type(grid[i][j]) == z3.z3.ArithRef:
                        Gf[i][j] = s.model()[grid[i][j]].as_long()

            return Gf

    def frame(self, line):
        return line[0]+line[5:9].join([line[1:5]*(self.base-1)]*self.base)+line[9:13]

    def prettyPrint(self, Gf):
        line0 = S.frame("╔═══╤═══╦═══╗")
        line1  = S.frame("║ . │ . ║ . ║")
        line2  = S.frame("╟───┼───╫───╢")
        line3  = S.frame("╠═══╪═══╬═══╣")
        line4  = S.frame("╚═══╧═══╩═══╝")
        symbol = " 1234567890"
        nums   = nums   = [ [""]+[symbol[n] for n in row] for row in Gf ]

        print(line0)
        for r in range(1, self.side+1):
            print("".join(n+s for n,s in zip(nums[r-1],line1.split("."))))
            print([line2,line3,line4][(r%self.side==0)+(r%self.base==0)])


S = sudoku()
Gi, Gf = S.elimVar()
print('Sudoku puzzle:')
S.prettyPrint(Gf)
sol = S.rules(Gi, Gf)
print('solution:')
S.prettyPrint(sol)
