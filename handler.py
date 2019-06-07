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

#%%

class Handler():
    def __init__(self, monte, mini, board=chess.Board()):
        self.monte = monte
        self.mini = mini
        self.board = board.copy()
        self.starting = board.copy()
    
    def moveMonte(self, time=30):
        """
        Queries the MonteCarlo search for the best move on the current board.
        catches and pushes move, updating the board.
        """
        #search(self, starting_state, time_limit, color):
        catch = self.monte.search(starting_state=self.board.fen(), time_limit=time, color='white' if self.board.turn else 'black')
        self.board.push_san(catch)
        catch = self.board.pop()
        self.board.push(catch)
        return catch
    
    def moveMini(self):
        """
        Queries the MiniMax search for the best move on the current board.
        Catches and pushes move, updating the board.
        """
        catch = self.mini.getMove(self.board.copy())
        self.board.push(catch)
        return catch
    
    def miniVmonte(self, maxTurns=30, rounds=1):
        """
        Starts a competetive game between Mini and Monte, with Mini moving first
        """
        games = []
        fileStr = "Mini_vs_Monte_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
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
                #print(catch)
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                #print(catch)
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games

    def monteVmini(self, maxTurns=30, rounds=1):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = "Mini_vs_Monte_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["White"]="Montecarlo"
            game.headers["Black"]="MiniMax"
            game.headers["Round"]=rounds
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                print(catch)
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                print(catch)
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games
    
    def miniVmini(self, maxTurns=30, rounds=1):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = "Mini_vs_Monte_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["White"]="MiniMax"
            game.headers["Black"]="MiniMax"
            game.headers["Round"]=rounds
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                print(catch)
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                print(catch)
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games
    
    def monteVmonte(self, maxTurns=30, rounds=1):
        """
        Starts a competetive game between Mini and Monte, with Monte moving first
        """
        games = []
        fileStr = "Mini_vs_Monte_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".pgn"
        for rnd in range(rounds):
            self.board = self.starting.copy()
            game = chess.pgn.Game()
            game.headers["White"]="MonteCarlo"
            game.headers["Black"]="Montecarlo"
            game.headers["Round"]=rounds
            game.headers["FEN"]=self.board.fen()
            turns = 0
            node = game
            while turns < maxTurns:
                print('Turn: {}'.format(turns+1))
                if self.board.is_game_over():
                    break
                catch = self.moveMonte()
                print(catch)
                node = node.add_variation(catch)
                if self.board.is_game_over():
                    break
                catch = self.moveMini()
                print(catch)
                node = node.add_variation(catch)
                turns += 1
            print(game, file=open(fileStr, "a+"), end="\n\n")
            games.append(game)
        return games
        

def main():
    monte = montecarlo.MonteCarlo()
    minim = minimax.MiniMax()
    
    handy = Handler(mini=minim, monte=monte, board=chess.Board('8/8/2kr4/2p5/5P2/4RK2/8/8 w - - 0 1'))
    handy.miniVmonte()
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