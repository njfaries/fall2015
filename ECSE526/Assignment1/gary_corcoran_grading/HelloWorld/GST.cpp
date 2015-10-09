/*
 * GST.cpp
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#include "GST.h"
#include <iostream>

/* GST ********************************************************************************
 *
 * @params: none
 *
 * @modifies: creates root of game tree and sets pointer to null
 *
 * @returns: nothing
 ****************************************************************************************/
GST::GST() {
	root = nullptr;
}

/* ~GST ********************************************************************************
 *
 * @params: none
 *
 * @modifies: deletes full game board
 *
 * @returns: nothing
 ****************************************************************************************/
GST::~GST() {
	clearTree();
	delete root;
}

/* clearTree *****************************************************************************
 *
 * @params: none
 *
 * @modifies: calls postOrderDelete to delete game board
 *
 * @returns: nothing
 ****************************************************************************************/
void GST::clearTree() {
	postOrderDelete(root);
}

/* postOrderDelete ***********************************************************************
 *
 * @params: none
 *
 * @modifies: traverse game tree in post order and deletes each node
 *
 * @returns: nothing
 ****************************************************************************************/
void GST::postOrderDelete(GSTNode* node) {
	if (node != nullptr) {
		postOrderDelete(node->childPtr);
		GSTNode* pTemp = node->siblingPtr;
		delete node;
		postOrderDelete(pTemp);
	}
}

/* insert ********************************************************************************
 *
 * @params: _board - the game board being stored in tree node
 * 			parent - pointer to the parent node of where child is being inserted,
 * 				if parent is left blank, we created the root of tree
 *
 * @modifies: updates general search tree with node inserted
 *
 * @returns: nothing
 ****************************************************************************************/
void GST::insert(Board _board, GSTNode* parent) {
	// if no parent, create game tree root
	if (parent == nullptr)
		root = new GSTNode(_board);
	// if parent has no child
	else {
		if (parent->childPtr == nullptr) {
			parent->childPtr = new GSTNode(_board);
		}
		else {
			GSTNode* pTemp = parent->childPtr;
			while (pTemp->siblingPtr != nullptr) {
				pTemp = pTemp->siblingPtr;
			}
			pTemp->siblingPtr = new GSTNode(_board);
		}
	}
}

/* getRoot ******************************************************************************
 *
 * @params: none
 *
 * @returns: returns pointer to root node
 ****************************************************************************************/
GSTNode* GST::getRoot() {
	return root;
}

/* preOrder ******************************************************************************
 *
 * @params: none
 *
 * @modifies: outputs full general search tree in pre order
 *
 * @returns: nothing
 ****************************************************************************************/
void GST::preOrder() {
	_preOrder(root);
}

/* _preOrder *****************************************************************************
 *
 * @params: node - pointer to next node to output
 *
 * @modifies: outputs full game tree in pre order
 *
 * @returns: nothing
 ****************************************************************************************/
void GST::_preOrder(GSTNode* node) {
	if (node != nullptr) {
		// print this node
		node->board->printBoard();
		std::cout << "Action = (" << node->action.x << ", " << node->action.y << ", " <<
				node->action.score << ")." << std::endl;
		std::cout << std::endl;
		_preOrder(node->childPtr);
		_preOrder(node->siblingPtr);
	}
}
