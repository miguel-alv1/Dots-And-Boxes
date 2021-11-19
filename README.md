# Dots And Boxes: MCTS, Parallelization, and a Neural Network

Final project for CS321 (Making Decisions with AI) made by Nick Pandelakis and Miguel Alvarez. Dots and boxes is a perfect information game that involves two agents drawing lines between two dots on a grid (6 x 6 in our implementation). When a player completes a box by drawing the last line around a 1 x 1 grid square, the player is awarded that square and draws another line. The game is finished when all possible lines have been drawn and the player with the most boxes at the end is the winner.

In this implementation of dots and boxes we'll be using Monte Carlo Tree Search (MCTS), parallelization, as well as a neural network to improve both the runtime and win-rate of the AI player. In order to measure the success of both parallelization and a neural network, we've included relevant data regarding the impovement of runtime and win-rate of the MCTS AI player after the implementation of parallelization and a neural network.

# How to Run the Project
If python3 is installed in local machine:
Type `python main.py` in a terminal while in directory that holds all the project files in this repo.

If python2.7 or an older version is installed in local machine:
Type `python3 main.py` in terminal while in directory that holds all the project files in this repo.

# MCTS Runtime with/without Parallelization

Runtime without Parallelization:

| Number of Games | 5 Rollouts | 50 Rollouts | 250 Rollouts | 1000 Rollouts|
|-----------------|------------|-------------|--------------|--------------|
| 5               | 0.116 secs | 1.144 secs  | 6.264 secs   | 27.249 secs  |
| 10              | 0.228 secs | 2.334 secs  | 12.679 secs  | 56.912 secs  |
| 15              | 0.341 secs | 3.480 secs  | 19.276 secs  | 84.284 secs  |
| 20              | 0.452 secs | 4.634 secs  | 25.798 secs  | 114.098 secs |
| 25              | 0.549 secs | 5.829 secs  | 32.261 secs  | 141.591 secs |

Runtime with Parallelization:

| Number of Games | 5 Rollouts | 50 Rollouts | 250 Rollouts | 1000 Rollouts|
|-----------------|------------|-------------|--------------|--------------|
| 5               | 0.295 secs | 0.613 secs  | 2.133 secs   | 8.742 secs   |
| 10              | 0.384 secs | 1.056 secs  | 4.462 secs   | 18.965 secs  |
| 15              | 0.393 secs | 1.279 secs  | 6.103 secs   | 25.830 secs  |
| 20              | 0.418 secs | 1.600 secs  | 8.290 secs   | 22.568  secs |
| 25              | 0.452 secs | 2.119 secs  | 10.406 secs  | 45.544  secs |

# MCTS Win Rate with/without Neural Network
#TODO
