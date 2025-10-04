import sys #import for CLI arguments

# ------------------- MINIMAX / ALPHA-BETA SEARCH ALGORITHMS -----------------------
#MINIMAX-SEARCH function with nodes argument that will count the number of search trees generated when it's the computer's turn
def MINIMAX_SEARCH(game, state, nodes):
    nodes['count'] = 1  # root node
    player = game.TO_MOVE(state)
    value, move = MAX_VALUE(game, state, player, nodes)
    return move


#MAX-VALUE function with nodes argument that will count the number of search trees generated when it's the computer's turn
def MAX_VALUE(game, state, player, nodes):
    nodes['count'] += 1
    if game.IS_TERMINAL(state):
        return game.UTILITY(state, player), None
    v, move = -float("inf"), None
    for a in game.ACTIONS(state):
        v2, a2 = MIN_VALUE(game, game.RESULT(state, a), player, nodes)
        if v2 > v:
            v, move = v2, a
    return v, move

#MIN-VALUE function with nodes argument that will count the number of search trees generated when it's the computer's turn
def MIN_VALUE(game, state, player, nodes):
    nodes['count'] += 1
    if game.IS_TERMINAL(state):
        return game.UTILITY(state, player), None
    v, move = float("inf"), None
    for a in game.ACTIONS(state):
        v2, a2 = MAX_VALUE(game, game.RESULT(state, a), player, nodes)
        if v2 < v:
            v, move = v2, a
    return v, move

#ALPHA-BETA-SEARCH function with nodes argument that will count the number of search trees generated when it's the computer's turn
def ALPHA_BETA_SEARCH(game, state, nodes):
    nodes['count'] += 1
    player = game.TO_MOVE(state)
    value, move = MAX_VALUE_AB(game, state, player, -float("inf"), float("inf"), nodes)
    return move

#MAX-VALUE-ALPHABETA function with nodes argument that will count the number of search trees generated when it's the computer's turn
def MAX_VALUE_AB(game, state, player, alpha, beta, nodes):
    nodes['count'] += 1
    if game.IS_TERMINAL(state):
        return game.UTILITY(state, player), None
    v, move = -float("inf"), None
    for a in game.ACTIONS(state):
        v2, a2 = MIN_VALUE_AB(game, game.RESULT(state, a), player, alpha, beta, nodes)
        if v2 > v:
            v, move = v2, a
        alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move

#MIN-VALUE-ALPHABETA function with nodes argument that will count the number of search trees generated when it's the computer's turn
def MIN_VALUE_AB(game, state, player, alpha, beta, nodes):
    nodes['count'] += 1
    if game.IS_TERMINAL(state):
        return game.UTILITY(state, player), None
    v, move = float("inf"), None
    for a in game.ACTIONS(state):
        v2, _ = MAX_VALUE_AB(game, game.RESULT(state, a), player, alpha, beta, nodes)
        if v2 < v:
            v, move = v2, a
        beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move

# ------------------- TIC-TAC-TOE CLASS -------------------
class TicTacToe:
    
    _INITIAL_STATE = [' '] * 9  # class-level constant (template for empty board)
    def __init__(self):
        #Different wins situations used to determine when the game stop
        self.wins = [(0,1,2),(3,4,5),(6,7,8),
                     (0,3,6),(1,4,7),(2,5,8),
                     (0,4,8),(2,4,6)]
        self.state = self._INITIAL_STATE[:]  # initial board for each game

    #TO-MOVE function used to count X’s and O’s to decide whose turn it is
    def TO_MOVE(self, state):
        x_count = state.count('X')
        o_count = state.count('O')
        return 'X' if x_count == o_count else 'O'

    #ACTIONS Function returns indices (1–9) that are still empty
    def ACTIONS(self, state):
        return [i+1 for i in range(9) if state[i] == ' ']

    # RESULT funcion used to return a new state after applying action a
    def RESULT(self, state, action):
        new_state = state[:]
        player = self.TO_MOVE(state)
        new_state[action-1] = player
        return new_state

    #IS_TERMINAL function to determinate whether a state is a terminal one by checking the value of the utility function
    def IS_TERMINAL(self, state):
        return self.UTILITY(state, 'X') != 0 or self.UTILITY(state, 'O') != 0 or ' ' not in state

    #UTILITY function used for terminal state
    def UTILITY(self, state, player):
        for a,b,c in self.wins:
            if state[a] != ' ' and state[a] == state[b] == state[c]:
                return 1 if state[a] == player else -1
        return 0

# print_board function prints the board in the required format
def print_board(state):
    print(f" {state[0]} | {state[1]} | {state[2]} ")
    print("---+---+---")
    print(f" {state[3]} | {state[4]} | {state[5]} ")
    print("---+---+---")
    print(f" {state[6]} | {state[7]} | {state[8]} ")
    
# ------------------- MAIN PROGRAM FOR ACTUAL GAME-------------------
#Check command line arguments
if len(sys.argv) != 4:
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()
    
#Getting the different arguments
ALGO, FIRST, MODE = sys.argv[1], sys.argv[2].upper(), sys.argv[3]

# Validate arguments
if ALGO not in ('1', '2') or FIRST not in ('X', 'O') or MODE not in ('1', '2'):
    print("ERROR: Not enough/too many/illegal input arguments.")
    sys.exit()
    
# Map algorithm choice to text
algo_text = "MiniMax" if ALGO == '1' else "MiniMax with alpha-beta pruning"
mode_text = "human versus computer" if MODE == '1' else "computer versus computer"

print("Konan, Otioh Marie-Lynn Corianne Delon, A20541182 solution:")
print(f"Algorithm: {algo_text}")
print(f"First: {FIRST}")
print(f"Mode: {mode_text}\n")

#Initialize the game
game = TicTacToe()
current_player = FIRST
nodes = {'count': 0}  # node counter

# ------------------- MAIN GAME LOOP -------------------
while not game.IS_TERMINAL(game.state):
    print_board(game.state)
    possible_moves = sorted(game.ACTIONS(game.state))

    # Human player's turn
    if MODE == '1' and current_player == 'X':
        while True:
            try:
                inp = input(f"{current_player}'s move. What is your move (possible moves at the moment are: {possible_moves} | enter 0 to exit the game)? ")
                move = int(inp)
                if move == 0:
                    print("Game terminated by user.")
                    sys.exit()
                if move in possible_moves:
                    break
            except ValueError:
                pass
            print(f"Invalid move. Please choose from {possible_moves} or 0 to exit.")
        game.state = game.RESULT(game.state, move)

    # Computer player's turn
    else:
        nodes['count'] = 1  # reset node counter for this move
        if ALGO == '1':
            move = MINIMAX_SEARCH(game, game.state, nodes)
        else:
            move = ALPHA_BETA_SEARCH(game, game.state, nodes)
        game.state = game.RESULT(game.state, move)
        print(f"{current_player}'s selected move: {move}. Number of search tree nodes generated: {nodes['count']}")

    current_player = 'O' if current_player == 'X' else 'X'

# Game over
print_board(game.state)
if game.UTILITY(game.state, 'X') == 1:
    print("X WON")
elif game.UTILITY(game.state, 'O') == 1:
    print("O WON")
else:
    print("TIE")