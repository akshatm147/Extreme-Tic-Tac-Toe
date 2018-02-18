# !/usr/bin/python

################################
# AI Assignment 1: Tic-Tac-Toe #
################################

from __future__ import print_function
import sys
import random
import signal
import time
import copy

class Team18():

    def __init__(self):

        self.validBlocks = [ [ 0 for i in range(4) ] for j in range(4) ]
        self.validBlocks[0][0] = ((0, 0), )
        self.validBlocks[0][1] = ((0, 1), )
        self.validBlocks[0][2] = ((0, 2), )
        self.validBlocks[0][3] = ((0, 3), )
        self.validBlocks[1][0] = ((1, 0), )
        self.validBlocks[1][1] = ((1, 1), )
        self.validBlocks[1][2] = ((1, 2), )
        self.validBlocks[1][3] = ((1, 3), )
        self.validBlocks[2][0] = ((2, 0), )
        self.validBlocks[2][1] = ((2, 1), )
        self.validBlocks[2][2] = ((2, 2), )
        self.validBlocks[2][3] = ((2, 3), )
        self.validBlocks[3][0] = ((3, 0), )
        self.validBlocks[3][1] = ((3, 1), )
        self.validBlocks[3][2] = ((3, 2), )
        self.validBlocks[3][3] = ((3, 3), )
        self.allValidList = ((0, 0),
                            (0, 1),
                            (0, 2),
                            (0, 3),
                            (1, 0),
                            (1, 1),
                            (1, 2),
                            (1, 3),
                            (2, 0),
                            (2, 1),
                            (2, 2),
                            (2, 3),
                            (3, 0),
                            (3, 1),
                            (3, 2),
                            (3, 3))
        self.heuristicDict = {}


        def checkAllowedBlocks(self, prevMove, blockStatus):
            # Returns the valid blocks allowed given the previous move

            if prevMove[0]<0 or prevMove[1]<0:
                return self.allValidList

            allowedBlocks = self.validBlocks[prevMove[0] % 4][prevMove[1] % 4]
            allowedCells = []

            for i in allowedBlocks:
                if blockStatus[i[0]][i[1]] == 0:
                    allowedCells.append(i)

            if len(allowedCells) == 0:
                if i in self.allValidList:
                    if blockStatus[i[0]][i[1]] == 0:
                        allowedCells.append(i)

            return allowedCells


        def checkAllowedMarkers(self, block):
            # Returns all the valid cells of a block which the player can make a move on

            allowed = []

            for i in range(4):
                for j in range(4):
                    if block[i][j] == 0:
                        allowed.append((i, j))

            return allowed


        def getAllowedMoves(self, currentBoardStatus, currentBlockStatus, prevMove):
            # Returns the set of all the possible moves the player has, given the previous move and the
            # current block and board status

            possibleMoves = []

            for allowedBlock in self.checkAllowedBlocks(prevMove, currentBlockStatus):
                possibleMoves += [ (4 * allowedBlock[0] + move[0], 4 * allowedBlock[1] + move[1] ) for move in self.checkAllowedMarkers(currentBoardStatus[allowedBlock[0]][allowedBlock[1]]) ]

            return possibleMoves


        def getBlockStatus(self, block):
            # Returns the status of the 4X4 block if that particular position block in the board has been won

            # 1 -> x/o (depending on whether P1 or P2)
            # 2 -> o/x
            # 3 -> d

            for i in range(4):
                if block[i][0] == block[i][1] == block[i][2] == block[i][3] and block[i][0] in (1,2):
                    # Checking for horizontal pattern in the block
                    return block[i][0]
                if block[0][i] == block[1][i] == block[2][i] == block[3][i] and block[0][i] in (1,2):
                    # Checking for vertical pattern in the block
                    return block[0][i]

            # Checking for diagonals
            if block[0][0] == block[1][1] == block[2][2] == block[3][3] and block[0][0] in (1,2):
                return block[0][0]
            if block[0][3] == block[1][2] == block[2][1] == block[3][0] and block[1][2] in (1,2):
                return block[0][3]

            # Checking for diamonds
            # diamond-1
            if block[0][1] == block[1][0] == block[2][1] == block[1][1] and block[0][1] in (1,2):
                return block[0][1]
            # diamond-2
            if block[0][2] == block[1][1] == block[2][2] == block[1][3] and block[0][2] in (1,2):
                return block[0][2]
            # diamond-3
            if block[1][1] == block[2][0] == block[3][1] == block[2][2] and block[1][1] in (1,2):
                return block[1][1]
            # diamond-4
            if block[1][2] == block[2][1] == block[3][2] == block[2][3] and block[1][2] in (1,2):
                return block[1][2]

            # If case of draw
            if not len(self.checkAllowedMarkers(block)):
                return 3

        def scoreCount(self, i, j, block):

            flagr = 1   # flag for row win
            flagc = 1   # flag for column win
            flagpd = 1  # flag for primary diagonal win
            flagnd = 1  # flag for non-primary diagonal win
            flagd1 = 1   # flag for diamond-1 win
            flagd2 = 1   # flag for diamond-2 win
            flagd3 = 1   # flag for diamond-3 win
            flagd4 = 1   # flag for diamond-4 win

            self.score = 0

            new_block = copy.deepcopy(block)

            for row in range(4):
                if new_block[i][row] == 2:
                    flagr = 0
            if flagr:
                for row in range(4):
                    if new_block[i][row] == 1:
                        self.score += 1

            for col in range(4):
                if new_block[col][j] == 2:
                    flagc = 0
            if flagc:
                for col in range(4):
                    if new_block[col][j]:
                        self.score += 1

            if (i,j) in [(0,0), (1,1), (2,2), (3,3)]:
                for diag in range(4):
                    if new_block[diag][diag] == 2:
                        flagpd = 0
                if flagpd:
                    for diag in range(4):
                        if new_block[diag][diag] == 1:
                            self.score += 1

            if (i,j) in [(0,3), (1,2), (2,1), (3,0)]:
                for diag in range(4):
                    if new_block[diag][3 - diag] == 2:
                        flagnd = 0
                if flagnd:
                    for diag in range(4):
                        if new_block[diag][3 - diag] == 1:
                            self.score += 1

            if (i,j) in [(0,1), (1,0), (2,1), (1,1)]:
                if new_block[0][1] == 2:
                    flagd1 = 0
                if new_block[1][0] == 2:
                    flagd1 = 0
                if new_block[2][1] == 2:
                    flagd1 = 0
                if new_block[1][1] == 2:
                    flagd1 = 0
                if flagd1:
                    if new_block[0][1] == 1:
                        self.score += 1
                    if new_block[1][0] == 1:
                        self.score += 1
                    if new_block[2][1] == 1:
                        self.score += 1
                    if new_block[1][1] == 1:
                        self.score += 1

            if (i,j) in [(0,2), (1,1), (2,2), (1,3)]:
                if new_block[0][2] == 2:
                    flagd2 = 0
                if new_block[1][1] == 2:
                    flagd2 = 0
                if new_block[2][2] == 2:
                    flagd2 = 0
                if new_block[1][3] == 2:
                    flagd2 = 0
                if flagd2:
                    if new_block[0][2] == 1:
                        self.score += 1
                    if new_block[1][1] == 1:
                        self.score += 1
                    if new_block[2][2] == 1:
                        self.score += 1
                    if new_block[1][3] == 1:
                        self.score += 1

            if (i,j) in [(1,1), (2,0), (3,1), (2,2)]:
                if new_block[1][1] == 2:
                    flagd3 = 0
                if new_block[2][0] == 2:
                    flagd3 = 0
                if new_block[3][1] == 2:
                    flagd3 = 0
                if new_block[2][2] == 2:
                    flagd3 = 0
                if flagd3:
                    if new_block[1][1] == 1:
                        self.score += 1
                    if new_block[2][0] == 1:
                        self.score += 1
                    if new_block[3][1] == 1:
                        self.score += 1
                    if new_block[2][2] == 1:
                        self.score += 1

            if (i,j) in [(1,2), (2,1), (3,2), (2,3)]:
                if new_block[1][2] == 2:
                    flagd4 = 0
                if new_block[2][1] == 2:
                    flagd4 = 0
                if new_block[3][2] == 2:
                    flagd4 = 0
                if new_block[2][3] == 2:
                    flagd4 = 0
                if flagd4:
                    if new_block[1][2] == 1:
                        self.score += 1
                    if new_block[2][1] == 1:
                        self.score += 1
                    if new_block[3][2] == 1:
                        self.score += 1
                    if new_block[2][3] == 1:
                        self.score += 1

            return self.score