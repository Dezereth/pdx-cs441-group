"""Tree search: states are arrangements of pieces on the board available actions correspond to legal moves for the current player in that arrangement
Evaluation function: takes in a state of the game (board arrangement) and boils it down to a real number evaluation of the state. 
Ex: function gives higher scores to board states in which the player of interest has more of their pieces on the board then the opponent
we want the function to assign an infinity score to the board arrangement
in which the opponent's king is checkmate; meaning that our player of interest is guaranteed to win the game 
we could take the opponent's actions into consideration once we've moved.
MINIMAX chooses an action which minimizes our maximum possible loss from making a particular move; For each move we make, we look ahead as many steps as our computing power will allow and examine all possible moves our opponent could make in each of their future turns. 
We can then take the maximum loss (min of our eval function) that our opponent could induce for us via their moves and choose the move we could make, which minimizes this maximum. 
Heuristic: Cutting down computation time, and optimization of the algorithm, given the structure of chess.
The optimization of minimax is alpha-beta pruning; Any move for which another move has already been discovered that's guaranteed to do better than its eliminated. 

Game tree: structure in the form of a tree consisting of all possible moves which allow u to move 
from the state of the game to the next one.
SEARCH PROB:
 1. initial state(position of the board & whose move is it)
 2. successor function: legal moves that the player can make
 3. terminal state: position of the board when the game is over
 4. utility function: Numeric val of the outcome of the game
 Player MIN: tries to get lowest possible score - Player MAX: tries to get highest possible score
if depth is 0 or node is terminal node 
def minimax(node):
    moves = node.legalMoves()
    bestMove = moves[0]
    bestScore = float('-inf')
    for move in moves:
        clone = node.nextState(move)
        score = mimPlay(clone)
        if score > bestScore:
            bestMove = move
            bestScore = score
    return bestMove
 Given board configuration, minimax algorithm chooses the best move to take.
 Terminal state has a numeric score.
 implementation of minimax using recursion
 the function minimax takes the game board as input and
 checks if we’re at the terminal state (ending condition), and returns the score if true. Otherwise, return None
 2. if it’s not terminal state, for each legal move, we call the minimax function to return their score ([move]: to get the history of the game) (if it’s terminal -> return utility)
 3. finally, return the best score; maximum score if it’s max’s turn and vice versa. """
def minimax(board, turn):
	terminal = check(board)
	if terminal is not None:
		return (terminal, [])
	result = []
	for legalMoves in generateMoves(board):
		score, moves = bestMove(minimax(board, move))
		result.append((score, [move] + moves))

	if turn == ‘MAX’:
		return max(result)
	else:
		return min(result)

"""
def minimax(boardState , depth, maximizing, alpha, beta):

    if terminal not None:
        return terminalVal;
    if maximizing:
        bestVal= '-INFINITY'
         for child in boardState:
            value = minimax(boardState, depth+1, false, alpha, beta)
            bestVal = max( bestVal, value) 
            alpha = max( alpha, bestVal)
            if beta <= alpha:
                break
                    returnbestVal
    else:
        bestVal = '+INFINITY'
         for child in boardState:

            value = minimax(node, depth+1, true, alpha, beta)
            bestVal = min( bestVal, value) 
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
                    return bestVal

# Function call:
minimax(0, 0, true, '-INFINITY', '+INFINITY')"""
