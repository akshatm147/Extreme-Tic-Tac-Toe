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

            allowed = []

            for i in range(4):
                for j in range(4):
                    if block[i][j] == 0:
                        allowed.append((i, j))

            return allowed


        def getAllowedMoves(self, currentBoardStatus, currentBlockStatus, prevMove):

            possibleMoves = []

            for allowedBlock in self.checkAllowedBlocks(prevMove, currentBlockStatus):
                possibleMoves += [ (4 * allowedBlock[0] + move[0], 4 * allowedBlock[1] + move[1] ) for move in self.checkAllowedMarkers(currentBoardStatus[allowedBlock[0]][allowedBlock[1]]) ]

            return possibleMoves


        def getBlockStatus(self, block):

            for i in range(4):
