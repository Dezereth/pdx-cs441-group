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
        self.color = None
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
            if self.parent == "white":
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
    def __init__(self, ucb_constant=1):
        print("Monte-Carlo placeholder")
        self.root = None
        self.ucb_constant = ucb_constant
        self.epsilon = .9


    def search(self, starting_state, time_limit, color):
        #main alogirithm, begins a search from a starting state giben a time limit
        self.root = node(starting_state, None, root=True, color = color)
        self.root.expand_children()
        #loop until time expires
        count = 0
        end = time.time()+time_limit
        depth_plot = []
        while time.time()<=end:
            if count % 15 == 0:
                self.epsilon -= .1
            #select a leaf
            leaf = self.select_child(self.root)
            depth_plot.append(leaf.depth)
            #simulate until an end condition
            sim_result = self.simulation(leaf)
            #back propogate the results up to the orginal starting node
            self.backprop(leaf, sim_result)
            count += 1
        print(f"Looped {count} times")
        #once time is up, return the the child node with the greatest evaluation based on the upper confidence bound
        for child in self.root.children:
            print(f"{child.wins} out of {child.simulations} for {child.state}") #max(child.simulations for child in self.root.children)
        mx = -100
        best_move = None
        for child in self.root.children:
            if child.simulations > mx:
                best_move = child.move
                mx = child.simulations
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
        while not node.is_terminal and count < 40:
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
                node.wins += 1
            elif white == '0':
                node.wins += -1
            else:
                node.wins += float(white)
        elif node.color == 'black':
            if black == '1':
                node.wins += 1
            elif black == '0':
                node.wins += -1
            else:
                node.wins += float(black)

    def fully_epanded(self, node):
        #check if all chidlren have been visited
        if node.children == []:
            return False
        for child in node.children:
            if child.visited == False:
                return False
        return True

if __name__== '__main__':
    agent = MonteCarlo(1)

    agent.search('4k3/8/8/8/8/8/8/1R1K1R2 w - - 6 4',30,"white")

