# Playing Snake Using Q-Learning

Reinforcement Learning Project

Full Medium on the project to be found here: https://data4help.medium.com/human-vs-machine-reinforcement-learning-in-the-context-of-snake-ae84d0b1f5d1

The structure is as follows:
0. Code   --- Shows the pygame code as well as runs the already trained algorithm. A second player is already inserted in the game
1. Output --- The Q Tables are saved here as well as the png of the Model Performance
2. Images --- Since this game is using pngs for the Snake and the Snacks, these are saved here
3. Sounds --- For a hyper realistic game, Snake Snack eating sounds are saved in this folder 

Running the code leads to the starting page of the game, which looks like this:
![Screenshot 2021-01-06 at 17 42 56](https://user-images.githubusercontent.com/52722450/103796409-6f970380-5047-11eb-921e-f2165edd368c.png)

## Rules of the game
- Eat more rabbits than the reinforcement snake and die less often - What counts is the eating/dying ratio
- You have to eat the green rabbits, your opponent has to eat the red ones
- Your snake dies when it runs against a wall/ itself or the other snake, you are then getting respawned directly


