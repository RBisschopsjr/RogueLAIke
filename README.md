# RogueLAIke

Welcome to RogueLAIke, a game where the player has to move around in an unpredictable environment.

## Content
The directory **game** contains all the relevant files:
* Genetic programming.py 	- the file containing the genetic algorithm
* Monster.py			- the class constructing the Monster
* RandomPlayer.py		- the class constructing the RandomPlayer
* maze.py			- the file containing the entire game
* makeMaze.py			- the file constructing the maze

## How to run the game
To run the game for the RandomPlayer, you can run the `RandomPlayer.py`

To run the game for the Genentic Program, you can run the `Genetic programming.py`. Here you have to possibility to change some parameters for the algorithm. In the first two lines of the main function you can change the amount of individuals in a population and the amount of generations.

To alter something in the game, you need to go to `maze.py`. The top of the file has initialized a lot of global variables, here you can alter everything:
* gridSize		- needs to be an array with two values (e.g. [10,10])
* numOfMonsters 	- the amount of monsters
* walkScore		- the reward for taking a step
* monsterScore		- the reward for killing a monster
* exitScore		- the reward for finding the exit
* wrongStepScore	- the penalty for trying to take a step into the wall
* wrongAttack		- the penalty for attacking without killing a monster
* deathScore		- the penalty for getting killed by a monster