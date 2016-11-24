from board import Board
import pickle, random, sys, copy, os, minimax

# https://www.cs.swarthmore.edu/~meeden/cs63/f11/lab6.php

if os.path.isfile('Q/Q.p'):
    qfile = open('Q/Q.p', 'r')
    Q = pickle.load(qfile)
    qfile.close()
    print len(Q)

else:
    Q = {}

# TUNABLE VALUES
gamma = .8
k = 1


def deep_tuple(l):
    return tuple(tuple(row) for row in l)

def correct_state(board, player=0):
    if player == 0:
        player = board.player
    return map(lambda row: map(lambda x: x * player, row), board.state)


def R(board):
    if board.score():
        if board.winner == -board.player:
            return 3
        elif board.winner == 0:
            return 1
        else:
            return -1
    else:
        return 0


def choose_next_move(board, optimal=False):
    Qvals = get_next_Qvals(board)

    if optimal or random.randint(0, k) == 1:
        print max(Qvals)
        return board.children[Qvals.index(max(Qvals))]

    else:
        return board.children[random.randint(0, len(board.children) - 1)]


def get_next_Qvals(board):
    # Needs corrected board at input
    board.generate_games()
    Qvals = []
    for move in board.children:
        corrected_state = deep_tuple(correct_state(move))  # Make sure player is 1 for indexing into Q
        if corrected_state not in Q:
            Q[corrected_state] = 0

        Qvals.append(Q[corrected_state])

    return Qvals


def train():
    i = input("How many games?")
    games = 0
    while games < i:
        if games > 5000 and games % 5000 == 0:
            f = open('Q/Q' + str(games) + '.p', 'w')
            pickle.dump(Q, f)
            f.close()
        game = Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        last = game
        while not game.score():
            last = game
            game = choose_next_move(game)
            if game.score():
                Q[deep_tuple(correct_state(last))] = R(game)
                continue
            game = choose_next_move(game)
            Qvals = get_next_Qvals(game)
            Q[deep_tuple(correct_state(last))] = R(game) + gamma * max(Qvals)
        sys.stdout.write("\rGame #" + str(games + 1) + " completed.")
        sys.stdout.flush()
        games += 1
    print
    f = open('Q/Q.p', 'w')
    pickle.dump(Q, f)
    f.close()
    counter = 0
    for key, value in Q.iteritems():
        if value != 0:
            counter += 1
    print counter




def backpropagate(board):
    corrected_state = deep_tuple(correct_state(board))
    if corrected_state in Q and Q[corrected_state] != 0:
        return Q[corrected_state]
    elif board.score():
            print str(corrected_state) + " not explored"
            Qval = R(board)
            Q[corrected_state] = 0
            return Qval

    board.generate_games()
    Qval = R(board) + gamma * max(map(lambda child: backpropagate(child), board.children))
    Q[corrected_state] = Qval
    return Qval



def minimax_train():
    i = input("How many games?")
    games = 0
    while games < i:
        if games > 100 and games % 100 == 0:
            f = open('Q/Q' + str(games) + '.p', 'w')
            pickle.dump(Q, f)
            f.close()
        game = Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        while not game.score():
            last = game
            game, Qvals_first = choose_next_move(game)
            if game.score():
                Q[deep_tuple(correct_state(last))] = R(game) + gamma * max(Qvals_first)
                continue
            game = minimax.choose_next_move(game)
            Q[deep_tuple(correct_state(last))] = R(game) + gamma * max(Qvals_first)
        sys.stdout.write("\rGame #" + str(games + 1) + " completed.")
        sys.stdout.flush()
        games += 1
    f = open('Q/Q.p', 'w')
    pickle.dump(Q, f)
    f.close()

def play():
    game = choose_next_move(Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]), optimal=True)
    while game.winner is None:
        game.printState()
        move = map(int, raw_input('Your move:').split())  # expects "i j"
        new_state = copy.deepcopy(game.state)
        while len(move) != 2 or (move[0] - 1, move[1] - 1) not in game.empty():
            move = map(int, raw_input("Invalid Move.  Please try again:").split())
        new_state[move[0] - 1][move[1] - 1] = game.player
        game = choose_next_move(Board(-game.player, new_state), optimal=True)
        game.score()
    game.printState()
    if game.winner == 0:
        print "It's a tie!"
    elif game.winner == -1:
        print "You Win!"
    else:
        print "You lose!"
    print R(game)


inp = raw_input("Train (y/n)?")
if inp == 'n':
    play()
else:
    train()

# backpropagate(Board(1, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
# f = open('Q/Q.p', 'w')
# pickle.dump(Q, f)
# f.close()
