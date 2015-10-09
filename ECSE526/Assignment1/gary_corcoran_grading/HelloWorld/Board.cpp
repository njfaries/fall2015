/*
 * Board.cpp
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#include "Board.h"
#include <iostream>
#include <string>
#include <fstream>

/* Board ********************************************************************************
 *
 * @params: size - integer number representing width or height of square game board
 *
 * @modifies: a game board of MAX_SIZE consisting of Cell(0, 0, 'Z')
 *
 * @returns: nothing
 ****************************************************************************************/
Board::Board(int size) {
	// requests amount of space
	if ((gameBoard = new Cell[size * size])) {
		for (int i = 0; i < size * size; i++) {
			gameBoard[i] = Cell(0, 0, EMPTY);
		}
		dimensions = size;
	}
	else {
		gameBoard = 0;
		dimensions = 0;
	}
}

/* Board Copy Constructor**********************************************************************
 *
 * @params: none
 *
 * @modifies: performs deep copy of original game board
 *
 * @returns: nothing
 ****************************************************************************************/
Board::Board(const Board& original) {
	// requests amount of space
	if ((gameBoard = new Cell[original.dimensions * original.dimensions])) {
		dimensions = original.dimensions;
		// copy original's heap data
		for (int i = 0; i < dimensions * dimensions; i++) {
			*(gameBoard + i) = *(original.gameBoard + i);
		}
	}
	else dimensions = 0;
}

/* ~Board ********************************************************************************
 *
 * @params: none
 *
 * @modifies: clears game board
 *
 * @returns: nothing
 ****************************************************************************************/
Board::~Board() {
	dimensions = 0;
	delete[] gameBoard;
}

/* inputGameBoard ***********************************************************************
 *
 * @params: string of input text file consisting of game board layout
 * 				@pre: cannot be empty string
 *
 * @modifies: Sets the initial position of the game board corresponding to the input
 * 			text file game board. It then stores this into the game board array,
 * 			game_board
 *
 * @returns: nothing
 ****************************************************************************************/
void Board::inputGameBoard(std::string text_file) {
	std::cout << "Beginning Game of Dynamic Connect Four!" << std::endl;
	std::cout << "Player White is 'O', Player Black is 'X'" << std::endl;
	std::string line;
	int count = 0;	// keep count of the rows
	int counter = 0; // used to index array
	std::ifstream myfile(text_file);
	if (myfile.is_open()) {
	    while (getline (myfile,line)) {
	    	for (int i = 0; i < line.length(); i++) {
	    		if (line[i] == EMPTY || line[i] == BLACK || line[i] == WHITE) {
	    			gameBoard[counter] = (Cell(i + 1, count + 1, line[i]));
	    			counter++;
	    		}
	    	}
	    	count++;
	    }
	    myfile.close();
	}
	else std::cout << "Unable to open file";
}

/* printBoard *****************************************************************************************
 *
 * @params: none
 *
 * @modifies: output game board to console window
 *
 * @returns: nothing
 *****************************************************************************************************/
void Board::printBoard() {
	std::cout << " ";
	for (int i = 1; i <= dimensions; i++)
		std::cout << i << " ";
	std::cout << std::endl;
	for (int i = 1; i <= dimensions; i++) {
		std::cout << i;
		for (int j = 1; j < dimensions; j++) {
			std::cout << getValue(i, j);
			std::cout << ",";
		}
		std::cout << getValue(i, dimensions);
		std::cout << std::endl;
	}
}

/* getValue ********************************************************************************************
 *
 * @params: row - integer row values
 * 			col - integer column value
 *
 * @returns: returns value at (row, col), if row or col is outside dimensions
 * 				of the board, return false;
 *****************************************************************************************************/
char Board::getValue(int row, int col) {
	if (row < 1 || row > dimensions || col < 1 || col > dimensions)
		return false;
	return gameBoard[(row - 1) * dimensions + col - 1].value;
}

/* setValue *********************************************************************************************
 *
 * @params: row - integer corresponding to row
 * 				@pre: 0 < row <= dimensions
 * 			col - integer corresponding to col
 * 				@pre: 0 < col <= dimensions
 * 			value - char value of the piece you want to set
 * 				@pre: WHITE || BLACK || EMPTY
 *
 * @modifies: sets piece at coordinates row, col
 *
 * @returns: nothing
 *****************************************************************************************************/
void Board::setValue(int row, int col, char value) {
	gameBoard[(row - 1) * dimensions + col - 1].value = value;
}

