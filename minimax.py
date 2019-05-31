# -*- coding: utf-8 -*-
"""
Dalton Gray, ...
This file is the implementation of the MiniMax algorithm using alpha-beta pruning
to evaluate chess moves.

IMPLEMENTATION INCOMPLETE AND WILL NOT RUN CURRENTLY.

"""

class MiniMax():
    def __init__(self, state, limit):
        self.state = state;
        self.limit = limit;

    def getMove(state):    #Function to get move from algorithm, returns move to be pushed.
        self.state = state;
        moves = [];        #List of valid moves.
        alpha = -1000;     #Init alpha
        beta = 1000;       #Init beta
        depth = 0;         #Init depth
        limit = self.limit; #Depth limit
        value = -1000;     #Init value
        check = -1000;     #Variable to hold values to check against.
        best = '';         #Best move evaluated.

        for i in state.legal_moves:  #Populates list of valid moves from board state.
            vmoves.append(i);

        for move in moves: #Cycles through and evaluates each possible move.
            check = evaluate(state, move, depth, limit, alpha, beta, true);
            if check > value:
                value = check;
                best = move;

        return best;
       """
       Undecided on if it would be better to cycle through possible available moves here in order to isolate
       string of the best move, or to let the evaluate(function) do all of the work.
       I am leaning towards the former because moves must be pushed in order to obtain and evaluate the next
       player's moves so it seems easier to pass in the move to be pushed along with the state it will be
       pushed on.

       # return = evaluate(moves, depth, limit, alpha, beta, true); #Calls evaluate function and returns best move.
       """ 
    def evaluate(state, move, depth, limit, alpha, beta, player):
        if player: #Checks to see which player to evaluate.
            value = checkMove(move); #Gets value of individual move. checkMove() function not yet created.
            if depth == limit:    #Checks to ensure algorithm is within depth limit.   
                return value;
            else:
                #Evaluate opponents moves in order to return the absolute value for the move passed in.
                """
                IN PROGRESS

                state.push(move);  #Pushes passed in move, to evaluate opponents next move.
                for i in state.legal_moves:
                    min_val = evaluate(
                """

        else:
            value = checkMove(move)
            if value != 0:
                value = -value; #Makes value negative if the move is not the player's move.
            if depth == limit:
                return value;
            else:
                #Evaluate opponents moves in order to return the absolute value for the move passed in.
            
