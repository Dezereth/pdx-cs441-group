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
        depth = 0;         #Init depth
        limit = self.limit; #Depth limit
        value = -1000;     #Init value
        best = '';         #Best move evaluated.


       best, value = evaluate(value, depth, limit, true); #Calls evaluate function and returns best move.
       return best;

    def legals(): #Helper function to get legal moves.
        moves = []
        for i in self.state.legal_moves:
            moves.append(i);

        return moves;
       
    def evaluate(value, depth, limit, player): #Function to find the best move.
        catch = '';
        best = '';
        total = 0;
        if depth == limit: #Checks to ensure limit is not reached.
            return catch, total;

        moves = legals(); #Gets a legal list of moves.

        if player:
            for move in moves:
                move_val = checkMove(move); #Evaluates individual move. checkMove() does not exist.
                self.state.push(move);
                catch, total = evaluate(value, depth+1, limit, false);
                move_val += total;
                if move_val > value:
                    value = move_val;
                    best = move;
                self.state.pop();
            return best, value;

                #INCOMPLETE

        else:
            for move in moves:
                move_val = checkMove(move);
                if move_val != 0:
                    move_val = -move_val;
                self.state.push(move);
                catch, total = evaluate(value, depth+1, limit, true);
                move_val += total;
                if move_val < value:
                    value = move_val;
                    catch = move;
                self.state.pop();
            return catch, value;

          #INCOMPLETE
