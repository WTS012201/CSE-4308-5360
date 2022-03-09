#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

import copy
import random
import sys

INFINITY = 9999999

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.piece_count = 0
        self.gameFile = None
        random.seed()

        self.depth = 1
    # total the number of pieces already played
    def checkPieceCount(self):
        self.piece_count = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print (' -----------------')
        for i in range(6):
            print (' | ', end="")
            for j in range(7):
                print('%d ' % self.gameBoard[i][j], end="")
            print ('| ')
        print (' -----------------')

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested col
    def playPiece(self, col):
        if not self.gameBoard[0][col]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][col]:
                    self.gameBoard[i][col] = self.currentTurn
                    self.piece_count += 1
                    return 1

    # The AI section. Currently plays randomly.
    # def aiPlay(self):
    #     randcol = random.randrange(0,7)
    #     result = self.playPiece(randcol)
    #     if not result:
    #         self.aiPlay()
    #     else:
    #         print('\n\nmove %d: Player %d, col %d\n' % (self.piece_count, self.currentTurn, randcol+1))
    #         if self.currentTurn == 1:
    #             self.currentTurn = 2
    #         elif self.currentTurn == 2:
    #             self.currentTurn = 1

    # Place the current player's piece in the requested col
    def playPiece(self, col):
        if not self.gameBoard[0][col]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][col]:
                    self.gameBoard[i][col] = self.currentTurn
                    self.piece_count += 1
                    return 1
    
    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0
        self.player2Score = 0

        # Check horizontally
        for row in self.gameBoard:
            # Check player A
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player B
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player A
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player B
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player A
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player B
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1


    #-----------------------------------ADDED-----------------------------------
    def aiPlay(self):
        col = self.minimax(int(self.depth))
        if self.playPiece(col):
            self.nextTurn()

    def nextTurn(self):
        if self.currentTurn == 1:
            self.currentTurn = 2
        elif self.currentTurn == 2:
            self.currentTurn = 1
            
    def getPieceCount(self):
        return sum(1 for i in self.gameBoard for j in i if j)

    def minimax(self, depth):
        curr = copy.deepcopy(self.gameBoard)
        vals = {}
        for col in range(7):
            if self.playPiece(col):
                if self.piece_count == 42 or not self.depth:
                    self.gameBoard = copy.deepcopy(curr)
                    return col
                else:
                    val = self.min_val(self.gameBoard, -INFINITY, INFINITY, depth - 1)
                    vals[col] = val
                    self.gameBoard = copy.deepcopy(curr)

        max_vals = max([i for i in vals.values()])
        for col in range(7):
            if col in vals and vals[col] == max_vals:
                vals.clear()
                return col

    def min_val(self, curr, alpha, beta, depth):
        val = -INFINITY
        children = []
        
        parent = copy.deepcopy(curr)
        if self.currentTurn == 1:
            nextTurn = 2
        elif self.currentTurn == 2:
            nextTurn = 1
        for i in range(7):
            curr = None
            if not self.gameBoard[0][i]:
                for j in range(5, -1, -1):
                    if not self.gameBoard[j][i]:
                        self.gameBoard[j][i] = nextTurn
                        self.piece_count += 1
                        curr = 1
            if curr:
                children.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent)

        if not children or not depth:
            self.countScore()
            return self.evaluate(self.gameBoard)
        else:
            for child in children:
                self.gameboard = copy.deepcopy(child)
                val = min(val, self.max_val(child, alpha, beta, depth - 1))
                if val <= alpha:
                    return val
                beta = min(beta, val)
        return val

    def max_val(self, curr, alpha, beta, depth):
        val = -INFINITY
        children = []
        
        parent = copy.deepcopy(curr)
        for col in range(7):
            curr = self.playPiece(col)
            if curr:
                children.append(self.gameBoard)
                self.gameBoard = copy.deepcopy(parent)

        if not children or not depth:
            self.countScore()
            return self.evaluate(self.gameBoard)
        else:
            for child in children:
                self.gameBoard = copy.deepcopy(child)
                val = max(val, self.min_val(child, alpha, beta, depth - 1))
                if val >= beta:
                    return val
                alpha = max(alpha, val)
            return val

    def evaluate(self, curr):
        if self.currentTurn == 1:
            nextTurn = 2
        elif self.currentTurn == 2:
            nextTurn = 1
            
        currVal = self.check(curr, self.currentTurn)
        nextVal = self.check(curr, nextTurn)
        
        return currVal - nextVal

    def check(self, curr, turn):
        total = 0
        for row in range(6):
            for col in range(7):
                if curr[row][col] == turn:
                    for amount in range(1,5):
                        total += self.checkHorizontal(curr, amount, row, col)
                        total += self.checkVertical(curr, amount, row, col)
                        total += self.checkDiag(curr, amount, row, col)
        return total

    def checkHorizontal(self, curr, amount, row, col):
        total = 0
        for j in range(col, 7):
            if curr[row][j] == curr[row][col]:
                total += 1
            else:
                break
        if total >= amount:
            return amount
        else:
            return 0

    def checkVertical(self, curr, amount, row, col):
        total = 0
        for row in range(row, 6):
            if curr[row][col] == curr[row][col]:
                total += 1
            else:
                break
        if total >= amount:
            return amount
        else:
            return 0

    def checkDiag(self, curr, amount, row, col):
        total = 0
        j = col
        n = 0
        for i in range(row, 6):
            if j > 6:
                break
            elif curr[i][j] == curr[row][col]:
                n += 1
            else:
                break
            j += 1
        if n >= amount:
            total += 1
        j = col
        n = 0
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif curr[i][j] == curr[row][col]:
                n += 1
            else:
                break
            j += 1
        if n >= amount:
            total += 1
        return total
#-----------------------------------ADDED-----------------------------------
