import numpy as np
import copy
from board import Board
from scipy.special import expit
import random

trained_weights = np.loadtxt(open('weights/best_weights.txt', 'r'))
# weights_bkp
theta_one = np.reshape(trained_weights[:110], (10, 11))
theta_two = np.reshape(trained_weights[110:], (3, 11))


def choose_next_move(board):
    switch = True
    for i in xrange(3):
        for j in xrange(3):
            if board.state[i][j] != 0:
                switch = False
    if switch:
        new_state = copy.deepcopy(board.state)
        new_state[random.randint(0, 2)][random.randint(0, 2)] = 1
        return Board(-board.player, new_state)  # makes game more interesting by starting with a random move.  All first moves have same minimax score
    if board.score():
        return board
    board.generate_games()
    scores = []
    for child in board.children:
        scores.append(evaluate_move(board, child, theta_one, theta_two))
    if board.player == 1:
        max_score = max(scores)
        max_score_indices = []
        for i in xrange(len(scores)):
            if scores[i] == max_score:
                max_score_indices.append(i)
        print max_score_indices
        return board.children[random.choice(max_score_indices)]
    else:
        min_score = min(scores)
        min_score_indices = []
        for i in xrange(len(scores)):
            if scores[i] == min_score:
                min_score_indices.append(i)
        print min_score_indices
        return board.children[random.choice(min_score_indices)]

    # if board.player == 1:
    #     return board.children[scores.index(max(scores))]
    # else:
    #     return board.children[scores.index(min(scores))]


def evaluate_move(original_board, moved_board, t_one, t_two):
    move = 0
    for i in xrange(3):
        for j in xrange(3):
            if original_board.state[i][j] != moved_board.state[i][j]:
                move = i * 3 + j

    input = np.hstack((1, (np.array(original_board.state).flatten()), move))
    y_hat = expit(np.dot(np.insert(expit(np.dot(input, t_one.T)), 0, 1), t_two.T))
    return np.argmax(y_hat) - 1


print "Tic-Tac-Toe Neural Network"
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
    if x == 'n':
        game.score()
game.printState()
if game.winner == 0:
    print "It's a tie!"
elif game.winner == -1:
    print "O wins!"
else:
    print "X wins!"