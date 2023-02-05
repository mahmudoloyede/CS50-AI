"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
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
    cx = 0
    co = 0
    for i in board:
        for j in i:
            if j == X:
                cx += 1
            elif j == O:
                co += 1
            else:
                pass
    if cx == co:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionz = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                actionz.add((i, j))
    return actionz


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception('Invalid move')
    p = player(board)
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = p
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    b = board
    if b[0][0] == b[0][1] == b[0][2] == X or b[1][0] == b[1][1] == b[1][2] == X or b[2][0] == b[2][1] == b[2][2] == X or b[0][0] == b[1][0] == b[2][0] == X or b[0][1] == b[1][1] == b[2][1] == X or b[0][2] == b[1][2] == b[2][2] == X or b[0][0] == b[1][1] == b[2][2] == X or b[0][2] == b[1][1] == b[2][0] == X:
        return X
    elif b[0][0] == b[0][1] == b[0][2] == O or b[1][0] == b[1][1] == b[1][2] == O or b[2][0] == b[2][1] == b[2][2] == O or b[0][0] == b[1][0] == b[2][0] == O or b[0][1] == b[1][1] == b[2][1] == O or b[0][2] == b[1][2] == b[2][2] == O or b[0][0] == b[1][1] == b[2][2] == O or b[0][2] == b[1][1] == b[2][0] == O:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    b = board
    if b[0][0] == b[0][1] == b[0][2] != EMPTY or b[1][0] == b[1][1] == b[1][2] != EMPTY or b[2][0] == b[2][1] == b[2][2] != EMPTY or b[0][0] == b[1][0] == b[2][0] != EMPTY or b[0][1] == b[1][1] == b[2][1] != EMPTY or b[0][2] == b[1][2] == b[2][2] != EMPTY or b[0][0] == b[1][1] == b[2][2] != EMPTY or b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return True
    for i in b:
        for j in i:
            if j == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    val = winner(board)
    if val == X:
        return 1
    elif val == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    '''
    calculates max_values, takes board state, alpha and beta values as parameter
    '''
    if terminal(board):
        return utility(board)

    v = -2
    for a in actions(board):
        v1 = min_value(result(board, a), alpha, beta)
        if v1 > v:
            v = v1
        if v1 >= beta:
            return v
        if v1 > alpha:
            alpha = v1
    return v


def min_value(board, alpha, beta):
    '''
    calculates min_values, takes board state, alpha and beta values as parameter
    '''
    if terminal(board):
        return utility(board)
    v = 2
    for a in actions(board):
        v1 = max_value(result(board, a), alpha, beta)
        if v1 < v:
            v = v1
        if v1 <= alpha:
            return v
        if v1 < beta:
            beta = v1
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        v = -2
        for a in actions(board):
            val = min_value(result(board, a), -2, 2)
            if val > v:
                v = val
                action = a
    else:
        v = 2
        for a in actions(board):
            val = max_value(result(board, a), -2, 2)
            if val < v:
                v = val
                action = a

    return action

