# -*- coding: utf-8 -*-
import chess
import numpy as np
import random

#implementation based on Pseuocode at https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
class node:
    def __init__(self, state, parent, is_root=False):
        
        self.state = state
        self.parent = parent
        self.turn = None
        self.children = []
        self.is_root = is_root
        
        
        self.ucb = 0
        self.visited = False
        self.wins = 0
        self.simulations = 0
        self.is_terminal = False

        if not self.is_root:
            if self.parent.turn == "me":
                self.turn = "opp"
            else:
                self.turn = "me"

        board = chess.Board(state)
        if board.is_game_over():
            self.is_terminal = True

    def calc_ucb(self,constant):
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
            new_state=board.copy()
            new_state.push_san(mv)
            new_state = new_state.fen()
            children.append(node(new_state, self))
            self.children = children


class MonteCarlo():
    def __init__(self, color):
        print("Monte-Carlo placeholder")
        self.root = None
        self.color = None
        
    def search(self, starting_state, time_limit):
        #main alogirithm, begins a search from a starting state giben a time limit
        self.root = node(starting_state, None, is_root=True)
        self.root.turn == "me"
        self.root.expand_children()
        #loop until time expires
        while time_limit:
            #select a leaf
            leaf = self.select_child(self.root)
            #simulate until an end condition
            sim_result = self.simulation(leaf)
            #back propogate the results up to the orginal starting node
            backprop(leaf, sim_result)
        #once time is up, return the the child node with the greatest evaluation based on the upper confidence bound
        return max(child.vists for child in self.root.children)
        
    def select_child(self, node):
        #finds a leaf node
        while self.fully_epanded(node):
            for child in node.children:
                child.calc_ucb()
            node = max(child.ucb for child in node.children)
        if node.is_terminal:
        #if a terminal node, return self    
            return node
        for child in node.children:
        #returns an univisited child
            if not child.visited:
                child.visited = True
                return child
    
    def simulation(self, node):
        #simulate the game by choosing moves at random
        #Opponents moves are also chosen randomly
        while not node.is_terminal:
            if node.children == []:
                node.expand_children()
            node = random.choice(node.children)
            
        board = chess.Board(node.state)
        result = board.result()
        return ((node, result))

    def backprop(result):
        ##not sure how to implement, don't know yet how to interpret results from game
        while True:
            if node.is_root:
                return
            



    def fully_epanded(self, node):
        #check if all chidlren have been visited
        if node.children == None:
            return False
        for child in node.children:
            if child.visited == False:
                return False
        return True

if __name__== '__main__':
    agent = MonteCarlo("white")

    agent.search("2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1", 10)

