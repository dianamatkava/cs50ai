# Nim Game AI: Reinforcement Learning using Q-Learning
<img src="https://wild.maths.org/sites/wild.maths.org/files/nim_game.jpg">

## Overview
This project implements an AI to play the game of *Nim* using *Reinforcement Learning* through the *Q-learning* algorithm. The AI learns by playing games against itself, improving its strategy over time to make better decisions in future games.

In Nim, the game begins with a number of piles, each containing a certain number of objects. Players take turns removing any number of objects from a single pile, and the player forced to remove the last object loses.

The AI learns which actions are advantageous (leading to a win) and which actions to avoid (leading to a loss) by assigning a Q-value to every possible state-action pair and adjusting these values based on experience.


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

### What is Nim Game?
Nim is a mathematical game of strategy in which two players take turns removing (or "nimming") objects from distinct heaps or piles. On each turn, a player must remove at least one object, and may remove any number of objects provided they all come from the same heap or pile. Depending on the version being played, the goal of the game is either to avoid taking the last object or to take the last object.

Nim is fundamental to the Sprague–Grundy theorem, which essentially says that every impartial game is equivalent to a nim game with a single pile.


