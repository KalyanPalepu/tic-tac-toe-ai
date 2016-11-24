import copy, sys


class Board:
    def __init__(self, player, state):
        self.player = player
        self.state = state  # 1 is X, 0 is empty, -1 is O
        self.children = []
        self.winner = None

    def full(self):
        for i in xrange(3):
            for j in xrange(3):
                if self.state[i][j] == 0:
                    return False
        return True

    def diagonals(self):
        if self.state[0][0] == self.state[1][1] == self.state[2][2] and self.state[0][0] != 0:
            return self.state[0][0]
        if self.state[0][2] == self.state[1][1] == self.state[2][0] and self.state[0][0] != 0:
            return self.state[0][2]
        return 0

    def non_diagonals(self):
        # verticals and horizontals
        for i in xrange(3):
            if self.state[i][0] == self.state[i][1] == self.state[i][2] and self.state[i][0] != 0:
                return self.state[i][0]
            if self.state[0][i] == self.state[1][i] == self.state[2][i] and self.state[0][i] != 0:
                return self.state[0][i]
        return 0

    def score(self):
        # returns true if game is over

        diagonals = self.diagonals()
        if diagonals != 0:
            self.winner = diagonals
            return True

        non_diagonals = self.non_diagonals()
        if non_diagonals != 0:
            self.winner = non_diagonals
            return True

        if self.full():
            self.winner = 0
            return True

        return False

    def generate_games(self):
        empty_coords = []
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    empty_coords.append((i, j))

        for coord in range(len(empty_coords)):
            new_state = copy.deepcopy(self.state)
            new_state[empty_coords[coord][0]][empty_coords[coord][1]] = self.player
            self.children.append(Board(-self.player, new_state))

    def printState(self):
        write = self.state
        for i in xrange(3):
            for j in xrange(3):
                if write[i][j] == -1:
                    sys.stdout.write('O')
                if write[i][j] == 0:
                    sys.stdout.write('-')
                if write[i][j] == 1:
                    sys.stdout.write('X')
                sys.stdout.write(' ')
            sys.stdout.write('\n')

    def empty(self):
        ret = []
        for i in xrange(3):
            for j in xrange(3):
                if self.state[i][j] == 0:
                    ret.append((i, j))
        return ret

