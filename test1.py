import random
from time import time

class Team19:

    def __init__(self):
        self.initialDepth = 1
        self.maxdepth = 400
        self.sign = ' '
        self.opposite_sign = ' '
        self.timeLmt = 1
        self.INT_MAX = 100000000000
        self.INT_MIN = -100000000000
        self.factor = 7
        self.bonus = [2, 2]
        self.board_wins = 0
        self.old_board_wins = 0
        self.board_opp_wins = 0
        self.old_opp_wins = 0

    def iterative_search(self, board, old_move, flag):
        output_move = random.choice(board.find_valid_move_cells(old_move))
        for deep in range(self.initialDepth, self.maxdepth):
            valid_moves = board.find_valid_move_cells(old_move)
            maxval = self.INT_MIN
            max_set = valid_moves
            for move in valid_moves:
                board.update(old_move, move, self.sign)
                tempval = self.minimax(board, move, deep, False, self.INT_MIN, self.INT_MAX)
                board.board_status[move[0]][move[1]] = '-'
                board.block_status[move[0] / 4][move[1] / 4] = '-'
                if time() - self.startTime > self.timeLmt:
                    break
                if tempval > maxval:
                    maxval = tempval
                    max_set = [move]
                elif tempval == maxval:
                    max_set.append(move)

            if time() - self.startTime > self.timeLmt:
                break
            output_move = random.choice(max_set)
            print output_move

        return output_move

    def move(self, board, old_move, flag):
        self.startTime = time()
        self.sign = flag
        if flag == 'x':
            self.opposite_sign = 'o'
        else:
            self.opposite_sign = 'x'
        ansMove = self.iterative_search(board, old_move, flag)
        return ansMove

    def minimax(self, board, move, depth, isMaximizingPlayer, alpha, beta):
        if time() - self.startTime > self.timeLmt:
            return self.INT_MIN - 1
        if depth == 0 or board.find_terminal_state() != ('CONTINUE', '-'):
            return self.heuristic(board)
        if isMaximizingPlayer:
            bestVal = self.INT_MIN
            moves = board.find_valid_move_cells(move)
            for new_move in moves:
                board.update(move, new_move, self.sign)
                self.board_wins = self.boardWins(board)[0]
                if self.board_wins - self.old_board_wins > 0 and self.bonus[0] > 0:
                    self.old_board_wins = self.board_wins
                    self.bonus[0] -= 1
                    bestVal = max(bestVal, self.minimax(board, new_move, depth - 1, True, alpha, beta))
                else:
                    bestVal = max(bestVal, self.minimax(board, new_move, depth - 1, False, alpha, beta))
                board.board_status[new_move[0]][new_move[1]] = '-'
                board.block_status[new_move[0] / 4][new_move[1] / 4] = '-'
                if time() - self.startTime > self.timeLmt:
                    return self.INT_MIN - 1
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break

            return bestVal
        bestVal = self.INT_MAX
        moves = board.find_valid_move_cells(move)
        for new_move in moves:
            board.update(move, new_move, self.opposite_sign)
            self.board_opp_wins = self.boardWins(board)[1]
            if self.board_opp_wins - self.old_opp_wins > 0 and self.bonus[1] > 0:
                self.old_opp_wins = self.board_opp_wins
                self.bonus[1] -= 1
                bestVal = min(bestVal, self.minimax(board, new_move, depth - 1, False, alpha, beta))
            else:
                bestVal = min(bestVal, self.minimax(board, new_move, depth - 1, True, alpha, beta))
            board.board_status[new_move[0]][new_move[1]] = '-'
            board.block_status[new_move[0] / 4][new_move[1] / 4] = '-'
            if time() - self.startTime > self.timeLmt:
                return self.INT_MIN - 1
            beta = min(beta, bestVal)
            if beta <= alpha:
                break

        return bestVal

    def heuristic(self, board):
        new_state = board.find_terminal_state()
        if new_state[1] == 'WON':
            if new_state[0] == self.sign:
                score = self.INT_MAX
            else:
                score = self.INT_MIN
            return score
        block_rows_data = self.getBlockRows(board)
        block_cols_data = self.getBlockCols(board)
        block_dias_data = self.getBlockDias(board)
        block_pos_data = self.getBlockPos(board)
        block_cell_data = self.getCellAll(board)
        attack = 1000 * (block_rows_data[0] + block_cols_data[0] + block_dias_data[0]) + 50 * (block_cell_data[0] + block_cell_data[3] + block_cell_data[6])
        defence = 1000 * (block_rows_data[1] + block_cols_data[1] + block_dias_data[1]) + 50 * (block_cell_data[1] + block_cell_data[4] + block_cell_data[7])
        return attack - defence

    def getBlockRows(self, board):
        row_draw = 0
        row_win = 0
        row_lose = 0
        row_empty = 0
        for i in range(4):
            mycount = 0
            oppcount = 0
            drawcount = 0
            for j in range(4):
                if board.block_status[i][j] == self.sign:
                    mycount += 1
                elif board.block_status[i][j] == self.opposite_sign:
                    oppcount += 1
                elif board.block_status[i][j] == 'd':
                    drawcount += 1

            if drawcount > 0:
                row_draw += 1
            elif mycount > 0 and oppcount == 0:
                row_win += self.factor ** mycount
            elif oppcount > 0 and mycount == 0:
                row_lose += self.factor ** oppcount
            elif oppcount == 0 and mycount == 0 and drawcount == 0:
                row_empty += 1
            elif oppcount > 0 and mycount > 0:
                row_draw += 1

        return [
         row_win, row_lose, row_draw, row_empty]

    def getBlockCols(self, board):
        col_draw = 0
        col_win = 0
        col_lose = 0
        col_empty = 0
        for i in range(4):
            mycount = 0
            oppcount = 0
            drawcount = 0
            for j in range(4):
                if board.block_status[j][i] == self.sign:
                    mycount += 1
                elif board.block_status[j][i] == self.opposite_sign:
                    oppcount += 1
                elif board.block_status[j][i] == 'd':
                    drawcount += 1

            if drawcount > 0:
                col_draw += 1
            elif mycount > 0 and oppcount == 0:
                col_win += self.factor ** mycount
            elif oppcount > 0 and mycount == 0:
                col_lose += self.factor ** oppcount
            elif oppcount == 0 and mycount == 0 and drawcount == 0:
                col_empty += 1
            elif oppcount > 0 and mycount > 0:
                col_draw += 1

        return [
         col_win, col_lose, col_draw, col_empty]

    def getBlockDias(self, board):
        dia_draw = 0
        dia_win = 0
        dia_lose = 0
        dia_empty = 0
        for p in [[0, 1], [0, 2], [1, 1], [1, 2]]:
            mycount = 0
            oppcount = 0
            drawcount = 0
            if board.block_status[p[0]][p[1]] == self.sign:
                mycount += 1
            else:
                if board.block_status[p[0]][p[1]] == self.opposite_sign:
                    oppcount += 1
                else:
                    if board.block_status[p[0]][p[1]] == 'd':
                        drawcount += 1
            if board.block_status[p[0] + 1][p[1] - 1] == self.sign:
                mycount += 1
            else:
                if board.block_status[p[0] + 1][p[1] - 1] == self.opposite_sign:
                    oppcount += 1
                else:
                    if board.block_status[p[0] + 1][p[1] - 1] == 'd':
                        drawcount += 1
            if board.block_status[p[0] + 2][p[1]] == self.sign:
                mycount += 1
            else:
                if board.block_status[p[0] + 2][p[1]] == self.opposite_sign:
                    oppcount += 1
                else:
                    if board.block_status[p[0] + 2][p[1]] == 'd':
                        drawcount += 1
            if board.block_status[p[0] + 1][p[1] + 1] == self.sign:
                mycount += 1
            else:
                if board.block_status[p[0] + 1][p[1] + 1] == self.opposite_sign:
                    oppcount += 1
                else:
                    if board.block_status[p[1] + 1][p[1] + 1] == 'd':
                        drawcount += 1
            if drawcount > 0:
                dia_draw += 1
            elif mycount > 0 and oppcount == 0:
                dia_win += self.factor ** mycount
            elif oppcount > 0 and mycount == 0:
                dia_lose += self.factor ** oppcount
            elif oppcount == 0 and mycount == 0 and drawcount == 0:
                dia_empty += 1
            elif oppcount > 0 and mycount > 0:
                dia_draw += 1

        return [dia_win, dia_lose, dia_draw, dia_empty]

    def getBlockPos(self, board):
        center_win = 0
        center_lose = 0
        corner_win = 0
        corner_lose = 0
        edge_win = 0
        edge_lose = 0
        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == self.sign:
                    if self.is_centre(i, j) == 1:
                        center_win += 1
                    elif self.is_corner(i, j) == 1:
                        corner_win += 1
                    else:
                        edge_win += 1
                if board.block_status[i][j] == self.opposite_sign:
                    if self.is_centre(i, j) == 1:
                        center_lose += 1
                    elif self.is_corner(i, j) == 1:
                        corner_lose += 1
                    else:
                        edge_lose += 1

        return [
         center_win, center_lose, corner_win, corner_lose, edge_win, edge_lose]

    def is_centre(self, row, col):
        if row == 1 and col == 1:
            return 1
        if row == 1 and col == 2:
            return 1
        if row == 2 and col == 1:
            return 1
        if row == 2 and col == 2:
            return 1
        return 0

    def is_corner(self, row, col):
        if row == 0 and col == 0:
            return 1
        if row == 0 and col == 3:
            return 1
        if row == 3 and col == 0:
            return 1
        if row == 3 and col == 3:
            return 1
        return 0

    def getCellAll(self, board):
        row_draw = 0
        row_win = 0
        row_lose = 0
        row_empty = 0
        col_draw = 0
        col_win = 0
        col_lose = 0
        col_empty = 0
        dia_draw = 0
        dia_win = 0
        dia_lose = 0
        dia_empty = 0
        for ib in range(4):
            for jb in range(4):
                if board.block_status[ib][jb] == '-':
                    for i in range(4):
                        myrowcount = 0
                        opprowcount = 0
                        drawrowcount = 0
                        mycolcount = 0
                        oppcolcount = 0
                        drawcolcount = 0
                        ci = 4 * ib + i
                        for j in range(4):
                            cj = 4 * jb + j
                            if board.board_status[ci][cj] == self.sign:
                                myrowcount += 1
                            else:
                                if board.board_status[ci][cj] == self.opposite_sign:
                                    opprowcount += 1
                                else:
                                    if board.board_status[ci][cj] == 'd':
                                        drawrowcount += 1
                            if board.board_status[cj][ci] == self.sign:
                                mycolcount += 1
                            elif board.board_status[cj][ci] == self.opposite_sign:
                                oppcolcount += 1
                            elif board.board_status[cj][ci] == 'd':
                                drawcolcount += 1

                        if drawrowcount > 0:
                            row_draw += 1
                        else:
                            if myrowcount > 0 and opprowcount == 0:
                                row_win += self.factor ** myrowcount
                            else:
                                if opprowcount > 0 and myrowcount == 0:
                                    row_lose += self.factor ** opprowcount
                                else:
                                    if opprowcount == 0 and myrowcount == 0 and drawrowcount == 0:
                                        row_empty += 1
                                    else:
                                        if opprowcount > 0 and myrowcount > 0:
                                            row_draw += 1
                        if drawcolcount > 0:
                            col_draw += 1
                        elif mycolcount > 0 and oppcolcount == 0:
                            col_win += self.factor ** mycolcount
                        elif oppcolcount > 1 and mycolcount == 0:
                            col_lose += self.factor ** oppcolcount
                        elif oppcolcount == 0 and mycolcount == 0 and drawcolcount == 0:
                            col_empty += 1
                        elif oppcolcount > 0 and mycolcount > 0:
                            col_draw += 1

                    for p in [[4 * ib, 4 * jb + 1], [4 * ib, 4 * jb + 2], [4 * ib + 1, 4 * jb + 1], [4 * ib + 1, 4 * jb + 2]]:
                        mydiacount = 0
                        oppdiacount = 0
                        drawdiacount = 0
                        if board.board_status[p[0]][p[1]] == self.sign:
                            mydiacount += 1
                        else:
                            if board.board_status[p[0]][p[1]] == self.opposite_sign:
                                oppdiacount += 1
                            else:
                                if board.board_status[p[0]][p[1]] == 'd':
                                    drawdiacount += 1
                        if board.board_status[p[0] + 1][p[1] - 1] == self.sign:
                            mydiacount += 1
                        else:
                            if board.board_status[p[0] + 1][p[1] - 1] == self.opposite_sign:
                                oppdiacount += 1
                            else:
                                if board.board_status[p[0] + 1][p[1] - 1] == 'd':
                                    drawdiacount += 1
                        if board.board_status[p[0] + 2][p[1]] == self.sign:
                            mydiacount += 1
                        else:
                            if board.board_status[p[0] + 2][p[1]] == self.opposite_sign:
                                oppdiacount += 1
                            else:
                                if board.board_status[p[0] + 2][p[1]] == 'd':
                                    drawdiacount += 1
                        if board.board_status[p[0] + 1][p[1] + 1] == self.sign:
                            mydiacount += 1
                        else:
                            if board.board_status[p[0] + 1][p[1] + 1] == self.opposite_sign:
                                oppdiacount += 1
                            else:
                                if board.board_status[p[1] + 1][p[1] + 1] == 'd':
                                    drawdiacount += 1
                        if drawdiacount > 0:
                            dia_draw += 1
                        elif mydiacount > 0 and oppdiacount == 0:
                            dia_win += self.factor ** mydiacount
                        elif oppdiacount > 0 and mydiacount == 0:
                            dia_lose += self.factor ** oppdiacount
                        elif oppdiacount == 0 and mydiacount == 0 and drawdiacount == 0:
                            dia_empty += 1
                        elif oppdiacount > 0 and mydiacount > 0:
                            dia_draw += 1

        return [
         row_win, row_lose, row_draw, col_win, col_lose, col_draw, dia_win, dia_lose, dia_draw]

    def boardWins(self, board):
        mycount = 0
        oppcount = 0
        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == self.sign:
                    mycount += 1
                if board.block_status[i][j] == self.opposite_sign:
                    oppcount += 1

        return [
         mycount, oppcount]
