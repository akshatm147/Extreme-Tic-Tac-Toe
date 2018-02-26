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

import copy, signal, random, numpy as np

class MyPlayer:

    def __init__(self):
        self.r = 0
        self.mult = [ [ 0 for x in xrange(4) ] for y in xrange(4) ]
        self.store = np.empty([43046721, 2])
        self.store[:, :] = np.nan
        for l in xrange(4):
            for m in xrange(4):
                if (l == 0 or l == 3) and (m == 0 or m == 3):
                    self.mult[l][m] = 6
                elif (l == 1 or l == 2) and (m == 1 or m == 2):
                    self.mult[l][m] = 3
                else:
                    self.mult[l][m] = 4

    def signal_handler(self, signum, frame):
        raise Exception('')

    def changestate(self, state, choice, nu, blocksize):
        varx = choice[0] * blocksize
        vary = choice[1] * blocksize
        f = 0

        # Row check for completion
        for i in xrange(varx, varx + blocksize):
            cnt = 0
            for j in xrange(vary, vary + blocksize):
                cnt += state[i][j]

            if abs(cnt) == blocksize:
                f = 1
                break

        # Column check for completion
        if f == 0:
            for j in xrange(vary, vary + blocksize):
                cnt = 0
                for i in xrange(varx, varx + blocksize):
                    cnt += state[i][j]

                if abs(cnt) == blocksize:
                    f = 1
                    break

        # Diagonal check for completion
        if f == 0:
            i = varx
            j = vary
            cnt = 0

            cnt += state[i][j+1] + state[i+1][j] + state[i+2][j+1] + state[i+1][j+2]

            if abs(cnt) == blocksize:
                f = 1

        if f == 0:
            i = varx
            j = vary
            cnt = 0

            cnt += state[i+1][j+1] + state[i+2][j] + state[i+3][j+1] + state[i+2][j+2]

            if abs(cnt) == blocksize:
                f = 1

        if f == 0:
            i = varx
            j = vary
            cnt = 0

            cnt += state[i][j+2] + state[i+1][j+1] + state[i+2][j+2] + state[i+1][j+3]

            if abs(cnt) == blocksize:
                f = 1

        if f == 0:
            i = varx
            j = vary
            cnt = 0

            cnt += state[i+1][j+2] + state[i+2][j+1] + state[i+3][j+2] + state[i+2][j+3]

            if abs(cnt) == blocksize:
                f = 1

        if f:
            for i in xrange(varx, varx + blocksize):
                for j in xrange(vary, vary + blocksize):
                    state[i][j] = nu

        return state

    def max_value(self, state, alpha, beta, depth, choice, blocksize):
        if depth == 0:
            return [self.eval_fn(state, blocksize), [-1, -1]]
        v = -100000000000000.0
        boardsize = blocksize * blocksize
        rangexbeg = 0
        rangexend = 0
        rangeybeg = 0
        rangeyend = 0
        if self.filled(state, choice, blocksize):
            rangexbeg = 0
            rangexend = boardsize
            rangeybegin = 0
            rangeyend = boardsize
        else:
            rangexbeg = choice[0] * blocksize
            rangexend = rangexbeg + blocksize
            rangeybeg = choice[1] * blocksize
            rangeyend = rangeybeg + blocksize
        if self.nonew(state, [rangexbeg, rangexend, rangeybeg, rangeyend]):
            return [self.eval_fn(state, blocksize), [-1, -1]]
        for i in xrange(rangexbeg, rangexend):
            for j in xrange(rangeybeg, rangeyend):
                if state[i][j] == 0:
                    s = copy.deepcopy(state)
                    s[i][j] = 1
                    s = self.changestate(s, [i / blocksize, j / blocksize], 1, blocksize)
                    val = self.min_value(s, alpha, beta, depth - 1, [i % blocksize, j % blocksize], blocksize)
                    if v < val[0]:
                        v = val[0]
                        choice1 = copy.deepcopy([i, j])
                    if v >= beta:
                        return [v, choice1]
                    alpha = max(alpha, v)

        return [
         v, choice1]

    def min_value(self, state, alpha, beta, depth, choice, blocksize):
        if depth == 0:
            return [self.eval_fn(state, blocksize), [-1, -1]]
        v = 100000000000000.0
        boardsize = blocksize * blocksize
        rangexbeg = 0
        rangexend = 0
        rangeybeg = 0
        rangeyend = 0
        if self.filled(state, choice, blocksize):
            rangexbeg = 0
            rangexend = boardsize
            rangeybegin = 0
            rangeyend = boardsize
        else:
            rangexbeg = choice[0] * blocksize
            rangexend = rangexbeg + blocksize
            rangeybeg = choice[1] * blocksize
            rangeyend = rangeybeg + blocksize
        if self.nonew(state, [rangexbeg, rangexend, rangeybeg, rangeyend]):
            return [self.eval_fn(state, blocksize), [-1, -1]]
        for i in range(rangexbeg, rangexend):
            for j in xrange(rangeybeg, rangeyend):
                if state[i][j] == 0:
                    s = copy.deepcopy(state)
                    s[i][j] = -1
                    s = self.changestate(s, [i / blocksize, j / blocksize], -1, blocksize)
                    val = self.max_value(s, alpha, beta, depth - 1, [i % blocksize, j % blocksize], blocksize)
                    if v > val[0]:
                        v = val[0]
                        choice1 = copy.deepcopy([i, j])
                    if v <= alpha:
                        return [v, choice1]
                    beta = min(beta, v)

        return [
         v, choice1]

    def nonew(self, state, choice):
        flag = 0
        for i in xrange(choice[0], choice[1]):
            for j in xrange(choice[2], choice[3]):
                if state[i][j] == 0:
                    flag = 1

        return 1 - flag

    def compress(self, state, blocksize):
        boardsize = blocksize * blocksize
        listfor = [ [ 0 for x in xrange(blocksize) ] for y in xrange(blocksize) ]
        for i in xrange(0, boardsize, blocksize):
            for j in xrange(0, boardsize, blocksize):
                ans = 0
                for k in xrange(i, i + blocksize):
                    for l in xrange(j, j + blocksize):
                        ans += state[k][l]

                if abs(ans) == boardsize:
                    if ans < 0:
                        listfor[i / blocksize][j / blocksize] = -1
                    else:
                        listfor[i / blocksize][j / blocksize] = 1

        return listfor

    def wincheck(self, state, blocksize):
        win = 100000
        lose = -100000
        boardsize = blocksize * blocksize
        listfor = self.compress(state, blocksize)
        for i in xrange(0, blocksize):
            ans = 0
            for j in xrange(0, blocksize):
                ans += listfor[i][j]

            if abs(ans) == blocksize:
                if ans < 0:
                    return lose
                return win

        for i in xrange(0, blocksize):
            ans = 0
            for j in xrange(0, blocksize):
                ans += listfor[j][i]

            if abs(ans) == blocksize:
                if ans < 0:
                    return lose
                return win

        i=0
        j=0
        ans = 0
        ans += listfor[i][j+1] + listfor[i+1][j] + listfor[i+2][j+1] + listfor[i+1][j+2]

        if abs(ans) == blocksize:
            if ans < 0:
                return lose
            return win

        ans = 0
        ans += listfor[i+1][j+1] + listfor[i+2][j] + listfor[i+3][j+1] + listfor[i+2][j+2]

        if abs(ans) == blocksize:
            if ans < 0:
                return lose
            return win

        ans = 0
        ans += listfor[i][j+2] + listfor[i+1][j+1] + listfor[i+2][j+2] + listfor[i+1][j+3]

        if abs(ans) == blocksize:
            if ans < 0:
                return lose
            return win

        ans = 0
        ans += listfor[i+1][j+2] + listfor[i+2][j+1] + listfor[i+3][j+2] + listfor[i+2][j+3]

        if abs(ans) == blocksize:
            if ans < 0:
                return lose
            return win

        return 0

    def eval_fn(self, state, blocksize):
        val = 0
        sumx = 0
        val = self.wincheck(state, blocksize)
        if abs(val) == 10000000000:
            return val
        store_block = [ [ [ 0 for x in xrange(2) ] for y in xrange(4) ] for z in xrange(4) ]
        for i in xrange(0, blocksize):
            for j in xrange(0, blocksize):
                hashstore = self.ourhash(state, i * blocksize, j * blocksize, blocksize)
                if np.isnan(self.store[hashstore][0]):
                    self.store[hashstore] = self.winning(state, i * blocksize, j * blocksize, blocksize)
                store_block[i][j] = self.store[hashstore]
                sumx += store_block[i][j][0] - store_block[i][j][1]

        val = self.winning2(self.compress(state, blocksize), blocksize, store_block) / 10000.0
        if abs(val - 0.0) < 1e-06:
            val = sumx
        return val

    def ourhash(self, state, i, j, blocksize):
        k = 0
        for a in xrange(i, i + blocksize):
            for b in xrange(j, j + blocksize):
                k *= 3
                k += 1 + state[a][b]

        return k

    def winning2(self, state, blocksize, store_block):
        val = 0
        for i in xrange(blocksize):
            temp = 1
            temp1 = 1
            for j in xrange(blocksize):
                temp *= store_block[i][j][0]
                temp1 *= store_block[i][j][1]

            val += temp - temp1

        for i in xrange(blocksize):
            temp = 1
            temp1 = 1
            for j in xrange(blocksize):
                temp *= store_block[j][i][0]
                temp1 *= store_block[j][i][1]

            val += temp - temp1

        i=0
        j=0
        temp = 1
        temp1 = 1
        temp *= store_block[i][j+1][0] * store_block[i+1][j][0] * store_block[i+2][j+1][0] * store_block[i+1][j+2][0]
        temp1 *= store_block[i][j+1][1] * store_block[i+1][j][1] * store_block[i+2][j+1][1] * store_block[i+1][j+2][1]

        val += temp - temp1

        temp = 1
        temp1 = 1
        temp *= store_block[i+1][j+2][0] * store_block[i+2][j+1][0] * store_block[i+3][j+2][0] * store_block[i+2][j+3][0]
        temp1 *= store_block[i+1][j+2][1] * store_block[i+2][j+1][1] * store_block[i+3][j+2][1] * store_block[i+2][j+3][1]

        val += temp - temp1

        temp = 1
        temp1 = 1
        temp *= store_block[i][j+2][0] * store_block[i+1][j+1][0] * store_block[i+2][j+2][0] * store_block[i+1][j+3][0]
        temp1 *= store_block[i][j+2][1] * store_block[i+1][j+1][1] * store_block[i+2][j+2][1] * store_block[i+1][j+3][1]

        val += temp - temp1

        temp = 1
        temp1 = 1
        temp *= store_block[i+1][j+1][0] * store_block[i+2][j][0] * store_block[i+3][j+1][0] * store_block[i+2][j+2][0]
        temp1 *= store_block[i+1][j+1][1] * store_block[i+2][j][1] * store_block[i+3][j+1][1] * store_block[i+2][j+2][1]

        val += temp - temp1

        return val

    def winning(self, state, i, j, blocksize):
        val = 0
        f = 0
        val1 = 0
        for l in xrange(blocksize):
            temp1 = 1
            cnt1 = 0
            bnt1 = 0
            temp2 = 1
            cnt2 = 0
            bnt2 = 0
            for m in xrange(blocksize):
                if state[i + l][m + j] == 0:
                    temp1 *= 0.5
                else:
                    temp1 *= self.mult[l][m]
                bnt1 += state[i + l][j + m]
                cnt1 += abs(state[i + l][j + m])
                if state[i + m][j + l] == 0:
                    temp2 *= 0.5
                else:
                    temp2 *= self.mult[m][l]
                bnt2 += state[i + m][j + l]
                cnt2 += abs(state[i + m][j + l])

            if bnt1 == -cnt1:
                val1 += temp1
            if bnt1 == cnt1:
                val += temp1
            if bnt2 == -cnt2:
                val1 += temp2
            if bnt2 == cnt2:
                val += temp2

        i=0
        j=0
        temp = 1
        cnt = 0
        bnt = 0

        if state[i][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[i%4][(j+1)%4]
        cnt += abs(state[i][j+1])
        bnt += state[i][j+1]

        if state[i+1][j] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][j%4]
        cnt += abs(state[i+1][j])
        bnt += state[i+1][j]

        if state[i+2][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][(j+1)%4]
        cnt += abs(state[i+2][j+1])
        bnt += state[i+2][j+1]

        if state[i+1][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][(j+2)%4]
        cnt += abs(state[i+1][j+2])
        bnt += state[i+1][j+2]

        if bnt == -cnt:
            val1 += temp
        if bnt == cnt:
            val += temp

        temp = 1
        cnt = 0
        bnt = 0

        if state[i+1][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][(j+2)%4]
        cnt += abs(state[i+1][j+2])
        bnt += state[i+1][j+2]

        if state[i+2][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][(j+1)%4]
        cnt += abs(state[i+2][j+1])
        bnt += state[i+2][j+1]

        if state[i+3][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+3)%4][(j+2)%4]
        cnt += abs(state[i+3][j+2])
        bnt += state[i+3][j+2]

        if state[i+2][j+3] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][(j+3)%4]
        cnt += abs(state[i+2][j+3])
        bnt += state[i+2][j+3]

        if bnt == -cnt:
            val1 += temp
        if bnt == cnt:
            val += temp

        temp = 1
        cnt = 0
        bnt = 0

        if state[i+2][j] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][j%4]
        cnt += abs(state[i+2][j])
        bnt += state[i+2][j]

        if state[i+1][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][(j+1)%4]
        cnt += abs(state[i+1][j+1])
        bnt += state[i+1][j+1]

        if state[i+2][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][(j+2)%4]
        cnt += abs(state[i+2][j+2])
        bnt += state[i+2][j+2]

        if state[i+3][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+3)%4][(j+1)%4]
        cnt += abs(state[i+3][j+1])
        bnt += state[i+3][j+1]

        if bnt == -cnt:
            val1 += temp
        if bnt == cnt:
            val += temp

        temp = 1
        cnt = 0
        bnt = 0

        if state[i][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[i%4][(j+2)%4]
        cnt += abs(state[i][j+2])
        bnt += state[i][j+2]

        if state[i+1][j+1] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][(j+1)%4]
        cnt += abs(state[i+1][j+1])
        bnt += state[i+1][j+1]

        if state[i+2][j+2] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+2)%4][(j+2)%4]
        cnt += abs(state[i+2][j+2])
        bnt += state[i+2][j+2]

        if state[i+1][j+3] == 0:
            temp *= 0.5
        else:
            temp *= self.mult[(i+1)%4][(j+3)%4]
        cnt += abs(state[i+1][j+3])
        bnt += state[i+1][j+3]

        if bnt == -cnt:
            val1 += temp
        if bnt == cnt:
            val += temp

        return [val, val1]

    def wonby(self, state, i, j, blocksize):
        bal = 0
        boardsize = blocksize * blocksize
        for k in xrange(i, i + blocksize):
            for l in xrange(j, j + blocksize):
                bal += state[k][l]

        if bal == -boardsize:
            return -20
        if bal == boardsize:
            return 20
        return 0

    def filled(self, state, choice, blocksize):
        if choice[0] == -1 and choice[1] == -1:
            return 1
        varx = choice[0] * blocksize
        vary = choice[1] * blocksize
        f = 0
        for i in xrange(varx, varx + blocksize):
            for j in xrange(vary, vary + blocksize):
                if state[i][j] == 0:
                    f = 1

        return 1 - f

    def move(self, board, old_move, flag):
        blocksize = 4
        boardsize = 16
        other = 'x'
        if flag == 'x':
            other = 'o'
        state = [ [ 0 for x in xrange(boardsize) ] for y in xrange(boardsize) ]
        for i in xrange(0, blocksize * blocksize):
            for j in xrange(0, blocksize * blocksize):
                if board.block_status[i / blocksize][j / blocksize] == flag:
                    state[i][j] = 1
                elif board.block_status[i / blocksize][j / blocksize] == other:
                    state[i][j] = -1
                elif board.board_status[i][j] == other:
                    state[i][j] = -1
                elif board.board_status[i][j] == flag:
                    state[i][j] = 1

        choice = []
        choice_print = [0 for i in range(2)]
        choice.append(old_move[0] % blocksize)
        choice.append(old_move[1] % blocksize)
        ans = -1e+20
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(1)
        self.r = random.randint(0, 9)
        print self.r
        try:
            for i in xrange(2, 30):
                bal = self.max_value(state, -1e+20, 1e+20, i, choice, blocksize)
                if bal[0] <= -100000 and i > 2:
                    break
                print bal
                ans = bal[0]
                choice_print = bal[1]
                if ans >= 100000:
                    break

        except Exception as e:
            print e,

        signal.alarm(0)

        if choice_print:
            return (choice_print[0], choice_print[1])
        else:
            return (random.randint(0,15), random.randint(0,15))
