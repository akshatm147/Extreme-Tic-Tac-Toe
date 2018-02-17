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
