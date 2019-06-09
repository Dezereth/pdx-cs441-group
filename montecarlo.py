# -*- coding: utf-8 -*-
import chess
import numpy as np
import random
import time
from operator import attrgetter
from matplotlib import pyplot as plt

#implementation based on Pseuocode at https://www.geeksforgeeks.org/ml-monte-carlo-tree-search-mcts/
class node:
    def __init__(self, state, parent, root=False, color=None, move=None):
        
        self.state = state
        self.parent = parent
        self.color = color
        self.children = []
        self.is_root = root
        self.ucb = 0
        self.visited = False
        self.wins = 0.0
        self.simulations = 0
        self.is_terminal = False
        self.move = move
        self.depth = 0

        if not self.is_root:
            if self.parent.color == "white":
                self.color = "black"
            else:
                self.color = "white"
            self.depth = self.parent.depth + 1

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
            children.append(node(new_state, self, move=mv))
            random.shuffle(children)
            self.children = children


class MonteCarlo():
    def __init__(self, ucb_constant=10):
        self.root = None
        self.ucb_constant = ucb_constant
        self.eps = 0.9
        self.epsilon = self.eps
        
    def reset(self):
        self.root = None
        self.epsilon = self.eps

    def search(self, starting_state, time_limit, color, debug=False):
        #main alogirithm, begins a search from a starting state given a time limit
        self.epsilon = 0.9
        self.root = node(starting_state, None, root=True, color = color)
        self.root.expand_children()
        #loop until time expires
        count = 0
        end = time.time()+time_limit
        depth_plot = []
        while time.time()<=end:
            #decrease the values that favor exploration
            if count % 40 == 0:
                if self.epsilon > 0.1:
                    self.epsilon -= .1
                if self.ucb_constant > 1:
                    self.ucb_constant -= 1
            #select a leaf
            leaf = self.select_child(self.root)
            depth_plot.append(leaf.depth)
            #simulate until an end condition
            sim_result = self.simulation(leaf)
            #back propogate the results up to the orginal starting node
            self.backprop(leaf, sim_result)
            count += 1
        if debug:
            print(f"Looped {count} times")
        #once time is up, return the the child node with the greatest evaluation based on the upper confidence bound
        if debug:
            for child in self.root.children:
                print("{0:.4f}%: {1:.4f} out of {2} for {3}".format((100*child.wins/child.simulations), child.wins, child.simulations, child.state)) #max(child.simulations for child in self.root.children)
        mx = -100
        best_move = None
        for child in self.root.children:
            if child.simulations > mx:
                best_move = child.move
                mx = child.simulations
        if debug:
            print(f"The current best move is {best_move}")
            plt.plot(depth_plot)
            plt.show()
        return best_move

    def select_child(self, node):
        #finds a leaf node - will first pick unvisited nodes, then switch to to highest UCB value 
        while self.fully_epanded(node):
            for child in node.children:
                child.calc_ucb(self.ucb_constant)
            node = max(node.children, key=attrgetter('ucb'))

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
        #Simulation only allo
        count = 0
        while not node.is_terminal and count < 10/self.epsilon:
            if node.children == []:
                node.expand_children()
            if random.random() < self.epsilon:
                node = random.choice(node.children)
            else:
                node = max(node.children, key=attrgetter('ucb'))
            count += 1
        #get results of
        board = chess.Board(node.state)
        if board.is_game_over():
            result = board.result()
        else:
            result = self.evaluate_board_state(node)
        return ((node, result))


    def evaluate_board_state(self, node):
    #need board state evaluation function
    #not implemented
        whiteDict = {'P':1,
                     'N':3,
                     'B':3,
                     'R':5,
                     'Q':9,
                     'K':90
                     }
        blackDict = {'p':1,
                     'n':3,
                     'b':3,
                     'r':5,
                     'q':9,
                     'k':90
                     }
        whitePoints = 0.0
        blackPoints = 0.0
        for char in node.state.split()[0]:
            whitePoints += whiteDict.get(char,0)
            blackPoints += blackDict.get(char,0)
        whiteScore = whitePoints/(whitePoints+blackPoints)
        blackScore = 1-whiteScore
        return f"{whiteScore}-{blackScore}"


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
        #print(result)
        node.simulations += 1
        [white,black] = result.split("-")
        if white == black:
            node.wins += .5
            return
        if node.color == 'white':
            if white == '1':
                node.wins += 0
            elif white == '0':
                node.wins += 1
            else:
                node.wins += float(black)
        elif node.color == 'black':
            if black == '1':
                node.wins += 0
            elif black == '0':
                node.wins += 1
            else:
                node.wins += float(white)

    def fully_epanded(self, node):
        #check if all chidlren have been visited
        if node.children == []:
            return False
        for child in node.children:
            if child.visited == False:
                return False
        return True

if __name__== '__main__':
    agent = MonteCarlo()
    agent.search('6R1/8/7K/k1p5/6r1/8/5P2/8 b - - 0 1',10,"black", debug=True)
    agent.search('6R1/8/7K/k1p5/6r1/8/5P2/8 w - - 0 1',10,"white", debug=True )
    #agent.search('4k3/8/8/8/7r/8/r7/4K3 b - - 0 1',5,"black")
    #agent.epsilon=0.9
    #agent.search('4k3/R7/8/8/7R/8/8/4K3 w - - 0 1',15,"white", debug=True)
    #agent.search('4k3/8/8/8/7r/8/r7/4K3 b - - 0 1',15,"black", debug=True)
    #agent.search("2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1",60,"white")
    #agent.search('4k3/8/8/8/8/8/8/R2K3R w - - 0 1',20,"white")

