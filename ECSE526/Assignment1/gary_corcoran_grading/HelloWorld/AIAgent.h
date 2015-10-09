/*
 * AIAgent.h
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#ifndef AIAGENT_H_
#define AIAGENT_H_

#include "GST.h"

class AIAgent {
public:
	AIAgent(char _ai_player, char _human_player, int size, int _win_connections, clock_t _start, double _duration, std::string text_file);
	~AIAgent();
	void playGame();
private:
	Action iterativeDeepeningSearch();
	void depthLimitedSearch(int limit, Action _action = Action());
	void resursiveDLS(char player, GSTNode* node, int limit, Action best_move = Action());
	int heuristic(Board _board);
	int checkAdjacent(Board _board);
	int checkDistance(Board _board);
	Action findMove(int _score);
	int alphaBetaSearch(GSTNode* node, int alpha, int beta, char player);
	char ai_player;
	char human_player;
	int win_connections;
	int boardDimensions;
	clock_t start;
	double moveDuration;
	GST* gameTree;
};

#endif /* AIAGENT_H_ */
