# Dots And Boxes: MCTS, Parallelization, and a Neural Network

Final project for CS321 (Making Decisions with AI) made by Nick Pandelakis and Miguel Alvarez. Dots and boxes is a perfect information game that involves two agents drawing lines between two dots on a grid (6 x 6 in our implementation). When a player completes a box by drawing the last line around a 1 x 1 grid square, the player is awarded that square and draws another line. The game is finished when all possible lines have been drawn and the player with the most boxes at the end is the winner.

**Part 1**
In this implementation of dots and boxes we'll be using Monte Carlo Tree Search (MCTS) with parallelization in order to speed up the runtime of the simulations. In our game, red (R as marked in displayed boards) is player 1 and blue is player 2 (B as marked in displayed boards). In order to measure the success of this part, we've included runtime for the game below that includes runtime (in seconds), number of games, and number of rollouts. Both of the players in these simulations are MCTS agents.

**Part 2**
We will also be incorporating a neural network in order to increase the win-rate of the AI player. In order to measure the success of this part, we've included win-rate data for win-rate (out of 25 games) when we have an MCTS agent with the neural network playing against an MCTS agent without the neural network.

# How to Run the Project
First, unzip the folder in order to uncompress the files needed to run the game.

Install these Python modules since mirage doesn't have them:

pip3 install keras

pip3 install tensorflow

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

After running MCTS both with and without parallelization, we can see a clear decrease in runtime after about 5 rollouts when playing 20+ games. For every combination of number of games and number of rollouts we tested after this spot we saw about a 3-4x decrease in runtime with parallelization.

# MCTS Win Rate with/without Neural Network (Part 2)

Reference Paper: https://www.mdpi.com/2076-3417/11/5/2056/htm

We based our neural network approach off of the paper with the following modifications:

Changed board size from 5 x 5 to 4 x 4 for quicker data gathering.
Changed the input layer from 85 to 56 to match the new board size.
Changed the hidden layer from 100 to 67 to match the proportions of the paper’s original network (This had no effect on model accuracy).
Changed the output layer from 3 to 1, since we are only giving player 1 access to the neural network.

The input layer of our neural network takes in a vector with 56 entries. These entries correspond to the 40 total lines that can be drawn on the board plus the 16 boxes. At the recommendation of the paper, we used the sigmoid activation function for both the middle and output layers. This function is particularly useful for the output layer since it produces a number between 0 and 1, giving us the probability for a player 1 win. Overall, our neural network was able to achieve 70% accuracy after 100 training epochs. We then used the created model during the simulation phase of MCTS. If the model predicted that player 1 would win with a probability greater than some threshold, we cut the simulation short there and moved on to back propagation immediately.

Although the neural network itself showed great promise, it did not deliver desirable results when included in MCTS. Even with extremely few rollouts, player one takes an absurd amount of time to pick its move. We were not able to replicate the move speeds claimed in the paper. This could be due to the fact that the authors in the paper were using Java instead of Python. We collected our data by running 8950 games with 2000 rollouts for each MCTS player (that still took about 15 hours). This might have been an issue since in the paper they ran 115,000 games with 100,000 rollouts, giving them significantly better moves and likely yielding a neural network model much higher accuracy than ours.

The accuracy of the network seems like it needs to be much higher than ours to achieve what the authors claim. This makes sense because if we are choosing to cut our simulations short based on the prediction made by the network model, that prediction needs to be extremely accurate in order for us to be confident that that state is actually any good.



