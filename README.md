# Dots And Boxes: MCTS, Parallelization, and a Neural Network

Final project for CS321 (Making Decisions with AI) made by Nick Pandelakis and Miguel Alvarez. Dots and boxes is a perfect information game that involves two agents drawing lines between two dots on a grid (6 x 6 in our implementation). When a player completes a box by drawing the last line around a 1 x 1 grid square, the player is awarded that square and draws another line. The game is finished when all possible lines have been drawn and the player with the most boxes at the end is the winner.

In this implementation of dots and boxes we'll be using Monte Carlo Tree Search (MCTS), parallelization, as well as a neural network to improve both the runtime and win-rate of the AI player. In order to measure the success of both parallelization and a neural network, we've included relevant data regarding the impovement of runtime and win-rate of the MCTS AI player after the implementation of parallelization and a neural network.

# How to Run the Project
If python3 is installed in local machine:
Type `python main.py` in a terminal while in directory that holds all the project files in this repo.

If python2.7 or an older version is installed in local machine:
Type `python3 main.py` in terminal while in directory that holds all the project files in this repo.

# MCTS Runtime with/without Parallelization
#TODO

# MCTS Win Rate with/without Neural Network
#TODO
