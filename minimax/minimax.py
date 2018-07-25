import sys
sys.path.append('..')
from board import Board


def minimax(board):
    if board.score():
        return board.winner

    board.generate_games()
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
        return Board(-board.player, [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    if board.score():
        return board
    board.generate_games()
    scores = []
    for child in board.children:
        scores.append(minimax(child))
    if board.player == 1:
        return board.children[scores.index(max(scores))]
    else:
        return board.children[scores.index(min(scores))]


