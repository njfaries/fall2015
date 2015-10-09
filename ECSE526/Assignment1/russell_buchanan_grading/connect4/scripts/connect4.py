#!/usr/bin/env python
#
#A agent that plays a modified version of Connect 4
#
#Submitted Sept 30, 2015
#
#McGill University
#ECSE 526 Artificial Intelligence
#
#author: Russell Buchanan
#email: russell.buchanan@mail.mcgill.ca


import socket
import time


BEGINING_OF_GAME = (0,2,0,4,0,6,6,1,6,3,6,5
                   ,0,1,0,3,0,5,6,0,6,2,6,4)

STATES_EXPLORED = 0

TCP_PORT = 12345
BUFF_SIZE = 1024

TURN_NUM = 1

def whiteActions(s):
	#Returns all legal moves for the White player
	BOARD = build_board(s, 1)
	actions = []
	for i in range(0,11,2):
		if 0<=(s[i+1]-1):
			if BOARD[s[i]][s[i+1]-1] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "N"))
		if (s[i+1]+1)<=6:
			if BOARD[s[i]][s[i+1]+1] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "S"))
		if 0<=(s[i]-1):
			if BOARD[s[i]-1][s[i+1]] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "W"))
		if (s[i]+1)<=6:
			if BOARD[s[i]+1][s[i+1]] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "E"))

	return actions

def blackActions(s):
	#Returns all legal moves for the Black player
	BOARD = build_board(s, 1)
	actions = []
	for i in range(12,23, 2):
		if 0<=(s[i+1]-1):
			if BOARD[s[i]][s[i+1]-1] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "N"))
		if (s[i+1]+1)<=6:
			if BOARD[s[i]][s[i+1]+1] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "S"))
		if 0<=(s[i]-1):
			if BOARD[s[i]-1][s[i+1]] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "W"))
		if (s[i]+1)<=6:
			if BOARD[s[i]+1][s[i+1]] == " ":
				actions.insert(0, (1 + s[i], 1 + s[i+1], "E"))
	return actions

def result(s, a):
	#Returns the resulting state of applying an action
	global STATES_EXPLORED #Counts number of states expanded
	nState = [s[i] for i in range(24)]
	for k in range(0,23, 2):
		if s[k]==(a[0]-1) and s[k+1] == (a[1]-1):
			if a[2] == "N":
				nState[k] = s[k]
				nState[k+1] =s[k+1]-1
			if a[2] == "S":
				nState[k] = s[k]
				nState[k+1] =s[k+1]+1
			if a[2] == "W":
				nState[k] = s[k]-1
				nState[k+1] =s[k+1]
			if a[2] == "E":
				nState[k] = s[k]+1
				nState[k+1] =s[k+1]
	tnState = tuple(nState)	
	STATES_EXPLORED +=1
	return tnState

