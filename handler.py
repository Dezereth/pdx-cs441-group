# -*- coding: utf-8 -*-
"""
CS441 Group Programming assignment

An implementation of competing chess playing AI

Members:
    Ray Emory
    Wen Wu
    Dalton Gray
    Rawah Alsinan
    Jordan Dearborn-Childs
"""

#%%
import chess
import chess.pgn
import montecarlo
import minimax
import datetime
import random

#%%

class Handler():
    def __init__(self, monte, mini, board=chess.Board()):
        self.monte = monte
        self.mini = mini
        self.board = board.copy()
        self.starting = board.copy()
        self.time = 30
        
    def adjMini(self, limit):
        self.mini.limit = limit
    
    def adjMonte(self, time):
        self.time = time
    
    def moveMonte(self):
        """
        Queries the MonteCarlo search for the best move on the current board.
        catches and pushes move, updating the board.
        """
        #search(self, starting_state, time_limit, color):
        catch = self.monte.search(starting_state=self.board.fen(), time_limit=self.time, color='white' if self.board.turn else 'black', debug=True)
        self.board.push_san(catch)
        catch = self.board.pop()
        self.board.push(catch)
        return catch
    
    def moveMini(self):
        """
        Queries the MiniMax search for the best move on the current board.
        Catches and pushes move, updating the board.
        """
        catch = None
        catch = self.mini.getMove(self.board.copy())
        if not isinstance(catch, chess.Move):
            catch = self.miniBugWorkaround()
        self.board.push(catch)
        return catch
    
    def miniBugWorkaround(self):
        moves = []
        for i in self.board.legal_moves:
            moves.append(i)
        random.shuffle(moves)
        return moves[0]
    
    def miniVmonte(self, maxTurns=30, rounds=1, event="Mini_vs_Monte"):
        """
        Starts a competetive game between Mini and Monte, with Mini moving first
        """
        games = []
        fileStr = event+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["Event"]=event
            game.headers["Date"]=datetime.datetime.now().strftime("%Y.%m.%d")
            game.headers["White"]="MiniMax"
            game.headers["Black"]="Montecarlo"
            game.headers["Round"]=rnd+1
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games

    def monteVmini(self, maxTurns=30, rounds=1, event="Monte_vs_Mini"):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = event+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["Event"]=event
            game.headers["Date"]=datetime.datetime.now().strftime("%Y.%m.%d")
            game.headers["White"]="Montecarlo"
            game.headers["Black"]="MiniMax"
            game.headers["Round"]=rnd+1
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games
    
    def miniVmini(self, maxTurns=30, rounds=1, event="Mini_vs_Mini"):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = event+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["Event"]=event
            game.headers["Date"]=datetime.datetime.now().strftime("%Y.%m.%d")
            game.headers["White"]="MiniMax"
            game.headers["Black"]="MiniMax"
            game.headers["Round"]=rnd+1
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games
    
    def monteVmonte(self, maxTurns=30, rounds=1, event="Monte_vs_Monte"):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = event+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["Event"]=event
            game.headers["Date"]=datetime.datetime.now().strftime("%Y.%m.%d")
            game.headers["White"]="MonteCarlo"
            game.headers["Black"]="Montecarlo"
            game.headers["Round"]=rnd+1
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games

#%%

class miniEvaluator():
    def __init__(self, mini=minimax.MiniMax(), board=chess.Board()):
        self.mini = mini
        self.board = board.copy()
        self.starting = board.copy()
    
    def evaluate(self, depth=8, trials=1):
        bigStats = []
        fileStr = "MiniEvaluator_D"+str(depth)+"T"+str(trials)+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".txt"
        for j in range(trials):
            stats = []
            print("Trial: {}".format(j+1))
            for i in range(1,depth+1):
                print("Depth: {}".format(i))
                self.mini.limit = i
                start = datetime.datetime.now()
                catch = self.mini.getMove(self.board.copy())
                end = datetime.datetime.now()
                diff = end-start
                stats.append( (i, diff.total_seconds()) )
            bigStats.append(stats)
        with open(fileStr, 'w') as f:
            for l in bigStats:
                f.write("%s\n" % l)
        return bigStats

#%%

def main():
    monte = montecarlo.MonteCarlo()
    minim = minimax.MiniMax(limit=5)

    #me = miniEvaluator()
    #me.evaluate(depth=6, trials=1)
    
    
#King-Rook-Pawn game
    #boardKRP=chess.Board('2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1')
    #handy = Handler(mini=minim, monte=monte, board=boardKRP.copy())
    #handy.adjMonte(time=120)
    #handy.miniVmonte(maxTurns=10, rounds=1)
    #handy.monteVmini(maxTurns=25, rounds=5)

#King-Rook-Rook game
#    boardKRR=chess.Board('rkr5/8/8/8/8/8/8/5RKR w - - 0 1')
#    handy = Handler(mini=minim, monte=monte, board=boardKRR.copy())
#    handy.adjMonte(time=120)
#    handy.miniVmonte(maxTurns=25, rounds=5, event="Mini vs Monte RKR")
    #handy.monteVmini(maxTurns=25, rounds=5, event="Monte vs Mini RKR")

#Regular game
    #board=chess.Board()
    #handy = Handler(mini=minim, monte=monte, board=board.copy())
    #handy.adjMonte(time=120)
    #handy.miniVmonte(maxTurns=75, rounds=1)
    #handy.monteVmini(maxTurns=75, rounds=1)

#Hunter games

    boardHunt1=chess.Board('2k5/8/8/8/8/8/8/R2K3R w - - 0 1')
    #boardHunt2=chess.Board('2k5/8/8/8/8/8/8/B2K3R w - - 0 1')
    #boardHunt3=chess.Board('2k5/8/8/8/8/8/8/B2K3N w - - 0 1')
    #handy = Handler(mini=minim, monte=monte, board=boardHunt1.copy())
    #handy.adjMonte(time=120)
    #handy.miniVmonte(maxTurns=15, rounds=5, event="Mini vs Monte 2R Hunt")
    #handy.monteVmini(maxTurns=15, rounds=1, event="Monte vs Mini 2R Hunt")
    #handy.starting = boardHunt2.copy()
    #handy.miniVmonte(maxTurns=15, rounds=5, event="Mini vs Monte BR Hunt")
    #handy.monteVmini(maxTurns=15, rounds=5, event="Monte vs Mini BR Hunt")
    #handy.starting = boardHunt3.copy()
    #handy.miniVmonte(maxTurns=15, rounds=5, event="Mini vs Monte BN Hunt")
    #handy.monteVmini(maxTurns=15, rounds=5, event="Monte vs Mini BN Hunt")



#%%
def pgnTest():
        game = chess.pgn.Game()
        game.headers["White"]="MiniMax"
        game.headers["Black"]="Montecarlo"
        game.headers["Round"]=1
        game.headers["FEN"]='2kr4/2p5/8/8/8/8/5P2/4RK2 w - - 0 1'
        #game.headers["FEN"]='4k3/ppp5/8/8/8/8/3PP3/2BQK3 w - - 0 1'
        return game
#%%
if __name__ == '__main__':
    main()