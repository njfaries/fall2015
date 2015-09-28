__author__ = 'nathaniel'

import random
import socket

default_state = [[" ", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", " "]]

moves = ["N", "E", "S", "W"]

class Node():
    def __init__(self, state, score, parent, children):
        self.state = state
        self.score = score
        self.parent = parent
        self.children = children

def is_win(state):
    i = 0
    piece_locations = []
    for row in state:
        j = 0
        for index in row:
            if index == "X": #need to figure out how to define this guy to vary accoriding to colour
                piece_locations.append((i, j))
            j += 1
        i += 1
    print piece_locations
    i = 0
    # while i < len(piece_locations - 3):
    #     if piece_locations[i][0] == piece_locations[i+1][0] == piece_locations[i+2][0] == piece_locations[i+3][0] \
    #         or piece_locations[i][1] == piece_locations[i+1][1] == piece_locations[i+2][1] == piece_locations[i+3][0] \
    #         or piece_locations[i][0] == piece_locations[i+1][0] + 1 == piece_locations[i+2][0] + 2 == piece_locations[i+3][0] + 3 and piece
    #lolwtf am i doing

def is_loss(state):
    return 0

def is_terminal(state):
    if is_win(state):
        return 1
    elif is_loss(state):
        return -1
    return 0

def find_sequence(character, state): #character = x or o
    i = 0
    j = 0
    for row in state:
        for index in row:
            if index == character:
                j = index


def examine_neightbors(x, y, sequence, character, state):
    if sequence == 3:
        return True
    for i = x - 1: i <= x + 1: i++:
        for j = y - 1: y <= y + 1: j++:
            if not (i == x and j == y):
                if state[i][j] == character:
                    examine_neightbors(i, j, sequence + 1, character, state)


def get_best_valid_move(state):
    return 0

def is_move_valid(state, move):
    x = move[0]
    if x < 0 or x > 6:
        return False
    y = move[1]
    if y < 0 or y > 6:
        return False
    direction = move[2]
    if direction == "N":
        y += 1
    elif direction == "E":
        x += 1
    elif direction == "S":
        y -= 1
    elif direction == "W":
        x -= 1
    else:
        return False
    if x < 0 or x > 6 or y < 0 or y > 6:
        return False
    if state[x][y] == " ":
        return True
    else:
        return False

def minimax(state):
    return 0

def state_value(state):
    if is_win(state):
        return 1
    elif is_loss(state):
        return -1
    else:
        return 0

def board_init(dimension, state):
    if state is not None:
        return state
    board = []
    return board + [" "] * dimension ** 2

def find_all_moves(state):
    i = 0
    piece_locations = []
    for row in state:
        j = 0
        for index in row:
            if index == "X": #need to figure out how to define this guy to vary accoriding to colour
                piece_locations.append((i, j))
            j += 1
        i += 1
    return 0

def apply_move(state, move):
    return 0

def compute_score(state):
    return 0

def make_tree(state, root):
    if root is None:
        root = Node(state, compute_score(state), None, [])
    all_moves = find_all_moves(state)
    for move in all_moves:
        new_state = apply_move(state, move)
        next_root = Node(new_state, compute_score(new_state), root, [])
        make_tree(state, next_root)
        root.children.append(next_root)


def make_move(state):
    return "" + str(random.randint % 7) + str(random.randint % 7) + moves[random.randint % 3]

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

game_board = board_init(7, default_state)
# print game_board

is_win(game_board)