/* checkWin *******************************************************************************************
 *
 * @params: connections - integer number of connections needed for win
 * 				@pre: > 1
 *
 * @returns: checks if there are connectNum connected tokens either horizontally, vertically,
 * 			 or diagonally. If W_PLAYER wins, return 'O', if B_PLAYER wins return 'X',
 * 			 else return false.
 *******************************************************************************************************/
const char Board::checkWin(int connections) {
	int row, col = 0;
	char pColour;
	int counter = 1;	// counts how many tokens are connected
	for (int i = 1; i <= dimensions; i++) {
		for (int j = 1; j <= dimensions; j++) {
			if (getValue(i, j) == BLACK || getValue(i, j) == WHITE) {
				pColour = getValue(i, j);
				// check right
				row = i;
				col = j;
				while (getValue(i, ++col) == pColour) {
					counter++;
					if (counter == connections)
						return pColour;
				}
				// reset parameters
				row = i;
				col = j;
				counter = 1;	// reset counter
				// check up
				while (getValue(--row, j) == pColour) {
					counter++;
					if (counter == connections)
						return pColour;
				}
				// reset parameters
				row = i;
				col = j;
				counter = 1;
				// check for diagonal win (+45 degrees)
				while (getValue(++row, --col) == pColour) {
					counter++;
					if (counter == connections)
						return pColour;
				}
				// reset parameters
				row = i;
				col = j;
				counter = 1;
				// check for diagonal win (+135 degrees)
				while (getValue(--row, --col) == pColour) {
					counter++;
					if (counter == connections)
						return pColour;
				}
			}
		}
	}
	return false;
}

/* getPlayerMove **************************************************************************************
 *
 * @params: char player - char number corresponding to player's move
 * 				@pre: WHITE || BLACK
 *
 * @returns: returns string corresponding to user's input
 ******************************************************************************************************/
pMove Board::getPlayerMove(char playersTurn) {
	std::cout << std::endl;
	if (playersTurn == WHITE) {
		std::cout << "White: Please input player move " << std::endl;
	}
	else {
		std::cout << "Black: Please input player move." << std::endl;
	}
	std::cout << "in the form of Col-Row-Direction (e.g. 71W)." << std::endl;
	std::string playerMove;
	std::cin >> playerMove;
	std::cout << "Your move was " << playerMove << std::endl;
	pMove player_move;
	player_move.col = playerMove[0] - 48;
	player_move.row = playerMove[1] - 48;
	player_move.direction = playerMove[2];
	return player_move;
}

/* checkAndMove ****************************************************************************************
 *
 * @params: char player - char depicting player's turn
 * 				@pre: BLACK || WHITE
 * 			pMove playerMove - player move consisting of row, col, and direction
 *
 * @returns: returns true if string is a valid move, else, return false
 *******************************************************************************************************/
bool Board::checkAndMove(char player, pMove playerMove) {
	char pColour;
	pColour = (player == WHITE) ? WHITE : BLACK;
	// check if input coordinates are inside game board
	if (playerMove.row > 0 && playerMove.row <= dimensions &&
			playerMove.col > 0 && playerMove.col <= dimensions) {
		// check if the player's piece sits at input coordinates
		if (getValue(playerMove.row, playerMove.col) == pColour) {
			// check direction
			if (playerMove.direction == 'N') {
				if (playerMove.row > 1 && getValue(--playerMove.row, playerMove.col) == EMPTY) {
					setValue(playerMove.row, playerMove.col, player);
					setValue(++playerMove.row, playerMove.col, EMPTY);
					return true;
				}
			}
			else if (playerMove.direction == 'S') {
				if (playerMove.row < dimensions && getValue(++playerMove.row, playerMove.col) == EMPTY) {
					setValue(playerMove.row, playerMove.col, player);
					setValue(--playerMove.row, playerMove.col, EMPTY);
					return true;
				}
			}
			else if (playerMove.direction == 'E') {
				if (playerMove.col < dimensions && getValue(playerMove.row, ++playerMove.col) == EMPTY) {
					setValue(playerMove.row, playerMove.col, player);
					setValue(playerMove.row, --playerMove.col, EMPTY);
					return true;
				}
			}
			if (playerMove.direction == 'W') {
				if (playerMove.col > 1 && getValue(playerMove.row, --playerMove.col) == EMPTY) {
					setValue(playerMove.row, playerMove.col, player);
					setValue(playerMove.row, ++playerMove.col, EMPTY);
					return true;
				}
			}
		}
	}
	return false;
}

void Board::deleteGameBoard() {
	delete[] gameBoard;
}