def getHeuristic(s,depth):
	#Returns heuristic value for a given state
	BOARD = build_board(s, 1)
	heuristic = 0
	#Check for vertical four in a row
	for k in range(0,11,2):
		if s[k+1]>=3:
			if BOARD[s[k]][s[k+1]-1]=='O':
				if BOARD[s[k]][s[k+1]-2]=='O':
					if BOARD[s[k]][s[k+1]-3]=='O':
						heuristic += 10000# four in a row
					else:
						heuristic += 50# three in a row
				else:
					heuristic += 20# two in a row
	for k in range(0,11,2):
	#Check for horizontal four in a row
		if s[k]>=3:
			if BOARD[s[k]-1][s[k+1]]=='O':
				if BOARD[s[k]-2][s[k+1]]=='O':
					if BOARD[s[k]-3][s[k+1]]=='O':
						heuristic +=  10000# four in a row
					else:
						heuristic +=  50# three in a row
				else:
					heuristic +=  20# two in a row
	for k in range(0,11,2):
	#Check for forward diagonal four in a row
		if s[k]>=3 and s[k+1]<=3:
			if BOARD[s[k]-1][s[k+1]+1]=='O':
				if BOARD[s[k]-2][s[k+1]+2]=='O':
					if BOARD[s[k]-3][s[k+1]+3]=='O':
						heuristic +=  10000# four in a row
					else:
						heuristic +=  50# three in a row
				else:
					heuristic +=  20# two in a row
	for k in range(0,11,2):
	#Check for backward diagonal four in a row
		if s[k]>=3 and s[k+1]>=3:
			if BOARD[s[k]-1][s[k+1]-1]=='O':
				if BOARD[s[k]-2][s[k+1]-2]=='O':
					if BOARD[s[k]-3][s[k+1]-3]=='O':
						heuristic +=  10000# four in a row
					else:
						heuristic +=  50# three in a row
				else:
					heuristic +=  20# two in a rowc
	#Additional heuristic for tie breaking
	#Specific values for each column, favouring pieces closer to the center
	#Favours pieces in the center the same as two in a row
	if depth > 1:
		for k in range (0,11,2):
			if s[k]==3:
				heuristic+=20
			elif s[k] == 2 or s[k] == 4:
				heuristic +=15
			elif s[k] == 1 or s[k] == 5:
				heuristic +=10
	#Check for vertical four in a row
	for k in range(12,23,2):
		if s[k+1]>=3:
			if BOARD[s[k]][s[k+1]-1]=='X':
				if BOARD[s[k]][s[k+1]-2]=='X':
					if BOARD[s[k]][s[k+1]-3]=='X':
						heuristic -= 10000# four in a row
					else:
						heuristic -= 50# four in a row
				else:
					heuristic -= 20# four in a row
	for k in range(12,23,2):
	#Check for horizontal four in a row
		if s[k]>=3:
			if BOARD[s[k]-1][s[k+1]]=='X':
				if BOARD[s[k]-2][s[k+1]]=='X':
					if BOARD[s[k]-3][s[k+1]]=='X':
						heuristic -= 10000# four in a row
					else:
						heuristic -= 50# four in a row
				else:
					heuristic -= 20# four in a row
	for k in range(12,23,2):
	#Check for forward diagonal four in a row
		if s[k]>=3 and s[k+1]<=3:
			if BOARD[s[k]-1][s[k+1]+1]=='X':
				if BOARD[s[k]-2][s[k+1]+2]=='X':
					if BOARD[s[k]-3][s[k+1]+3]=='X':
						heuristic -= 10000# four in a row
					else:
						heuristic -= 50# four in a row
				else:
					heuristic -= 20# four in a row
	for k in range(12,23,2):
	#Check for backward diagonal four in a row
		if s[k]>=3 and s[k+1]>=3:
			if BOARD[s[k]-1][s[k+1]-1]=='X':
				if BOARD[s[k]-2][s[k+1]-2]=='X':
					if BOARD[s[k]-3][s[k+1]-3]=='X':
						heuristic -= 10000# four in a row
					else:
						heuristic -= 50# four in a row
				else:
					heuristic -= 20# four in a row
	#Additional heuristic for tie breaking
	#Specific values for each column, favouring pieces closer to the center
	#Favours pieces in the center the same as two in a row
	if depth > 1:
		for k in range (12,23,2):
				if s[k]==3:
					heuristic -=20
				elif s[k] == 2 or s[k] == 4:
					heuristic -=15
				elif s[k] == 1 or s[k] == 5:
					heuristic -= 10
	return heuristic

##################################################################################################

def build_board(s, supress):
	#Simple function to "Build the Board"
	#Returns a 2x2 matrix representing the board based on state
	#Can print to terminal a visual representaiton ofthe board
	BOARD = [[' ' for i in range(7)]for j in range(7)]           
	for j in range(7):
		for i in range(7):
			for k in range(0,23, 2):
				if j == s[k] and i == s[k+1]:
					if k <= 11:
						BOARD[j][i] = "O"
					else:
						BOARD[j][i] = "X"
	if supress == 0:
		print
		print
		for i in range(8):
			if i!=0:
				print i, 
			for j in range(8):
				if i == 0 and j ==0:
					print ' ',
				elif i == 0:
					print (j), '',
				elif j!=0:
					print BOARD[j-1][i-1] + ',',
				if j == 7:
					print
		print
		print
	return BOARD


