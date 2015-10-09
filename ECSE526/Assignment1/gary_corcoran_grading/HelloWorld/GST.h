/*
 * GST.h
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#ifndef GST_H_
#define GST_H_

#include "GSTNode.h"

class GST {
public:
	GST();
	~GST();
	void clearTree();
	void insert(Board _board, GSTNode* parent = nullptr);
	GSTNode* getRoot();
	void preOrder();
protected:
	void _preOrder(GSTNode*);
	void postOrderDelete(GSTNode* node);
	GSTNode* root;
};

#endif /* GST_H_ */
