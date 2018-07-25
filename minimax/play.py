import sys
sys.path.append('..')
from board import Board
from minimax import choose_next_move
import copy

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
    while len(move) != 2 or (move[0] - 1, move[1] - 1) not in game.empty():
        move = map(int, raw_input("Invalid Move.  Please try again:").split())
    new_state[move[0] - 1][move[1] - 1] = game.player
    game = choose_next_move(Board(-game.player, new_state))
    if x == 'n':
        game.score()
game.printState()
if game.winner == 0:
    print "It's a tie!"
else:
    print "You lose!"



