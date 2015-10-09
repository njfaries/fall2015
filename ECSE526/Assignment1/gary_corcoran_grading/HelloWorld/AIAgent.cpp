/*
 * AIAgent.cpp
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#include "AIAgent.h"
#include <iostream>

AIAgent::AIAgent(char _ai_player, char _human_player, int size, int _win_connections, clock_t _start, double _duration, std::string text_file) {
	ai_player = _ai_player;
	human_player = _human_player;
	boardDimensions = size;
	win_connections = _win_connections;
	start = _start;
	moveDuration = _duration;
	gameTree = new GST();
	Board* board = new Board(size);
	board->inputGameBoard(text_file);
	gameTree->insert(*board);
	gameTree->getRoot()->board->printBoard();
}

AIAgent::~AIAgent() {
}

void AIAgent::playGame() {
	if (human_player == WHITE) {
		pMove playersMove = gameTree->getRoot()->board->getPlayerMove(human_player);
		while (!gameTree->getRoot()->board->checkAndMove(human_player, playersMove)) {
			std::cout << "Move invalid, please input valid move." << std::endl;
			gameTree->getRoot()->board->printBoard();
			playersMove = gameTree->getRoot()->board->getPlayerMove(human_player);
		}
		std::cout << "Move is valid move." << std::endl;
		gameTree->getRoot()->board->printBoard();
	}
	while (gameTree->getRoot()->board->checkWin(win_connections) != ai_player ||
			gameTree->getRoot()->board->checkWin(win_connections) != human_player) {
		Action _action = iterativeDeepeningSearch();
//		float duration = clock() - start;
//		std::cout << "Time for move = ";
//		std::cout << ((float)duration)/CLOCKS_PER_SEC << " seconds." << std::endl;
		gameTree->getRoot()->board->setValue(_action.x, _action.y, ai_player);
		// set previous value on board to empty
		if (gameTree->getRoot()->board->getValue(_action.x - 1, _action.y) == ai_player){
			gameTree->getRoot()->board->setValue(_action.x - 1, _action.y, EMPTY);
			// reset score of root to 0
			gameTree->getRoot()->action.score = 0;
		}
		else if (gameTree->getRoot()->board->getValue(_action.x + 1, _action.y) == ai_player){
			gameTree->getRoot()->board->setValue(_action.x + 1, _action.y, EMPTY);
			// reset score of root to 0
			gameTree->getRoot()->action.score = 0;
		}
		else if (gameTree->getRoot()->board->getValue(_action.x, _action.y - 1) == ai_player){
			gameTree->getRoot()->board->setValue(_action.x, _action.y - 1, EMPTY);
			// reset score of root to 0
			gameTree->getRoot()->action.score = 0;
		}
		else if (gameTree->getRoot()->board->getValue(_action.x, _action.y + 1) == ai_player){
			gameTree->getRoot()->board->setValue(_action.x, _action.y + 1, EMPTY);
			// reset score of root to 0
			gameTree->getRoot()->action.score = 0;
		}
		std::cout << std::endl;
		std::cout << "Current Board" << std::endl;
		gameTree->getRoot()->board->printBoard();
		pMove playersMove = gameTree->getRoot()->board->getPlayerMove(human_player);
		while (!gameTree->getRoot()->board->checkAndMove(human_player, playersMove)) {
			std::cout << "Move invalid, please input valid move." << std::endl;
			gameTree->getRoot()->board->printBoard();
			playersMove = gameTree->getRoot()->board->getPlayerMove(human_player);
		}
		std::cout << "Move is valid move." << std::endl;
		gameTree->getRoot()->board->printBoard();
		// get current root
		Board* newRoot = new Board(*gameTree->getRoot()->board);
		// clear previous game tree
		gameTree->clearTree();
		gameTree->insert(*newRoot);
	}
//	if (gameTree->getRoot()->board->checkWin(win_connections) == ai_player)
//		std::cout << "AI Agent has defeated human player." << std::endl;
//	else std::cout << "Human player has defeated AI agent player." << std::endl;
	std::cout << "Done" << std::endl;
}


Action AIAgent::iterativeDeepeningSearch() {
	int depth = 1;
	depthLimitedSearch(depth);
	int score = alphaBetaSearch(gameTree->getRoot(), -1000000000, 100000000, ai_player);
	Action _action = findMove(score);
	for (; depth < 6; depth++) {
		depthLimitedSearch(depth);
		score = alphaBetaSearch(gameTree->getRoot(), -1000000000, 100000000, ai_player);
		_action = findMove(score);
		if (score == 10000000) {
			return _action;
		}
	}
	return _action;
}

/* depthLimiedSearch *****************************************************************************************************
 *
 * @params: limit - integer value of cut off value for depth limited search @pre: > 1
 *
 * @modifies: this function calls resursiveDLS
 *
 * @returns: returns an action consisting of best move, (x, y), along with score
 ************************************************************************************************************************/
void AIAgent::depthLimitedSearch(int limit, Action _action) {
	resursiveDLS(ai_player, gameTree->getRoot(), limit, _action);
}

