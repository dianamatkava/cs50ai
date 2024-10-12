# CS50AI Projects
![Harvard CS50AI](assets/harvard-cs50ai.png)

## Minesweeper Game
[1. Knowledge Minesweeper Specification](https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/)

### Description:
Minesweeper game implemented with `pygame`, offering both solo play AI play. The Minesweeper game follows the classic rules where the player must uncover all cells on the board.

![Minesweeper Game requirements](./assets/minesweepers.gif)

### Implementation
The game implementation utilizes **Propositional Logic** for intelligent decision-making.


## Nim Game AI: Reinforcement Learning using Q-Learning
<img src="https://wild.maths.org/sites/wild.maths.org/files/nim_game.jpg">

### Description:
This project implements an AI to play the game of *Nim* using *Reinforcement Learning* through the *Q-learning* algorithm. The AI learns by playing games against itself, improving its strategy over time to make better decisions in future games.

![Nin Game requirements](https://cs50.harvard.edu/ai/2024/projects/4/nim/)

## Key Concepts
- *State*: Represents the configuration of piles. Example: [1, 1, 3, 5] represents a state where pile 0 has 1 object, pile 1 has 1 object, pile 2 has 3 objects, and pile 3 has 5 objects.
- *Action*: A pair (i, j) representing removing j objects from pile i. For instance, the action (3, 5) means removing 5 objects from pile 3.
- *Q-value*: A value associated with a specific state-action pair, indicating the "quality" or potential reward of taking that action in that state.
- *Q-learning Update*: After each move, update the Q-value for the action taken using the formula:


Where:

`Q(s,a)←Q(s,a)+α×(new_estimate−old_estimate)`

- `α (alpha)` is the learning rate, controlling how much value new information.
- `new estimate` is the sum of the immediate reward and the future rewards from the next state.
- `old estimate` is the current Q-value for the state-action pair.



# Crossword
[3. Optimization Crossword Specification](https://cs50.harvard.edu/ai/2024/projects/3/crossword/)


# Heredity

## Description
The task in this project is to use **Bayesian Network Model** to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, the AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question using **join probability**.



