/*
 * Board.h
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#ifndef BOARD_H_
#define BOARD_H_

#include <string>

// cells that make up game board
struct Cell {
	Cell() {};
	Cell(int _row, int _col, char _value) {
		row = _row;
		col = _col;
		value = _value;
	}
	int row;
	int col;
	char value;
};

// structure that makes up player's input move
struct pMove {
	pMove() {
		row = 0;
		col = 0;
		// set random number, this will be replaced when used
		direction = 'G';
	};
	pMove(int _row, int _col, char _direction) {
		row = _row;
		col = _col;
		direction = _direction;
	};
	int row;
	int col;
	char direction;
};

const int MAX_SIZE = 100;

// set of constants
const char BLACK = 'X';
const char WHITE = 'O';
const char EMPTY = ' ';

class Board {
public:
	Board(int size);
	Board(const Board& obj);
	~Board();
	void inputGameBoard(std::string text_file);
	void printBoard();
	char getValue(int row, int col);
	void setValue(int row, int col, char value);
	const char checkWin(int connections);
	pMove getPlayerMove(char player);
	bool checkAndMove(char player, pMove playerMove);
	void deleteGameBoard();
	int dimensions;
private:
	Cell* gameBoard;
};

#endif /* BOARD_H_ */