################################################################################
def myMiniMax(curState,curDepth,depthLimit,player):
	#My Minimax function, based on pseudocode from Wikipedia
	heuristic = getHeuristic(curState,curDepth)
	if heuristic >= 5000 or heuristic <= -5000 or curDepth == depthLimit:
		return heuristic

	if player == 'white':#Maximizing Player
		bestOutcome = -10000
		possibleMoves = whiteActions(curState)
		bestMove = possibleMoves[0]
		for i in range(len(possibleMoves)):#range(len(possibleMoves)-1,-1,-1): for reverse direction
			nextState = result(curState, possibleMoves[i])
			val = myMiniMax(nextState,curDepth+1, depthLimit, 'black')
			if val > bestOutcome:
				bestOutcome = val
				bestMove = possibleMoves[i]
		if curDepth == 0:
			return bestMove
		return bestOutcome
	else:#Minimizing Player
		bestOutcome = 10000
		possibleMoves = whiteActions(curState)
		bestMove = possibleMoves[0]
		for i in range(len(possibleMoves)):#range(len(possibleMoves)-1,-1,-1): for reverse direction
			nextState = result(curState, possibleMoves[i])
			val = myMiniMax(nextState, curDepth+1, depthLimit, 'white')
			if val < bestOutcome:
				bestOutcome = val
				bestMove = possibleMoves[i]
		if curDepth == 0:
			return bestMove
		return bestOutcome

################################################################################
def myAlphaBeta(curState, curDepth, depthLimit, player, alpha, beta):
	#My Alpha Beta Pruning algorithm function, based on pseudocode from Wikipedia
	heuristic = getHeuristic(curState, curDepth)

	if heuristic >= 10000 or heuristic <= -10000 or curDepth == depthLimit:
		return heuristic

	if player == 'white':#Maximizing Player
		possibleMoves = whiteActions(curState)
		bestMove = possibleMoves[0]
		for i in range(len(possibleMoves)):#range(len(possibleMoves)-1,-1,-1): for reverse direction
			nextState = result(curState, possibleMoves[i])
			val = myAlphaBeta(nextState,curDepth+1, depthLimit, 'black', alpha, beta)
			if val > alpha:
				alpha = val
				bestMove = possibleMoves[i]
			if beta <= alpha:
				break
		if curDepth == 0:
			return bestMove
		return alpha
	else:#Minimizing Player
		possibleMoves = blackActions(curState)
		bestMove = possibleMoves[0]
		if curDepth == 0:#Check for win in 1 move
			for i in range(len(possibleMoves)):
				nextState = result(curState, possibleMoves[i])
				heuristic = getHeuristic(curState, curDepth)
				if heuristic <=-10000:
					return possibleMoves[i]
		for i in range(len(possibleMoves)):#range(len(possibleMoves)-1,-1,-1): for reverse direction
			nextState = result(curState, possibleMoves[i])
			val = myAlphaBeta(nextState, curDepth+1, depthLimit, 'white', alpha, beta)
			if val < beta:
				beta = val
				bestMove = possibleMoves[i]
			if beta <= alpha:
				break
		if curDepth == 0:
			return bestMove
		return beta
################################################################################
#Basic User input for TCP scoket
#Mycroft is this program's AI
#Sherlock is the oponent's (A)I
print("Which colour for AI?")
colour =input("1. White or 2. Black? ")

TCP_IP = raw_input("Please Enter TCP IP address: ")
if TCP_IP == '':
	TCP_IP = '127.0.0.1'#default
print "TCP address: ",
print TCP_IP
GAME_ID = raw_input("Please Enter Game ID: ")
if GAME_ID == '':
	GAME_ID = "mytestgame"
print "Game ID:",
print GAME_ID

if colour == 1:
	player = 'white'
	limit = 4
else:
	player = "black"
	limit = 5


MSG = [GAME_ID, ' ', player, '\n']
MESSAGE = ''.join(MSG)

