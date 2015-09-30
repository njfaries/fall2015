__author__ = 'nathaniel'

import random
import socket
import copy

default_state = [[" ", " ", "X", " ", "X", "X", "X"],
                 ["X", " ", " ", "O", " ", "O", "O"],
                 ["O", " ", " ", " ", " ", " ", "X"],
                 ["X", " ", " ", " ", " ", " ", "O"],
                 ["O", " ", " ", " ", " ", " ", "X"],
                 ["X", " ", " ", " ", " ", " ", "O"],
                 ["O", " ", " ", " ", " ", " ", " "]]
#defining inf and neginf just for convenience
INF = 1000000
NEG_INF = -1000000
MOVES = ["N", "E", "S", "W"]

character = ""
opponent = ""


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
            # print sequences
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
    # print "My_turn: " + str(my_turn)
    # print "Printing piece locations"
    # print piece_locations
    for piece in piece_locations:
        for direction in MOVES:
            string_move = str(piece[0]) + str(piece[1]) + direction
            # print is_move_valid(state, string_move)
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
    # print "Applied move: " + move
    # print new_state
    return new_state


def compute_score(state, my_sequences, opponent_sequences):
    if is_win(state):
        return INF
    elif is_loss(state):
        return NEG_INF
    elif my_sequences is not None and opponent_sequences is not None:
        return 3 * len(my_sequences) - 2 * len(opponent_sequences)
    else:
        my_sequences = find_sequence(state, character)
        print my_sequences
        opponent_sequences = find_sequence(state, opponent)
        return 3 * len(my_sequences) - 2 * len(opponent_sequences)


def make_tree(state, root, depth, my_turn):  # depth to show how many more iterations to go through.
    if root is None:
        root = Node(state, compute_score(state, find_sequence(state, character), find_sequence(state, opponent)), None, [], None)
    all_moves = find_all_moves(state, my_turn)
    # print "Printing possible moves for this state"
    # print all_moves
    for move in all_moves:
        new_state = apply_move(state, move, my_turn)
        next_root = Node(new_state, 0, root, [], move)
        if not is_terminal(new_state) and depth != 0:
            # print depth
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

def alpha_beta(state, depth, alpha, beta, my_turn):
    if depth == 0 or is_terminal(state):
        return compute_score(state, None, None)
    if my_turn:
        value = NEG_INF
        for move in find_all_moves(state, my_turn):
            value = max(value, alpha_beta(apply_move(state, move, my_turn), depth - 1, alpha, beta, not my_turn))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        print "My turn.  Move " + move + " has value: " + str(value) + "  Current depth is: " + str(depth)
        return value
    else:
        value = INF
        for move in find_all_moves(state, my_turn):
            value = min(value, alpha_beta(apply_move(state, move, my_turn), depth - 1, alpha, beta, not my_turn))
            beta = min(beta, value)
            if beta <= alpha:
                break
        print "Opponent turn: " + str(value)
        return value


def make_move(state):
    tree = make_tree(state, None, 3)  # depth of three to start, just as default. will tweak in the future as needed
    move = find_best_move(tree)
    return move #note that I'll have to add 1 to both of the indices before sending the string to the server cause yay 1-indexing -_-


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
# print compute_score(game_board, find_sequence(game_board, character), find_sequence(game_board, opponent))
i = 0
turn = True

# print character

# print compute_score(game_board, None, None)


# alpha_beta(game_board, 3, NEG_INF, INF, turn)
while (not is_win(game_board)):
    test_tree = make_tree(game_board, None, 3, turn)
    best_move = find_best_move(test_tree, turn)
    print best_move
    game_board = apply_move(game_board, best_move, turn)
    for row in game_board:
        print row
    i += 1
    print compute_score(game_board, find_sequence(game_board, character), find_sequence(game_board, opponent))
    turn = not turn
# print is_win(game_board)