# -*- coding: utf-8 -*-
import chess
import numpy as np

class node:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.children = []
        self.is_root = False
        self.ucb = 0
        self.visits = 0
        self.wins = 0
        self.simulations = 0
    
    def calc_ucb(constant):
        #calcualte the upper confidence bound for the node
        if self.visits == 0:
            self.ucb = 0
         (self.wins/self.simulations) + constant*np.sqrt(np.log(self.parent.simulations)/self.simulations)))
        

def simulation_node

class MonteCarlo():
    def __init__(self, boa):
        print("Monte-Carlo placeholder")
        self.root = None
        
    def search(self, starting_state, time_limit):
        self.root = node(starting_state, None)
        self.expand_children()
        while time_limit:
            pass


    def expand_children(self):
        for move in self.root.board.legal_moves:
            new_state = self.root.board.copy()
            new_state.push_san(move)
            self.root.children.append(node(new_state, parent=self.root))
        
    def select_child(node):
        #finds a leaf node
        while self.fully_epanded(node):
            node = max(child.ucb for child in node.chidlren)
        if 


    def fully_epanded(node):
        #check if all chidlren have been visited
        if node.chidlren = None:
            return False
        for child in node.chidlren:
            if child.visits = 0
                return False
        return True

if __name__== '__main__':
    board = chess.Board("2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1")
    move = MonteCarlo.search(board)

