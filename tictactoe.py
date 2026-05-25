"""
Tic Tac Toe Player
"""

import math
import copy

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
    total_x = 0
    total_o = 0
    for row in board:
        for cell in row:
            if cell == "X":
                total_x += 1
            elif cell == "O":
                total_o += 1
    if total_x == total_o:
        return "X"
    else:
        return "O" 


def actions(board):
    action = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i, j))      
    return action    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Raise exception if move is invalid
    if action is None or len(action) != 2:
        raise Exception("Invalid move (invalid action)")
    
    # Copy board so as not to modify the original
    simulated_board = copy.deepcopy(board)
    
    # Return new board with move applied:
    row = action[0]
    column = action[1]

    # If position of move is already occupied raise exception
    if simulated_board[row][column] is not None:
        raise Exception("Invalid move (Cell already occupied)")

    # Ff move is out of bounds raise exception 
    if row < 0 or row > 2 or column < 0 or column > 2:
        raise Exception("Invalid move (out of bounds)")

    if player(board) == "X" or player(board) == "O":
        simulated_board[row][column] = player(board)
        return simulated_board
    else: 
        raise Exception("Invalid move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x_diagonal = 0
    x_verticle = 0
    x_horizontal = 0
    o_diagonal = 0
    o_verticle = 0
    o_horizontal = 0
    # Diagonal check (X)
    for i in range(3):
        if board[i][i] == "X":
            x_diagonal += 1 
        elif board[i][i] == "O":
            o_diagonal += 1
    if x_diagonal == 3:
        return "X"
    elif o_diagonal == 3:
        return "O"
    
    x_diagonal = 0
    o_diagonal = 0

    # Check other diagonal 
    for i in range(3):
        if board[i][2 - i] == "X":
            x_diagonal += 1
        elif board[i][2 - i] == "O":
            o_diagonal += 1

    if x_diagonal == 3:
        return "X"
    if o_diagonal == 3:
        return "O"

    # Horizontal check (X)
    for row in range(3):
        x_horizontal = 0
        o_horizontal = 0
        for column in range(3):
            if board[row][column] == "X":
                x_horizontal += 1
            elif board[row][column] == "O":
                o_horizontal += 1
        if x_horizontal == 3:
            return "X"
        elif o_horizontal == 3:
            return "O"

    # Verticle check
    for column in range(3):
        x_verticle = 0
        o_verticle = 0
        for row in range(3):
            if board[row][column] == "X":
                x_verticle += 1
            elif board[row][column] == "O":
                o_verticle += 1
        if x_verticle == 3:
            return "X"
        elif o_verticle == 3:
            return "O"


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # We store winner if any as variable so we don't have to call it twice as a small optimization
    player_won = winner(board)
    if player_won == "X" or player_won == "O":
        return True 
    # Game also over if all cells filled, check if none empty
    elif len(actions(board)) == 0:
        return True 
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    player_won = winner(board)
    if player_won == "X":
        return 1
    elif player_won == "O":
        return -1
    else:
        return 0
    
# First check if board is terminal (meaning game is over), then return the score of that board using utility, then for every action return the one that has the highest minimum possible value as v (value)


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        # Set alpha (the "floor" for the max player) as the max of alpha and v (value), if alpha is greater than beta (the ceiling of the min player), prune it by breaking, as the min player will always
        # Find the optimal move and won't play it if it's lower than beta since it has better options that have a lower value or are at least equal in the case of our logic
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v

# First check if board is terminal (meaning game is over), then return the score of that board using utility, then for every action return the one that has the lowest possible maximum value as v (value)


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        # Beta pruning, we find the lowest value out of beta and v (value) and set that as beta, then if beta is less than alpha (where alfa is the lowest max will go, the best option they have)
        # then we can prune it by breaking, as max given the choice between their alpha value, e.g 1, and a lower possibility like 0, will always choose the optimal move and get 1 so there's no point considering this as min
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Define alpha and beta as infinitely low initially so that there is always a better option
    alpha = float('-inf')
    beta = float('inf')
    if terminal(board):
        return None
    
    """
    If it's X's turn, we set best_value to minus infinity (so that we ALWAYS can find a better option initially) and best move to none
    We then check for each available action we can take, what the lowest possible value of that action is using min_value, then if the lowest is greater than our current best value, we set that as the new best_value
    and also set the action that got that value as the current best action, after looping through all possible moves we finally return the best_move we are left with
    """
    if player(board) == "X":
        best_value = float('-inf')
        best_move = None
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_move = action
            # Update the alpha to be the max of the best value or alpha so far, Alpha is the "floor" of the maximizer, basically any score lower than this isn't worth considering since min will always choose
            # The lowest possible score, meaning if we have to choice between a 0 or a -1, we don't even consider possibilities if any outcome can lead to -1 because min will always find it     
            alpha = max(alpha, best_value)
        return best_move

    # Otherwise if it's O's turn we set best_value to positive infinity, best move etc to none, and we then check for each available action what is the highest possible value that could result from it? 
    # (remember as the min player our goal is the minimize the score while the max player tries to maximize it), if the highest possible value is less than the current best_value we update it with that value and update
    # the best move to be the move that resulted in that value, after we finish looping through all possible moves we return the final best_move we are left with

    elif player(board) == "O":
        best_value = float('inf')
        best_move = None
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_move = action 
            beta = min(beta, best_value)
        return best_move