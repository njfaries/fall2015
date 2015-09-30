__author__ = 'nathaniel'

import random
import socket
import copy

default_state = [[' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                ['X', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', 'X'],
                ['X', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', 'X'],
                ['X', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ']]


problem_state = [[' ', ' ', ' ', ' ', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', 'O', 'O', ' '],
                [' ', 'O', ' ', 'X', 'X', ' ', ' '],
                [' ', ' ', 'O', 'X', ' ', 'X', ' '],
                [' ', 'X', ' ', 'O', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', 'O', ' ']]

new_problem_state = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', 'O', ' ', 'X', ' '],
                    [' ', ' ', ' ', ' ', ' ', 'X', 'O'],
                    [' ', ' ', ' ', 'O', 'X', 'O', 'X'],
                    [' ', 'X', ' ', 'X', ' ', ' ', ' '],
                    [' ', 'O', ' ', ' ', ' ', ' ', 'O']]

question_1 =    [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                ['O', ' ', 'X', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'O', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', 'O', 'X', 'X'],
                [' ', ' ', 'O', ' ', ' ', 'O', 'X'],
                [' ', ' ', ' ', 'X', 'O', ' ', ' ']]
 
question_2 =    [['O', 'O', ' ', ' ', ' ', ' ', ' '],
                ['X', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', 'X', ' ', ' ', 'O', ' '],
                [' ', ' ', 'X', 'O', ' ', ' ', 'X'],
                [' ', ' ', ' ', ' ', 'O', 'X', ' '],
                [' ', 'X', ' ', ' ', ' ', ' ', ' '],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ']]

question_3 =    [[' ', ' ', 'O', ' ', 'X', ' ', ' '],
                [' ', ' ', 'O', ' ', 'X', ' ', ' '],
                [' ', ' ', 'X', ' ', 'O', ' ', ' '],
                [' ', ' ', 'X', ' ', 'O', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', 'O', ' ', 'X', ' ', ' '],
                [' ', ' ', 'X', ' ', 'O', ' ', ' ']]



#defining inf and neginf just for convenience
INF = 1000000
NEG_INF = -1000000
MOVES = ["N", "E", "S", "W"]

character = ""
opponent = ""
nodes = 0


class Node:
    def __init__(self, state, score, parent, children, move):
        self.state = state
        self.score = score
        self.parent = parent
        self.children = children
        self.move = move  # to clarify, this is the move performed to reach this node from its parent. different nodes with the same state may have different moves


def get_piece_locations(state, piece):
    i = 0
    piece_locations = []
    for row in state:
        j = 0
        for index in row:
            if index == piece:
                piece_locations.append((i, j))
            j += 1
        i += 1
    return piece_locations

def is_win(state):
    sequences = find_sequence(state, character)
    for group in sequences:
        if len(group) == 4:
            return True
    return False

def is_loss(state):
    sequences = find_sequence(state, opponent)
    for group in sequences:
        if len(group) == 4:
            return True
    return False


def is_terminal(state):
    return is_win(state) or is_loss(state)


def find_sequence(state, char):  # character = x or o
    pieces = get_piece_locations(state, char)
    directions = [(-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, 1), (1, 0), (1, -1)]
    groupings = []
    for piece in pieces:
        for direction in directions:
            group = [piece]
            i = 0
            x = piece[0] + direction[0]
            y = piece[1] + direction[1]
            while 0 <= x < 7 and 0 <= y < 7 and i < 3:
                if state[x][y] == char:
                    group.append((x, y))
                elif state[x][y] != " ":
                    break
                i += 1
                x += direction[0]
                y += direction[1]
            if len(group) > 1:
                groupings.append(group)
    return groupings


def is_move_valid(state, move):
    x = int(move[0])
    if x < 0 or x > 6:
        return False
    y = int(move[1])
    if y < 0 or y > 6:
        return False
    direction = move[2]
    if direction == "N":
        x -= 1
    elif direction == "E":
        y += 1
    elif direction == "S":
        x += 1
    elif direction == "W":
        y -= 1
    else:
        return False
    if x < 0 or x > 6 or y < 0 or y > 6:
        return False
    if state[x][y] == " ":
        return True
    else:
        return False


def board_init(state, dimension, colour):
    global character
    global opponent
    if colour == "white":
        character = "O"
        opponent = "X"
    elif colour == "black":
        character = "X"
        opponent = "O"
    if state is not None:
        return state
    board = []
    return board + [" "] * dimension ** 2


def find_all_moves(state, my_turn):
    if my_turn:
        piece_locations = get_piece_locations(state, character)
    else:
        piece_locations = get_piece_locations(state, opponent)
    moves = []
    for piece in piece_locations:
        for direction in MOVES:
            string_move = str(piece[0]) + str(piece[1]) + direction
            if is_move_valid(state, string_move):
                moves.append(string_move)
    return moves


def apply_move(state, move, my_turn):
    new_state = copy.deepcopy(state)
    x = int(move[0])
    y = int(move[1])
    direction = move[2]
    newx = x
    newy = y
    if direction == "N":
        newx -= 1
    elif direction == "E":
        newy += 1
    elif direction == "S":
        newx += 1
    elif direction == "W":
        newy -= 1
    new_state[x][y] = " "
    if my_turn:
        new_state[newx][newy] = character
    else:
        new_state[newx][newy] = opponent
    return new_state


def compute_score(state, my_sequences, opponent_sequences):
    if is_win(state):
        return INF
    elif is_loss(state):
        return NEG_INF
    elif my_sequences is not None and opponent_sequences is not None:
        my_twos = []
        my_threes = []
        op_twos = []
        op_threes = []
        for seq in my_sequences:
            if len(seq) == 2:
                my_twos.append(seq)
            elif len(seq) == 3:
                my_threes.append(seq)
        for seq in opponent_sequences:
            if len(seq) == 2:
                op_twos.append(seq)
            elif len(seq) == 3:
                op_threes.append(seq)
        return len(my_twos) + 3 * len(my_threes) - len(op_twos) - 3 * len(my_threes)
    else:
        return compute_score(state, find_sequence(state, character), find_sequence(state, opponent))


def make_tree(state, root, depth, my_turn):  # depth to show how many more iterations to go through.
    global nodes
    if root is None:
        root = Node(state, compute_score(state, find_sequence(state, character), find_sequence(state, opponent)), None, [], None)
    all_moves = find_all_moves(state, my_turn)
    for move in all_moves:
        new_state = apply_move(state, move, my_turn)
        nodes += 1
        next_root = Node(new_state, 0, root, [], move)

        if not is_terminal(new_state) and depth != 0:
            make_tree(new_state, next_root, depth - 1, not my_turn)
        else:
            my_sequences = find_sequence(new_state, character)
            opponent_sequences = find_sequence(new_state, opponent)
            next_root.score = compute_score(new_state, my_sequences, opponent_sequences)
        root.children.append(next_root)
    return root


def find_best_move(tree, my_turn):
    if my_turn:
        best_score = NEG_INF
    else:
        best_score = INF
    best_move = tree.move #this is here for when we reach leaf nodes
    print tree.move
    for child in tree.children:
        best_move_from_child = find_best_move(child, not my_turn)
        child_state = apply_move(child.state, best_move_from_child, my_turn)
        if my_turn:
            if child.score > best_score:
                best_score = child.score
                best_move = child.move
            tree.score = best_score #goes in the for loop otherwise it would override the score of leaf nodes
        else:
            if child.score < best_score:
                best_score = child.score
                best_move = child.move
            tree.score = best_score
    return best_move

def alpha_beta(state, depth, alpha, beta, my_turn, root):
    global nodes
    if depth == 0 or is_terminal(state):
        root.score = compute_score(state, None, None) #root already fully exists as a node. Just need to add the score
        return root
    if root is None:
        root = Node(state, 0, None, None, None)
    if my_turn:
        value = NEG_INF
        moves = find_all_moves(state, my_turn)
        for move in moves:
            new_state = apply_move(state, move, my_turn)
            new_node = Node(new_state, 0, root, None, move)
            nodes += 1
            value = max(value, alpha_beta(new_state, depth - 1, alpha, beta, not my_turn, new_node).score)
            if value > alpha:
                root.move = move
            alpha = max(alpha, value)
            root.score = alpha
            if beta <= alpha:
                break
        if root.move is None:
            root.move = moves[0]
        return root
    else:
        value = INF
        moves = find_all_moves(state, my_turn)
        for move in moves:
            new_state = apply_move(state, move, my_turn)
            new_node = Node(new_state, 0, root, None, move)
            nodes += 1
            value = min(value, alpha_beta(new_state, depth - 1, alpha, beta, not my_turn, new_node).score)
            if value < beta:
                root.move = move
            beta = min(beta, value)
            root.score = beta
            if beta <= alpha:
                break
        if root.move is None: #this is because the value of nodes is getting stuff at INF or NEG_INF near goal states....
            root.move = moves[0]
        return root


def make_move(state):
    global nodes
    nodes = 0
    move = alpha_beta(state, 3, NEG_INF, INF, True, None).move
    x = int(move[0]) + 1 #because 1-indexing...
    y = int(move[1]) + 1
    move = str(x) + str(y) + move[2]
    print nodes
    return move

def make_minimax_move(state):
    global nodes
    nodes = 0
    tree = make_tree(state, None, 3, True)
    print nodes



#
# TCP_PORT = 12345
# TCP_IP = '127.0.0.1'
# colour = "white"
# MESSAGE = "mytestgame " + colour + "\n"
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# s.send(MESSAGE)
# data = s.recv(1024)
# s.close()
#
# print "received data:", data

game_board = board_init(default_state, 7, "white")
a = board_init(question_1, 7, "white")
b = board_init(question_2, 7, "white")
c = board_init(question_3, 7, "white")
# print compute_score(game_board, find_sequence(game_board, character), find_sequence(game_board, opponent))
i = 0
turn = True

# print character

print compute_score(game_board, None, None)

print "Board a minimax"
make_minimax_move(a)
print "Board b minimax"
make_minimax_move(b)
print "Board c minimax"
make_minimax_move(c)
print "Board a alpha-beta"
make_move(a)
print "Board b alpha-beta"
make_move(b)
print "Board c alpha-beta"
make_move(c)




# while (not is_win(game_board)):
#     best_move = alpha_beta(game_board, 6, NEG_INF, INF, turn, None)
#     print " "
#     print best_move.move
#     # for row in best_move.state:
#     #     print row
#     game_board = apply_move(game_board, best_move.move, turn)
#     for row in game_board:
#         print row
#     i += 1
#     print find_sequence(game_board, character)
#     # print compute_score(game_board, None, None)
#     turn = not turn
# print is_win(game_board)