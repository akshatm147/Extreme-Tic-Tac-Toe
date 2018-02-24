# !/usr/bin/python

################################
# AI Assignment 1: Tic-Tac-Toe #
################################

################################
#           Team - 18          #
################################

################################
#            D M G             #
################################

import copy
import random
import time

class Player():

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

    def checkAllowedBlocks(self, prevMove, BlockStatus):

        if prevMove[0] < 0 and prevMove[1] < 0:
            return self.allValidList

        allowedBlocks = self.validBlocks[prevMove[0] % 4][prevMove[1] % 4]
        finalAllowedBlocks = []

        for i in allowedBlocks:
            if BlockStatus[i[0]][i[1]] == 0:
                finalAllowedBlocks.append(i)

        if len(finalAllowedBlocks) == 0:
            for i in self.allValidList:
                if BlockStatus[i[0]][i[1]] == 0:
                    finalAllowedBlocks.append(i)

        return finalAllowedBlocks

    def checkAllowedMarkers(self, block):

        allowed = []

        for i in range(4):
            for j in range(4):
                if block[i][j] == 0:
                    allowed.append((i, j))

        return allowed

    def getAllowedMoves(self, currentBoard, currentBlockStatus, prevMove):

        moveList = []

        for allowedBlock in self.checkAllowedBlocks(prevMove, currentBlockStatus):
            moveList += [ (4 * allowedBlock[0] + move[0], 4 * allowedBlock[1] + move[1]) for move in self.checkAllowedMarkers(currentBoard[allowedBlock[0]][allowedBlock[1]]) ]

        return moveList

    def getBlockStatus(self, block):

        for i in range(4):
            if block[i][0] == block[i][1] == block[i][2] == block[i][3] and block[i][1] in (1,
                                                                                            2):
                return block[i][1]
            if block[0][i] == block[1][i] == block[2][i] == block[3][i] and block[1][i] in (1,
                                                                                            2):
                return block[1][i]

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

        if not len(self.checkAllowedMarkers(block)):
            return 3

        return 0

    def count(self, i, j, block):

        row_flag = 1
        col_flag = 1
        flagd1 = 1   # flag for diamond-1 win
        flagd2 = 1   # flag for diamond-2 win
        flagd3 = 1   # flag for diamond-3 win
        flagd4 = 1   # flag for diamond-4 win
        self.score = 0
        new_block = copy.deepcopy(block)

        for row in range(4):
            if new_block[i][row] == 2:
                row_flag = 0

        if row_flag:
            for row in range(4):
                if new_block[i][row] == 1:
                    self.score += 1

        for col in range(4):
            if new_block[col][j] == 2:
                col_flag = 0

        if col_flag:
            for col in range(4):
                if new_block[col][j] == 1:
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

    def getBlockScore(self, block):

        block = tuple([ tuple(block[i]) for i in range(4) ])

        if block not in self.heuristicDict:
            blockStat = self.getBlockStatus(block)
            if blockStat == 1:
                self.heuristicDict[block] = 100.0
            elif blockStat == 2:
                self.heuristicDict[block] = 0.1
            elif blockStat == 3:
                self.heuristicDict[block] = 0.0
            else:
                best = -1000
                moves = self.checkAllowedMarkers(block)
                playBlock = [ list(block[i]) for i in range(4) ]
                opnplayBlock = [ list(block[i]) for i in range(4) ]
                for i in range(4):
                    for j in range(4):
                        if opnplayBlock[i][j]:
                            opnplayBlock[i][j] = 3 - opnplayBlock[i][j]

                for move in moves:
                    ans = 1.0 + self.count(move[0], move[1], playBlock) - self.count(move[0], move[1], opnplayBlock)
                    if ans > best:
                        wePlayList = []
                        best = 1.0 + self.count(move[0], move[1], playBlock) - self.count(move[0], move[1], opnplayBlock)
                        wePlayList.append((move[0], move[1]))
                    else:
                        if ans == best:
                            wePlayList.append((move[0], move[1]))
                    self.heuristicDict[block] = best

        return self.heuristicDict[block]

    def lineScore(self, line, blockProb, revBlockProb, currentBlockStatus):

        if 3 in [ currentBlockStatus[x[0]][x[1]] for x in line ]:
            return 0

        positiveScore = [ blockProb[x[0]][x[1]] for x in line ]
        negativeScore = [ revBlockProb[x[0]][x[1]] for x in line ]
        pos = 1
        neg = 1

        for i in positiveScore:
            pos = pos * i

        for i in negativeScore:
            neg = neg * i

        return pos - neg

    def getDiamondScore(self, blockProb, revBlockProb, currentBlockStatus):

        diamond = [ [0 for _ in range(4)] for _ in range(4) ]

        diamond[0] = [(0, 1), (1, 0), (1, 2), (2, 1)]
        diamond[1] = [(0, 2), (1, 1), (2, 2), (1, 3)]
        diamond[2] = [(1, 1), (2, 0), (3, 1), (2, 2)]
        diamond[3] = [(1, 2), (2, 1), (3, 2), (2, 3)]

        dScore = 0

        for k in range(4):
            if 3 in [ currentBlockStatus[i][j] for (i,j) in diamond[k] ]:
                dScore += 0

        if dScore == 0:
            return 0

        positiveScore = []
        negativeScore = []

        for k in range(4):
            positiveScore.append(blockProb[i][j] for (i, j) in diamond[k])
            negativeScore.append(revBlockProb[i][j] for (i, j) in diamond[k])

        pos = 1
        neg = 1

        for i in positiveScore:
            pos *= i
        for i in negativeScore:
            neg *= i

        return pos - neg

    def getBoardScore(self, currentBoard, currentBlockStatus):

        terminalStat, terminalScore = self.terminalCheck(currentBoard, currentBlockStatus)

        if terminalStat:
            return terminalScore

        revCurrenBoard = copy.deepcopy(currentBoard)

        for row in range(4):
            for col in range(4):
                for i in range(4):
                    for j in range(4):
                        if revCurrenBoard[row][col][i][j]:
                            revCurrenBoard[row][col][i][j] = 3 - revCurrenBoard[row][col][i][j]

        blockProb = [ [0] * 4 for i in range(4) ]
        revBlockProb = [ [0] * 4 for i in range(4) ]

        for i in range(4):
            for j in range(4):
                blockProb[i][j] = self.getBlockScore(currentBoard[i][j])
                revBlockProb[i][j] = self.getBlockScore(revCurrenBoard[i][j])

        boardScore = []

        for i in range(4):
            line = [ (i, j) for j in range(4) ]
            boardScore.append(self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))
            line = [ (j, i) for j in range(4) ]
            boardScore.append(self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))

        boardScore.append(self.getDiamondScore(blockProb, revBlockProb, currentBlockStatus))

        if 100000000 in boardScore:
            return 100000000
        if 1e-05 in boardScore:
            return -100000000

        return sum(boardScore)

    def move(self, currentBoard, oldMove, flag):

        formattedBoard = [ [ [ [0] * 4 for i in range(4) ] for j in range(4) ] for j in range(4) ]
        formattedBlockStatus = [ [0] * 4 for i in range(4) ]
        copyBlock = [ [0] * 4 for i in range(4) ]

        for i in range(16):
            for j in range(16):
                if currentBoard.board_status[i][j] == flag:
                    formattedBoard[i / 4][j / 4][i % 4][j % 4] = 1
                elif currentBoard.board_status[i][j] == '-':
                    formattedBoard[i / 4][j / 4][i % 4][j % 4] = 0
                else:
                    formattedBoard[i / 4][j / 4][i % 4][j % 4] = 2

        for i in range(4):
            for j in range(4):
                if currentBoard.block_status[i][j] == flag:
                    formattedBlockStatus[i][j] = 1
                elif currentBoard.block_status[i][j] == '-':
                    formattedBlockStatus[i][j] = 0
                elif currentBoard.block_status[i][j] == 'd':
                    formattedBlockStatus[i][j] = 3
                else:
                    formattedBlockStatus[i][j] = 2

        if oldMove[0] < 0 or oldMove[1] < 0:
            uselessScore, nextMove, retDepth = 0, (random.randint(0, 15), random.randint(0, 15)), 0
            depth = 0
        else:
            depth = 3
            uselessScore, nextMove, retDepth = self.alphaBetaPruning(formattedBoard, formattedBlockStatus, -1000000000, 1000000000, True, oldMove, depth)

        return nextMove

    def terminalCheck(self, currentBoard, currentBlockStatus):

        terminalStat = self.getBlockStatus(currentBlockStatus)

        if terminalStat == 0:
            return (False, 0)
        if terminalStat == 1:
            return (True, 100000000)
        if terminalStat == 2:
            return (True, -100000000)

        blockCount = 0
        midCount = 0

        for i in range(4):
            for j in range(4):
                if currentBlockStatus[i][j] in (1, 2):
                    blockCount += 3 - 2 * currentBlockStatus[i][j]

        return (True, blockCount)

    def alphaBetaPruning(self, currentBoard, currentBlockStatus, alpha, beta, flag, prevMove, depth):

        tempBoard = copy.deepcopy(currentBoard)
        tempBlockStatus = copy.deepcopy(currentBlockStatus)
        terminalStat, terminalScore = self.terminalCheck(currentBoard, currentBlockStatus)

        if terminalStat:
            return (terminalScore, (), 0)
        if depth <= 0:
            return (self.getBoardScore(currentBoard, currentBlockStatus), (), 0)

        possibMoves = self.getAllowedMoves(currentBoard, currentBlockStatus, prevMove)
        random.shuffle(possibMoves)
        bestMove = ()
        bestDepth = 100

        if flag:
            v = -1000000000
            for move in possibMoves:
                tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 1
                tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
                childScore, childBest, childDepth = self.alphaBetaPruning(tempBoard, tempBlockStatus, alpha, beta, not flag, move, depth - 1)
                if childScore >= v:
                    if v < childScore or bestDepth > childDepth:
                        v = childScore
                        bestMove = move
                        bestDepth = childDepth
                alpha = max(alpha, v)
                tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 0
                tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
                if alpha >= beta:
                    break

            return (v, bestMove, bestDepth + 1)

        v = 1000000000
        for move in possibMoves:
            tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 2
            tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
            childScore, childBest, childDepth = self.alphaBetaPruning(tempBoard, tempBlockStatus, alpha, beta, not flag, move, depth - 1)
            if childScore <= v:
                if v > childScore or bestDepth > childDepth:
                    v = childScore
                    bestMove = move
                    bestDepth = childDepth
            beta = min(beta, v)
            tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 0
            tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
            if alpha >= beta:
                break

        return (v, bestMove, bestDepth + 1)
