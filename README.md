# Dots And Boxes: MCTS, Parallelization, and a Neural Network

Final project for CS321 (Making Decisions with AI) made by Nick Pandelakis and Miguel Alvarez. Dots and boxes is a perfect information game that involves two agents drawing lines between two dots on a grid (6 x 6 in our implementation). When a player completes a box by drawing the last line around a 1 x 1 grid square, the player is awarded that square and draws another line. The game is finished when all possible lines have been drawn and the player with the most boxes at the end is the winner.

**Part 1**
In this implementation of dots and boxes we'll be using Monte Carlo Tree Search (MCTS) with parallelization in order to speed up the runtime of the simulations. In order to measure the success of this part, we've included runtime for the game below that includes runtime (in seconds), number of games, and number of rollouts. Both of the players in these simulations are MCTS agents.

**Part 2**
We will also be incorporating a neural network in order to increase the win-rate of the AI player. In order to measure the success of this part, we've included win-rate data for win-rate (out of 25 games) when we have an MCTS agent with the neural network playing against an MCTS agent without the neural network.

# How to Run the Project
Type `python3 MCTS-DB.py --rollouts [desired number of rollouts] --numGames [don't include if only simulating one game]` in terminal while in directory that holds all the project files in this repo. Optional flags include: `--second [if included, MCTS will go second] --displayBoard [will display game board as simulation plays out - cannot do this when parallelizing] --rolloutsSecondMCTSAgent [if included, will second player will also be an MCTS agent, must include number of rollouts desired] --ucbConst [must precede the desired value to set the UCB Constant value to] --parallel [if included, will run the games asynchronously]`.

# MCTS Runtime with/without Parallelization (Part 1)
We decided to speed up MCTS by parallelizing the games with the concurrent.futures Python module which allows for asynchronous execution performed with seperate processes using ProcessPoolExecutor. We decided to parallelize the games when multiple games are being played via the --numGames argument since each game does not give any valuable information to the next game that might be lost due to running multiple processes at the same time. We decided to play the dots and boxes games with two MCTS against each other. Also, we kept the number of rollouts the same for each agent and timed the time it took to print each game number (example: Game 1, Game 2, and so on) and print out the time from start of execution to finish. We first did this process without parallelization, recorded our results, and then repeated this with parallelization.

**Runtime without Parallelization**

| Number of Games | 5 Rollouts | 50 Rollouts | 250 Rollouts | 1000 Rollouts|
|-----------------|------------|-------------|--------------|--------------|
| 5               | 0.116 secs | 1.144 secs  | 6.264 secs   | 27.249 secs  |
| 10              | 0.228 secs | 2.334 secs  | 12.679 secs  | 56.912 secs  |
| 15              | 0.341 secs | 3.480 secs  | 19.276 secs  | 84.284 secs  |
| 20              | 0.452 secs | 4.634 secs  | 25.798 secs  | 114.098 secs |
| 25              | 0.549 secs | 5.829 secs  | 32.261 secs  | 141.591 secs |

**Runtime with Parallelization**

| Number of Games | 5 Rollouts | 50 Rollouts | 250 Rollouts | 1000 Rollouts|
|-----------------|------------|-------------|--------------|--------------|
| 5               | 0.295 secs | 0.613 secs  | 2.133 secs   | 8.742 secs   |
| 10              | 0.384 secs | 1.056 secs  | 4.462 secs   | 18.965 secs  |
| 15              | 0.393 secs | 1.279 secs  | 6.103 secs   | 25.830 secs  |
| 20              | 0.418 secs | 1.600 secs  | 8.290 secs   | 22.568  secs |
| 25              | 0.452 secs | 2.119 secs  | 10.406 secs  | 45.544  secs |

After running 

# MCTS Win Rate with/without Neural Network (Part 2)
To be implemented...
