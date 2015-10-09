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
QUESTION_ONE_A   = (0,2,3,3,2,5,4,4,4,6,5,5
				   ,2,2,3,6,5,4,6,3,6,4,6,5)
QUESTION_ONE_B   = (0,0,1,0,0,6,3,3,4,4,5,2
				   ,0,1,2,2,2,3,1,5,5,4,6,3)
QUESTION_ONE_C	 = (2,0,2,1,2,5,4,2,4,3,4,6
				   ,2,2,2,3,2,6,4,0,4,1,4,5)

STATES_EXPLORED = 0

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

def getHeuristic(s):
	#Returns heuristic value for a given state
	BOARD = build_board(s, 1)
	heuristic = 0
	#Check for vertical four in a row
	for k in range(0,11,2):
		if s[k+1]>=3:
			if BOARD[s[k]][s[k+1]-1]=='O':
				if BOARD[s[k]][s[k+1]-2]=='O':
					if BOARD[s[k]][s[k+1]-3]=='O':
						heuristic +=  10000# four in a row
					else:
						heuristic +=  50# three in a row
				else:
					heuristic +=  20# two in a row
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
	#Check for backward diagonal four in a row
		if s[k]>=3 and s[k+1]>=3:
			if BOARD[s[k]-1][s[k+1]-1]=='O':
				if BOARD[s[k]-2][s[k+1]-2]=='O':
					if BOARD[s[k]-3][s[k+1]-3]=='O':
						heuristic +=  10000# four in a row
					else:
						heuristic +=  50# three in a row
				else:
					heuristic +=  20# two in a row
	#Additional heuristic for tie breaking
	#Specific values for each column, favouring pieces closer to the center
	#Favours pieces in the center the same as two in a row
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
	heuristic = getHeuristic(curState)
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
	heuristic = getHeuristic(curState)
	if heuristic >= 5000 or heuristic <= -5000 or curDepth == depthLimit:
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

player = 'white'
print "Hello, my name is Mycroft"
algo = raw_input('Would you like to use Alpha/Beta pruning? (y/n)')
if algo == 'y':
	print algo

while algo not in ['y','Y','n','N']:
	algo = raw_input('Please answer y or n')

curState = QUESTION_ONE_A#Modify this for each question
build_board(curState,0)

if algo not in ['n','N']:
	print 'Using Alpha Beta pruning'
	start = time.time()
	mycroftMove = myAlphaBeta(curState, 0, 4, player,-10000,10000)
	end = time.time()
else:
	print 'Using Minimax'
	start = time.time()
	mycroftMove = myMiniMax(curState, 0, 6, player)
	end = time.time()

print STATES_EXPLORED,
print' States Explored'
print end - start,
print "Seconds"