/* resursiveDLS *********************************************************************************************************
 *
 * @params: player - char value of the current player @pre: ai_player || human_player
 * 			node - pointer to current GSTNode
 * 			limit - integer value of cut off value for depth limited search @pre: > 1
 *
 * @modifies: creates game tree consisting of nodes for the depth limited search
 *
 * @returns: nothing
 ************************************************************************************************************************/
void AIAgent::resursiveDLS(char player, GSTNode* node, int limit, Action best_move) {
	// check for base cases
	char winner = node->board->checkWin(win_connections);
	if (winner == ai_player) {
		node->action.score = 10000000;
		return;
	}
	else if (winner == human_player) {
		node->action.score = -10000000;
		return;
	}
	else if (limit == 0) {
		node->action.score = heuristic(*node->board);
		return;
	}
	// if no action from alpha best pruning is given
	if (best_move.x == 0 || best_move.y == 0) {
		// recursive call
		for (int i = 1; i <= boardDimensions; i++) {
			for (int j = 1; j <= boardDimensions; j++) {
				if (((node->board->getValue(i, j) == EMPTY)) && (node->board->getValue(i, j - 1) == player
						|| node->board->getValue(i, j + 1) == player || node->board->getValue(i - 1, j) == player
						|| node->board->getValue(i + 1, j) == player)) {
					// deep copy of node
					Board* _board = new Board(*node->board);
					if (_board->getValue(i + 1, j) == player)
						_board->setValue(i + 1, j, EMPTY);
					else if (_board->getValue(i - 1, j) == player)
						_board->setValue(i - 1, j, EMPTY);
					else if (_board->getValue(i, j + 1) == player)
						_board->setValue(i, j + 1, EMPTY);
					else if (_board->getValue(i, j - 1) == player)
						_board->setValue(i, j - 1, EMPTY);
					_board->setValue(i, j, player);
					gameTree->insert(*_board, node);
					GSTNode* pTemp = node->childPtr;
					// if we are already reached a terminal node
					while (pTemp->siblingPtr != nullptr) {
						pTemp = pTemp->siblingPtr;
					}
					pTemp->action.x = i;
					pTemp->action.y = j;
					if (player == ai_player) {
						resursiveDLS(human_player, pTemp, limit - 1);
					}
					else {
						resursiveDLS(ai_player, pTemp, limit - 1);
					}
					node->board->setValue(i, j, EMPTY);
				}
			}
		}
	}
	return;
}


/* heuristic *******************************************************************************************
 *
 * @params: _board - Board object that corresponds to current game board
 *
 * @modifies: nothing
 *
 * @returns: returns integer value of evaluated game board
 *******************************************************************************************************/
int AIAgent::heuristic(Board _board) {
	int score = checkAdjacent(_board);
	score += checkDistance(_board);
	return score;
}

// check distance between each piece for ai agent
int AIAgent::checkDistance(Board _board) {
	int tally = 0;
	int row, col = 0;
	int counter = 1;
	for (int i = 1; i <= boardDimensions; i++) {
		for (int j = 1; j <= boardDimensions; j++) {
			if (_board.getValue(i, j) == ai_player) {
				// check right
				row = i;
				col = j;
				// find closest AI's token to the right
				while ((_board.getValue(i, ++col) != ai_player) && (col <= boardDimensions)) {
					counter++;
				}
				// check if we exited loop because we ran off the board, if so, reset counter
				if (col > boardDimensions)
					counter = 1;
				else {
					tally -= counter;
				}
				// reset parameters
				counter = 1;
				row = i;
				col = j;
				// find closest AI's token to the up
				while ((_board.getValue(--row, col) != ai_player) && (row >= 1)) {
					counter++;
				}
				// check if we exited loop because we ran off the board, if so, reset counter
				if (row < 1)
					counter = 1;
				else {
					tally -= counter;
				}
				// reset parameters
				counter = 1;
				row = i;
				col = j;
				// find closest AI's token to the diagonal (+45 degrees)
				while ((_board.getValue(--row, ++col) != ai_player) && (row >= 1) && (col <= boardDimensions)) {
					counter++;
				}
				// check if we exited loop because we ran off the board, if so, reset counter
				if (col > boardDimensions)
					counter = 1;
				else {
					tally -= (2 * (counter - 1) + 1);
				}
				// reset parameters
				counter = 1;
				row = i;
				col = j;
				// find closest AI's token to the diagonal (+135 degrees)
				while ((_board.getValue(--row, --col) != ai_player) && (row >= 1) && (col >= 1)) {
					counter++;
				}
				// check if we exited loop because we ran off the board, if so, reset counter
				if (row < 1 || col < 1)
					counter = 1;
				else {
					tally -= (2 * (counter - 1) + 1);
				}
			}
		}
	}
	return tally * 20;
}


