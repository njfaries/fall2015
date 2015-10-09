#!/usr/bin/env python
#
#Purely for Human vs AI games
#
#Submitted Sept 30, 2015
#
#McGill University
#ECSE 526 Artificial Intelligence
#
#author: Russell Buchanan
#email: russell.buchanan@mail.mcgill.ca

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE = "mytestgame black \n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

while(1):
	print 'Your Move'
	columnMove = raw_input("Column: ")
	while columnMove not in ['1','2','3','4','5','6','7']:
		columnMove = raw_input('Please enter Column')

	rowMove = raw_input("Row: ")
	while rowMove not in ['1','2','3','4','5','6','7']:
		rowMove = raw_input('Please enter a Row')

	dirMove = raw_input("Direction (NSEW): ")
	while dirMove not in ['n','N','s','S','e','E','w','W']:
		dirMove = raw_input('Please enter a cardinal direction')

	if dirMove == 'n':
		dirMove = 'N'
	if dirMove == 's':
		dirMove = 'S'
	if dirMove == 'e':
		dirMove = 'E'
	if dirMove == 'w':
		dirMove = 'W'

	move = [columnMove,rowMove,dirMove,'\n']
	MESSAGE = ''.join(move)

	s.send(MESSAGE)

	data = s.recv(BUFFER_SIZE)
	print "received data:", data


s.close()





