# -*- coding: utf-8 -*-
import chess
import numpy as np
import random
import time

#implementation based on Pseuocode at https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
class node:
    def __init__(self, state, parent, root=False, color=None):
        
        self.state = state
        self.parent = parent
        self.color = None
        self.children = []
        self.is_root = root
        self.ucb = 0
        self.visited = False
        self.wins = 0
        self.simulations = 0
        self.is_terminal = False

        if not self.is_root:
            if self.parent == "white":
                self.color == "black"
            else:
                self.color == "white"

        board = chess.Board(state)
        if board.is_game_over():
            self.is_terminal = True

    def calc_ucb(self,constant):
        #calcualte the upper confidence bound for the node
        if self.parent.simulations == 0 or self.simulations == 0:
            self.ucb = self.wins/self.simulations
        else:
            self.ucb = np.divide(self.wins,self.simulations) + constant * np.sqrt(np.divide(np.log(self.parent.simulations), self.simulations))
        
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
    def __init__(self, ucn_constant):
        print("Monte-Carlo placeholder")
        self.root = None
        self.ucb_constant = ucn_constant


    def search(self, starting_state, time_limit, color):
        #main alogirithm, begins a search from a starting state giben a time limit
        self.root = node(starting_state, None, root=True, color = color)
        self.root.expand_children()
        #loop until time expires
        count = 0
        end = time.time()+time_limit
        while time.time()<=end:
            #select a leaf
            leaf = self.select_child(self.root)
            #simulate until an end condition
            sim_result = self.simulation(leaf)
            #back propogate the results up to the orginal starting node
            self.backprop(leaf, sim_result)
            count += 1
        print(f"Looped {count} times")
        #once time is up, return the the child node with the greatest evaluation based on the upper confidence bound
        for child in self.root.children:
            print(f"{child.wins} out of {child.simulations} for {child.state}") #max(child.simulations for child in self.root.children)
        
    def select_child(self, node):
        #finds a leaf node - will first pick unvisited nodes, then switch to to highest UCB value 
        while self.fully_epanded(node):
            for child in node.children:
                child.calc_ucb(self.ucb_constant)
            max_ucb = -100
            for child in node.children:
                if child.ucb > max_ucb:
                    max_node = child
            node = max_node
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

    def backprop(self, leaf, result):
        ##not sure how to implement, don't know yet how to interpret results from game
        node = result[0]
        resul = result[1]
        while True:
            if node.is_root:
                break
            self.update_state(node, resul)
            node = node.parent

    def update_state(self, node, result):
        node.simulations += 1
        [white,black] = result.split("-")
        if white == black:
            node.wins += .5
            return
        if node.color == 'white':
            if white == '1':
                node.wins += 1
            else:
                node.wins += -1
        elif node.color == 'black':
            if black == '1':
                node.wins += 1
            else:
                node.wins += -1

        
        


    def fully_epanded(self, node):
        #check if all chidlren have been visited
        if node.children == None:
            return False
        for child in node.children:
            if child.visited == False:
                return False
        return True

if __name__== '__main__':
    agent = MonteCarlo(10)

    agent.search("2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1", 30, "white")

