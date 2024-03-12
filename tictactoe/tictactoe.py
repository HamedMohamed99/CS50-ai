import copy
"""
Tic Tac Toe Player
"""

X = "X"
O = "O"
EMPTY = None

class Node():
    def __init__(self, state, parent, action, ):
        self.state = state
        self.parent = parent
        self.action = action
        

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node



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
    x=0
    o=0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'X' :
                x += 1 
            if board[i][j] == 'O' :
                o += 1
    
    if x==0 and o==0 :
        return 'X'
    elif x==o :
        return 'X'
    elif x>o :
        return 'O'



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY :
                action.append((i,j)) 
            

    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not board[action[0]][action[1]] == EMPTY :
        raise NameError('Wrong Move')

    new_board = copy.deepcopy(board)
    
    new_board[action[0]][action[1]] = player(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if board[i][0] == 'X' and board[i][1] == 'X' and board[i][2] == 'X' :
            return 'X'
        elif board[0][i] == 'X' and board[1][i] == 'X' and board[2][i] == 'X' :
            return 'X'
        
        elif board[i][0] == 'O' and board[i][1] == 'O' and board[i][2] == 'O' :
            return 'O'
        elif board[0][i] == 'O' and board[1][i] == 'O' and board[2][i] == 'O' :
            return 'O'

    if board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X' :
        return 'X'
    elif board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X' :
        return 'X'

    elif board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O' :
        return 'O'
    elif board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O' :
        return 'O'
    else :
        return None
        



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    x=0
    o=0
    if not winner(board) == None :
        return True
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'X' :
                x += 1 
            if board[i][j] == 'O' :
                o += 1
    if x+o == 9 :
        return True
    else :
        return False
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == 'X' :
        return 1
    elif winner(board) == 'O' :
        return -1
    elif terminal(board):
        return 0
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    m = True
    if m :
        m = False
        m1=0
        m2=0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'X' :
                    m1 += 1 
                if board[i][j] == 'O' :
                    m2 += 1
        
        if m1==0 and m2==0 :
            return (0,0)
    
    solve =[]
    def max_value(board):
        if terminal(board):
            return utility(board)
        v=-10
        for action in actions(board):
            v=max(v,min_value(result(board,action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v=10
        for action in actions(board):
            v=min(v,max_value(result(board,action)))
        return v

    if player(board)=='X':
        for action in actions(board):
            solve.append((min_value(result(board,action)),action))
        solve.sort(key=lambda row: (row[0]), reverse=True)
        return solve[0][1]

    if player(board)=='O':
        for action in actions(board):
            solve.append((max_value(result(board,action)),action))
        solve.sort(key=lambda row: (row[0]))
        return solve[0][1]

    


