"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for line in board:
        count += len(list(filter(None, line)))

    if len(board) ** 2 == count:
        return None

    return X if count % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for line_idx, line in enumerate(board):
        for cell_idx, cell in enumerate(line):
            if cell == EMPTY:
                actions.add((line_idx, cell_idx))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    res_board = board.copy()
    if action is None:
        raise ValueError
    res_board[action[0]][action[1]] = player(board)
    return res_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # left-right
    for line in board:
        if line.count(X) == len(board[0]):
            return X
        elif line.count(O) == len(board[0]):
            return O

    # top-bottom
    for line_idx, line in enumerate(board):
        if [board[i][line_idx] for i in range(len(line))].count(X) == len(board[0]):
            return X
        elif [board[i][line_idx] for i in range(len(line))].count(O) == len(board[0]):
            return O

    # diagonal
    right = (board[0][0], board[1][1], board[2][2])
    left = (board[2][0], board[1][1], board[0][2])
    if right.count(X) == len(board[0]) or left.count(X) == len(board[0]):
        return X
    elif right.count(O) == len(board[0]) or left.count(O) == len(board[0]):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is a terminal board, the minimax function should return None
    if terminal:
        return None

    for line_idx, line in enumerate(board):
        for cell_idx, cell in enumerate(line):
            if cell == EMPTY:
                return (line_idx, cell_idx)

