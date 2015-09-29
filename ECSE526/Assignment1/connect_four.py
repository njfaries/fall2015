__author__ = 'nathaniel'

import random
import socket
import copy

default_state = [[" ", " ", " ", " ", " ", " ", "X"],
                 ["X", " ", " ", " ", " ", " ", "O"],
                 ["O", " ", " ", " ", " ", " ", "X"],
                 ["X", " ", " ", " ", " ", " ", "O"],
                 ["O", " ", " ", " ", " ", " ", "X"],
                 ["X", " ", " ", " ", " ", " ", "O"],
                 ["O", " ", " ", " ", " ", " ", " "]]

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


def is_win(state):
    i = 0
    piece_locations = []
    for row in state:
        j = 0
        for index in row:
            if index == "X":  # need to figure out how to define this guy to vary accoriding to colour
                piece_locations.append((i, j))
            j += 1
        i += 1
    i = 0
    # while i < len(piece_locations - 3):
    #     if piece_locations[i][0] == piece_locations[i+1][0] == piece_locations[i+2][0] == piece_locations[i+3][0] \
    #         or piece_locations[i][1] == piece_locations[i+1][1] == piece_locations[i+2][1] == piece_locations[i+3][0] \
    #         or piece_locations[i][0] == piece_locations[i+1][0] + 1 == piece_locations[i+2][0] + 2 == piece_locations[i+3][0] + 3 and piece
    # lolwtf am i doing


def is_loss(state):
    return 0


def is_terminal(state):
    if is_win(state):
        return 1
    elif is_loss(state):
        return -1
    return 0


def find_sequence(state, character):  # character = x or o
    i = 0
    j = 0
    for row in state:
        for index in row:
            if index == character:
                j = index


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
    else:
        character = "X"
        opponent = "O"
    if state is not None:
        return state
    board = []
    return board + [" "] * dimension ** 2


def find_all_moves(state, my_turn):
    i = 0
    piece_locations = []
    moves = []
    for row in state:
        j = 0
        for index in row:
            if my_turn:
                if index == character:  # need to figure out how to define this guy to vary according to colour
                    piece_locations.append((i, j))
            else:
                if index == opponent:
                    piece_locations.append((i, j))
            j += 1
        i += 1
    print "Printing piece locations"
    print piece_locations
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
    print "Applied move: " + move
    print new_state
    return new_state


def compute_score(state):
    if is_win(state):
        return 1
    elif is_loss(state):
        return -1
    return 0


def make_tree(state, root, depth, my_turn):  # depth to show how many more iterations to go through.
    if root is None:
        root = Node(state, compute_score(state), None, [], None)
    all_moves = find_all_moves(state, my_turn)
    print "Printing possible moves for this state"
    print all_moves
    for move in all_moves:
        new_state = apply_move(state, move, my_turn)
        next_root = Node(new_state, compute_score(new_state), root, [], move)
        if not is_terminal(new_state) and depth != 0:
            # print depth
            make_tree(new_state, next_root, depth - 1, not my_turn)
        root.children.append(next_root)
    return root


def find_best_move(tree):
    best_score = 0
    best_move = None
    for child in tree.children:
        score = child.score + compute_score(find_best_move(child))
        if score > best_score:
            best_score = score
            best_move = child.move
    return best_move


def make_move(state):
    tree = make_tree(state, None, 10)  # depth of ten to start, just as default. will tweak in the future as needed
    move = find_best_move(tree)
    return move


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
print game_board
test_tree = make_tree(game_board, None, 2, True)
#print test_tree.children
print test_tree.move
# is_win(game_board)