curState = BEGINING_OF_GAME
build_board(curState,0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send(MESSAGE)
data = s.recv(BUFF_SIZE)#Recieve echo for confirmation of send
while(len(data)<4):
	time.sleep(1)
	s.send(MESSAGE)
	data = s.recv(BUFF_SIZE)

if player == 'black':#Wait for White Player's first move
	data = s.recv(BUFF_SIZE)
	while(len(data)<4):
		time.sleep(1)
		data = s.recv(BUFF_SIZE)

	sherlockMove = (int(data[0]),int(data[1]),data[2])
	print 'Oponent\'s move',
	print sherlockMove
	nextState = result(curState, sherlockMove)
	build_board(nextState,0)
	curState = nextState

#Hard coded for three first moves
#Strategy based on research of best opening moves
while(TURN_NUM<=2):

	if player == 'white':
		if TURN_NUM == 1:
			mycroftMove = (1,5,'E')
		if TURN_NUM == 2:
			mycroftMove = (7,6,'W')
	else:
		if TURN_NUM == 1:
			for k in range (0,11,2):
				if curState[k] == 1:
					mycroftMove = (1,curState[k+1],'E')
					break
				elif curState[k] == 5:
					mycroftMove = (7,curState[k+1],'W')
				else:
					mycroftMove = (7,5,'W')

		if TURN_NUM == 2:
			mycroftMove = myAlphaBeta(curState, 0, limit, player,-10000,10000)#Too many choices at this point

	print 'Mycroft\'s move:',
	print mycroftMove
	print STATES_EXPLORED,
	print'States Explored'

	nextState = result(curState, mycroftMove)
	build_board(nextState,0)
	curState = nextState

	mycroftMove = [str(mycroftMove[0]),str(mycroftMove[1]),mycroftMove[2],'\n']
	mycroftMove = ''.join(mycroftMove)

	s.send (mycroftMove)
	data = s.recv(BUFF_SIZE)#Recieve echo for confirmation of send
	while(len(data)<4):
		time.sleep(1)
		s.send (mycroftMove)
		data = s.recv(BUFF_SIZE)

	data = s.recv(BUFF_SIZE)#Listening for oponent's move
	while(len(data)<4):
		time.sleep(1)
		data = s.recv(BUFF_SIZE)

	sherlock = (int(data[len(data)-4]),int(data[len(data)-3]),data[len(data)-2]) 

	print 'Oponent\'s move',
	print sherlock
	nextState = result(curState, sherlock)
	build_board(nextState,0)

	curState = nextState
	TURN_NUM +=1

#Now the implementation of Apha Beta Pruning
while(1):
	STATES_EXPLORED = 0
	start = time.time()
	mycroftMove = myAlphaBeta(curState, 0, limit, player,-10000,10000)
	end = time.time()

	print player,
	print 'Move:',
	print mycroftMove
	print STATES_EXPLORED,
	print'States Explored'
	print end - start,
	print "Seconds"

	nextState = result(curState, mycroftMove)
	build_board(nextState,0)
	curState = nextState

	mycroftMove = [str(mycroftMove[0]),str(mycroftMove[1]),str(mycroftMove[2]),'\n']
	mycroftMove = ''.join(mycroftMove)

	s.send (mycroftMove)
	data = s.recv(BUFF_SIZE)#Recieve echo for confirmation of send
	while(len(data)<4):
		time.sleep(1)
		s.send (mycroftMove)

	#Need to check twice for end of game
	#For when the AI is playing against itself
	if getHeuristic(curState,1) >= 5000:
		print'Game Over, White Wins'
		break
	elif getHeuristic(curState,1) <= -5000:
		print'Game Over, Black Wins'
		break

	data = s.recv(BUFF_SIZE)#Listening for oponent's move
	while(len(data)<4):
		time.sleep(1)
		data = s.recv(BUFF_SIZE)

	#Need to check twice for end of game
	#For when the AI is playing against itself
	if getHeuristic(curState,1) >= 5000:
		print'Game Over, White Wins'
		break
	elif getHeuristic(curState,1) <= -5000:
		print'Game Over, Black Wins'
		break

	sherlock = (int(data[len(data)-4]),int(data[len(data)-3]),data[len(data)-2]) 

	print 'Oponent\'s move',
	print sherlock

	nextState = result(curState, sherlock)
	build_board(nextState,0)
	curState = nextState


