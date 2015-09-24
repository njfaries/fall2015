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

def is_win(state):
    i = 0
    piece_locations = []
    for row in state:
        j = 0
        for index in row:
            if index == "X":
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

def minimax(state):
    return 0


def board_init(dimension, state):
    if state is not None:
        return state
    board = []
    return board + [" "] * dimension ** 2

def make_move():
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