/* checkAdajacent ************************************************************************************************
 *
 * @params: _board - the board you want to check for clusters for AI tokens and potential clusters of human tokens
 * 			_row - pass by reference integer row, this row will correspond to a placement where we have 3 or more
 * 				tokens
 * 			_col - same as _row, however, it is the column value
 *
 * @modifies: nothing
 *
 * @returns: returns the score of the board
 *****************************************************************************************************************/
int AIAgent::checkAdjacent(Board _board) {
	int row, col = 0;
	int counter = 1;
	int tally = 0;
	for (int i = 1; i <= boardDimensions; i++) {
		for (int j = 1; j <= boardDimensions; j++) {
			// check for AI clusters
			if (_board.getValue(i, j) == ai_player) {
				// check right
				row = i;
				col = j;
				while (_board.getValue(i, ++col) == ai_player) {
					counter++;
					if (counter == 2)
						tally += 300;
					else if (counter == 3) {
						tally += 800;
					}
				}
				// reset parameters
				counter = 1;
				row = i;
				col = j;
				// check up
				while (_board.getValue(--row, j) == ai_player) {
					counter++;
					if (counter == 2)
						tally += 300;
					else if (counter == 3)
						tally += 800;
				}
				counter = 1;
				row = i;
				col = j;
				// check diagonal +45 degrees
				while (_board.getValue(--row, ++col) == ai_player) {
					counter++;
					if (counter == 2)
						tally += 300;
					else if (counter == 3)
						tally += 800;
				}
				counter = 1;
				row = i;
				col = j;
				// check diagonal +135 degrees
				while (_board.getValue(--row, --col) == ai_player) {
					counter++;
					if (counter == 2)
						tally += 300;
					else if (counter == 3)
						tally += 800;
				}
			}
			row = i;
			col = j;
			// check for human clusters
			if (_board.getValue(i, j) == human_player) {
				// check right
				if ((_board.getValue(i, j + 2) == human_player) && (_board.getValue(i, j + 1) == EMPTY))
					tally += -80;
				// check up
				else if ((_board.getValue(i - 2, j) == human_player) && (_board.getValue(i - 1, j) == EMPTY))
					tally += -80;
				// check diagonal +45
				else if ((_board.getValue(i - 2, j + 2) == human_player) && (_board.getValue(i - 1, j + 1) == EMPTY))
					tally += -80;
				// check diagonal +135
				else if ((_board.getValue(i - 2, j - 2) == human_player) && (_board.getValue(i - 1, j - 1) == EMPTY))
					tally += -80;
			}
		}
	}
	return tally;
}

/* findMove **********************************************************************************************
 *
 * @params: _score - integer score value of root node after minimax algorithm
 *
 * @modifies: nothing
 *
 * @returns: returns action move corresponding to _score from minimax algorithm
 *********************************************************************************************************/
Action AIAgent::findMove(int _score) {
	// find action corresponding to best score
	GSTNode* pTemp = gameTree->getRoot();
	pTemp = pTemp->childPtr;
	if (pTemp->action.score == _score) {
		Action _action;
		_action.x = pTemp->action.x;
		_action.y = pTemp->action.y;
		_action.score = pTemp->action.score;
		return _action;
	}
	else {
		while (pTemp->siblingPtr != nullptr) {
			if (pTemp->siblingPtr->action.score == _score) {
				Action _action;
				_action.x = pTemp->siblingPtr->action.x;
				_action.y = pTemp->siblingPtr->action.y;
				_action.score = pTemp->siblingPtr->action.score;
				return _action;
			}
			pTemp = pTemp->siblingPtr;
		}
	}
	// should never reach this point
	Action _action;
	_action.x = 0;
	_action.y = 0;
	_action.score = 0;
	return _action;
}

/* alphaBetaSearch ************************************************************************************************************
 *
 * @params: player - char value representing current player @pre: ai_player || human_player
 * 			node - GSTNode pointer to current node you are applying the minimax algorithm to
 *
 * @modifies: updates node's action score to min/max of children nodes depending on minimax
 *
 * @returns: returns node's action score
 **********************************************************************************************************************/
int AIAgent::alphaBetaSearch(GSTNode* node, int alpha, int beta, char player) {
	// if depth is 0 or node is a terminal node
	if (node->childPtr == nullptr) {
		// return heuristic value of node
		return node->action.score;
	}
	if (player == ai_player) {
		GSTNode* pTemp = node->childPtr;
		while (pTemp != nullptr) {
			int temp = alphaBetaSearch(pTemp, alpha, beta, human_player);
			alpha = (temp > alpha) ? temp : alpha;
			if (beta <= alpha)
				break;
			pTemp = pTemp->siblingPtr;
		}
		node->action.score = alpha;
		return alpha;
	}
	else {
		GSTNode* pTemp = node->childPtr;
		while (pTemp != nullptr) {
			int temp = alphaBetaSearch(pTemp, alpha, beta, ai_player);
			beta = (temp < beta) ? temp : beta;
			if (beta <= alpha)
				break;
			pTemp = pTemp->siblingPtr;
		}
		node->action.score = beta;
		return beta;
	}
}
