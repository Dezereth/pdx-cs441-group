# -*- coding: utf-8 -*-
import chess
import numpy as np
import copy

class node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.children = []
        self.is_root = False
        self.ucb = 0
        self.visits = 0
        self.wins = 0
        self.simulations = 0
        self.is_terminal = False


    def calc_ucb(constant):
        #calcualte the upper confidence bound for the node
        if self.visits == 0:
            self.ucb = 0
        self.ucb = (self.wins/self.simulations) + constant*np.sqrt(np.log(self.parent.simulations)/self.simulations)
        
    def expand_children(self):
        if self.is_terminal:
            return []
        
        children = []
        board = chess.Board(self.state)
        legal_moves = board.legal_moves

        for move in legal_moves:
            mv = board.san(move)
            print(board)
            new_state=board.copy()
            new_state.push_san(mv)
            print(new_state)
            print(board)
            new_state = new_state.fen()
            children.append(node(new_state, self))


class MonteCarlo():
    def __init__(self, color):
        print("Monte-Carlo placeholder")
        self.root = None
        self.color = None
        
    def search(self, starting_state, time_limit):
        self.root = node(starting_state, None)
        self.root.expand_children()
        while time_limit:
            leaf = self.select_child(self.root)
            sim_result = self.simulation(leaf)
        
    def select_child(self, node):
        #finds a leaf node
        while self.fully_epanded(node):
            node = max(child.ucb for child in node.chidlren)
        if node.terminal:
        #if a terminal node, return self    
            return node
        for child in node.chidlren:
        #returns an univisited child
            if child.visited == 0:
                child.visited == 1
                return child
    
    def simulation(self, node):
        while not node.is_terminal:
            pass


    def fully_epanded(self, node):
        #check if all chidlren have been visited
        if node.chidlren == None:
            return False
        for child in node.chidlren:
            if child.visits == 0:
                return False
        return True

if __name__== '__main__':
    agent = MonteCarlo("white")

    agent.search("2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1", 10)

