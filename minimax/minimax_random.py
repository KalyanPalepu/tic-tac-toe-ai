import copy
import sys
import random


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
        for i in range(3):
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


def generate_games(board):
    empty_coords= []
    for i in range(3):
        for j in range(3):
            if board.state[i][j] == 0:
                empty_coords.append((i, j))

    for coord in range(len(empty_coords)):
        new_state = copy.deepcopy(board.state)
        new_state[empty_coords[coord][0]][empty_coords[coord][1]] = board.player
        board.children.append(Board(-board.player, new_state))


def minimax(board):
    if board.score():
        return board.winner

    generate_games(board)
    if board.player == 1:
        return max(map(lambda child: minimax(child), board.children))
    else:
        return min(map(lambda child: minimax(child), board.children))


def choose_next_move(board):
    switch = True
    for i in xrange(3):
        for j in xrange(3):
            if board.state[i][j] != 0:
                switch = False
    if switch:
        new_state = copy.deepcopy(board.state)
        new_state[random.randint(0, 2)][random.randint(0, 2)] = 1
        return Board(-board.player, new_state)

    if board.score():
        return board

    generate_games(board)
    scores = []
    for child in board.children:
        scores.append(minimax(child))

    if board.player == 1:
        max_score = max(scores)
        max_score_indices = []
        for i in xrange(len(scores)):
            if scores[i] == max_score:
                max_score_indices.append(i)
        return board.children[random.choice(max_score_indices)]
    else:
        min_score = min(scores)
        min_score_indices = []
        for i in xrange(len(scores)):
            if scores[i] == min_score:
                min_score_indices.append(i)
        return board.children[random.choice(min_score_indices)]


def print_game(board):
    write = board.state
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


print "Tic-Tac-Toe Minimax"
print
x = raw_input("Will you play first? (y/n)")
game = Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

if x == 'n':
    game = choose_next_move(game)
while game.winner is None:
    game.printState()
    move = map(int, raw_input('Your move:').split()) # expects "i j"
    new_state = copy.deepcopy(game.state)
    while new_state[move[0] - 1][move[1] - 1] != 0:
        move = map(int, raw_input("Invalid Move.  Please try again:").split())
    new_state[move[0] - 1][move[1] - 1] = game.player
    game = choose_next_move(Board(-game.player, new_state))
    game.score()
game.printState()
if game.winner == 0:
    print "It's a tie!"
else:
    print "You lose!"
