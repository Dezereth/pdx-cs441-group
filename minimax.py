# -*- coding: utf-8 -*-
"""
Dalton Gray, ...
This file is the implementation of the MiniMax algorithm using alpha-beta pruning
to evaluate chess moves.

IMPLEMENTATION INCOMPLETE AND WILL NOT RUN CURRENTLY.

"""

import chess

#%%

class MiniMax():
    def __init__(self, state, limit):
        self.state = state;
        self.limit = limit;

    def getMove(self, state):    #Function to get move from algorithm, returns move to be pushed.
        self.state = state
        depth = 0         #Init depth
        limit = self.limit #Depth limit
        best = ''         #Best move evaluated.
        alpha = -1000
        beta = 1000

        best, value = self.evaluate(depth, limit, True, alpha, beta) #Calls evaluate function and returns best move.
        return best

    def legals(self): #Helper function to get legal moves.
        moves = []
        for i in self.state.legal_moves:
            moves.append(i)
        return moves
       
    def evaluate(self, depth, limit, player, alpha, beta): #Function to find the best move.
        catch = '';
        best = '';
        total = 0;
        if depth == limit: #Checks to ensure limit is not reached.
            return catch, total;

        moves = self.legals(); #Gets a legal list of moves.

        if player:
            value = -1000;
            for move in moves:
                self.state.push(move);
                move_val = self.checkMove(str(self.state), self.state.turn); #Evaluates individual move. checkMove() does not exist.
                catch, total = self.evaluate(depth+1, limit, False, alpha, beta);
                move_val += total;
                alpha = max(move_val, alpha);
                if move_val > value:
                    value = move_val;
                    best = move;
                self.state.pop();
                if beta <= alpha:
                    break;
            return best, value;

                #INCOMPLETE

        else:
            value = 1000;
            for move in moves:
                self.state.push(move);
                move_val = self.checkMove(str(self.state), self.state.turn)
                move_val = -move_val;
                catch, total = self.evaluate(depth+1, limit, True, alpha, beta);
                move_val += total;
                beta = min(move_val, beta);
                if move_val < value:
                    value = move_val;
                    catch = move;
                self.state.pop();
                if beta <= alpha:
                    break
            return catch, value;

    def checkMove(self, state, turn):
          """
          <state> = str(board)
          <turn> = board.turn
          """
          
          whiteDict = {'P':1,
                       'p':-1,
                       'N':3,
                       'n':-3,
                       'B':3,
                       'b':-3,
                       'R':5,
                       'r':-5,
                       'Q':9,
                       'q':-9,
                       'K':90,
                       'k':-90
                      }
          points = 0
          for char in state:
            points += whiteDict.get(char, 0)
          if not turn:
            points *= -1
          return points
          #INCOMPLETE
