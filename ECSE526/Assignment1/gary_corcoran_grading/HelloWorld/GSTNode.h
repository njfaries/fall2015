/*
 * GSTNode.h
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#ifndef GSTNODE_H_
#define GSTNODE_H_

#include "Board.h"

// score and move of each game board in tree
struct Action {
	Action() {
		score = 0;
		x = 0;
		y = 0;
	}
	int score;
	int x;
	int y;
};

class GSTNode {
public:
	GSTNode(int size) {
		childPtr = nullptr;
		siblingPtr = nullptr;
		action.x = 0;
		action.y = 0;
		action.score = 0;
		board = new Board(size);
	}
	// deep copy constructor
	GSTNode(Board _board) {
		childPtr = nullptr;
		siblingPtr = nullptr;
		action.x = 0;
		action.y = 0;
		action.score = 0;
		// copy board into tree node
		board = new Board(_board);
	}
	~GSTNode() {
		childPtr = nullptr;
		siblingPtr = nullptr;
		delete board;
	}
	GSTNode* childPtr;
	GSTNode* siblingPtr;
	Board* board;	// each node has an empty game board
	Action action;
};

#endif /* GSTNODE_H_ */
