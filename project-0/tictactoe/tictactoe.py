"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

# player must fill any of these sets of cells to win the game
WIN_CASES = [
        #row streak
        {(0,0),(0,1),(0,2)},
        {(1,0),(1,1),(1,2)},
        {(2,0),(2,1),(2,2)},
        #column streak
        {(0,2),(1,2),(2,2)},
        {(0,1),(1,1),(2,1)},
        {(0,0),(1,0),(2,0)},
        #diagonal streak
        {(0,0),(1,1),(2,2)},
        {(0,2),(1,1),(2,0)}
    ]

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
    players = [X,O]
    [lineA, lineB, lineC] = board
    played = list(filter(lambda x: x != EMPTY, lineA+lineB+lineC))
    return players[len(played) % 2]


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    # check if any win case is filled by a single player
    for win_case in WIN_CASES:
        cell_values = [board[i][j] for (i,j) in win_case]
        if cell_values[0] is not EMPTY:
            if all(val == cell_values[0] for val in cell_values):
                winner = cell_values[0]
                break
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in [X,O] or len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not terminal(board):
        raise Exception("board is not terminal")
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board:list):
    """
    Returns the optimal action for the current player on the board.
    """
    start = Node(board, None)
    options = []
    #gather best utility values for each possible action
    for action in actions(start.state):
        if player(board) == X:
            options.append(min_value(start.get_child(action)))
        else:
            options.append(max_value(start.get_child(action)))
    # find best utility value in options
    if player(board) == X:
        #for maximizer player, best utility is the largest possible value
        best_utility = max([opt.utility for opt in options])
    else:
        #for minimizer player, best utility is the smallest possible value
        best_utility = min([opt.utility for opt in options])

    # best actions are the ones that lead to best utility
    best_actions = list(filter(lambda o:o.utility == best_utility, options))
    #the selection of actions[0] is arbitrary
    return best_actions[0].action

#helpers for minimax
class Node:
    """
    Representation of a state that stores state, action and utility
    """
    def __init__(self, state, action) -> None:
        self.state = state
        self.action = action

    def set_max_utility(self, node):
        """
        Updates self.utility to largest value between self.utility and node.utility
        """
        self.utility = max(self.utility, node.utility)

    def set_min_utility(self, node):
        """
        Updates self.utility to smallest value between self.utility and node.utility
        """
        self.utility = min(self.utility, node.utility)

    def get_child(self, action):
        '''
        Returns a Node that represents the new state after action is executed.
        
        '''
        clone_state = copy.deepcopy(self.state)
        child = Node(state=result(clone_state, action), action=action)
        initial_utility = {
            X: math.inf,
            O: -math.inf
        }
        child.utility = initial_utility[player(self.state)]
        return child
    
def max_value(node:Node):
    """
    Starting from node: assings utility of each possible action
    """
    if terminal(node.state):
        node.utility = utility(node.state)
    else:
        for action in actions(node.state):
            # create a child node from action and call min_value on child
            node.set_max_utility(min_value(node.get_child(action)))
    return node

def min_value(node:Node):
    if terminal(node.state):
        node.utility = utility(node.state)
    else:
        for action in actions(node.state):
            # create a child node from action and call max_value on child
            node.set_min_utility(max_value(node.get_child(action)))
    return node