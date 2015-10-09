/*
 * Main.cpp
 *
 *  Created on: 2015-09-30
 *      Author: garycorcoran
 */

#include "AIAgent.h"
#include <iostream>
#include <time.h>

int main() {
	clock_t start;
	start = clock();
	AIAgent aiAgent =  AIAgent(BLACK, WHITE, 7, 4, start, 4, "gameboard.txt");
	aiAgent.playGame();
	return 0;
}


