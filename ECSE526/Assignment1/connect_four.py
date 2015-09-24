__author__ = 'nathaniel'

import random
import socket

default_state = \
    [[" ", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", "X"],
     ["X", " ", " ", " ", " ", " ", "O"],
     ["O", " ", " ", " ", " ", " ", " "]
     ]

moves = ["N", "E", "S", "W"]


def minimax(state):
    return 0


def board_init(dimension, state):
    if state is not None:
        return state
    board = []
    return board + [" "] * dimension ** 2

def make_move():
    return "" + str(random.randint % 7) + str(random.randint % 7) + moves[random.randint % 3]


TCP_PORT = 12345
TCP_IP = '127.0.0.1'
colour = "white"
MESSAGE = "mytestgame " + colour + "\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(1024)
s.close()

print "received data:", data

game_board = board_init(7, default_state)
print game_board
