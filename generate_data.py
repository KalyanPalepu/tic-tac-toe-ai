import copy

f = open('data.txt', 'w')


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
        if self.full():
            self.winner = 0
            return True

        diagonals = self.diagonals()
        if diagonals != 0:
            self.winner = diagonals
            return True

        non_diagonals = self.non_diagonals()
        if non_diagonals != 0:
            self.winner = non_diagonals
            return True
        return False


def minimax(board, depth):
    if board.score():
        return board.winner

    empty_coords = []
    s = ""
    for i in range(3):
        for j in range(3):
            s += str(board.state[i][j]) + ' '
            if board.state[i][j] == 0:
                empty_coords.append((i, j))
    scores = []
    for coord in range(len(empty_coords)):
        new_state = copy.deepcopy(board.state)
        new_state[empty_coords[coord][0]][empty_coords[coord][1]] = board.player
        b = Board(-board.player, new_state)
        print depth
        minmax = minimax(b, depth + 1)
        scores.append(minmax)
        f.write(s + str(empty_coords[coord][0] * 3 + empty_coords[coord][1]) + ' ' + str(minmax) + '\n')

    if board.player == 1:
        return max(scores)
    else:
        return min(scores)


def generate_data(board):
    empty_coords = []
    for i in range(3):
        for j in range(3):
            f.write(str(board.state[i][j]) if i + j == 4 else str(board.state[i][j]) + ' ')
            if board.state[i][j] == 0:
                empty_coords.append((i, j))
    f.write('\n')
    for coord in range(len(empty_coords)):
        new_state = copy.deepcopy(board.state)
        new_state[empty_coords[coord][0]][empty_coords[coord][1]] = board.player
        b = Board(-board.player, new_state)
        board.children.append(b)
        f.write('+ ' + str(empty_coords[coord][0] * 3 + empty_coords[coord][1]))
        f.write(' ' + str(minimax(b)) + '\n')


berd = Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
minimax(berd, 0)

f.close()