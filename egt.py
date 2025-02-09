import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import imageio.v2 as imageio
import os
import shutil

stateC = 'O'
stateD = '|'
B = 1.55
n_iter = 200
L = 2000
mode = 'random'

class Player():
    def __init__(self, i, j, mode: str='stateC'):
        if mode == 'random':
            self.state = random.choice([stateC, stateD])
        elif mode == 'stateC':
            self.state = stateC
        elif mode == 'stateD':
            self.state = stateD
        self.old_state = self.state
        self.score = 0
        self.position = (i, j)
    
    def __str__(self):
        return self.state

class Scenario():
    def __init__(self, L, mode: str='stateC'):
        self.side = L
        self.board = np.ndarray([L, L], dtype=object)
        for i in range(L):
            for j in range(L):
                self.board[i][j] = Player(i, j, mode)
                
    def players(self):
        string = ''
        for row in self.board:
            for element in row:
                string += f'{element.state} '
            string += '\n'
        return f'{string}'
                
    def scores(self):
        string = ''
        for row in self.board:
            for element in row:
                string += f'{element.score} '
            string += '\n'
        return f'{string}'
    
    def neighbours(self, player: Player):
        I, J = player.position
        result = [
            ((I)%self.side, (J+1)%self.side),
            ((I+1)%self.side, (J)%self.side),
            ((I)%self.side, (J-1)%self.side),
            ((I-1)%self.side, (J)%self.side),
            ((I+1)%self.side, (J+1)%self.side),
            ((I-1)%self.side, (J+1)%self.side),
            ((I+1)%self.side, (J-1)%self.side),
            ((I-1)%self.side, (J-1)%self.side),
        ]
        random.shuffle(result)
        return result
    
    def update_states(self):
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j].old_state = self.board[i][j].state
        for i in range(self.side):
            for j in range(self.side):
                p = -np.inf
                neighbours_coordinates = self.neighbours(self.board[i][j])
                for (I, J) in neighbours_coordinates:
                    score2 = self.board[I][J].score
                    if score2 > p:
                        p = score2
                        self.board[i][j].state = self.board[I][J].old_state
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j].score = 0

    def count(self):
        countC = 0
        countD = 0
        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].state == stateC:
                    countC += 1
                elif self.board[i][j].state == stateD:
                    countD += 1
        countD = countD/(self.side**2)
        countC = countC/(self.side**2)
        return [countC, countD]

    def show_players(self):
        X, Y = np.meshgrid(list(range(self.side)), list(range(self.side)))
        plotter = []
        for i in range(self.side):
            for j in range(self.side):
                if self.board[i][j].state == stateC:
                    plotter.append(100)
                elif self.board[i][j].state == stateD:
                    plotter.append(0)

        graph = []        
        for i in range(self.side):
            graph.append(plotter[i*self.side:(i+1)*self.side])
        return [X, Y, graph]
        plt.pcolormesh(X, Y, graph, cmap='Greys', vmin=0, vmax=100)

def set_score(player1: Player, player2: Player):
    state1 = player1.state
    state2 = player2.state
    if state1 == stateC:
        if state2 == stateC:
            player1.score += 1/2
            player2.score += 1/2
        elif state2 == stateD:
            player2.score += B/2
    if state1 == stateD:
        if state2 == stateC:
            player1.score += B/2
    # player1.score = round(player1.score, 2)
    # player2.score = round(player2.score, 2)


def main():

    B = 1.50
    if mode == 'random':
        scenario = Scenario(L, mode=mode)
    elif mode == 'stateC':
        scenario = Scenario(L, mode=mode)
        scenario.board[int(L/2)][int(L/2)] = Player(int(L/2), int(L/2), mode='stateD')
    elif mode == 'stateD':
        scenario = Scenario(L, mode=mode)
        scenario.board[int(L/2)][int(L/2)] = Player(int(L/2), int(L/2), mode='stateC')

    plt.figure(figsize=(7, 7))
    try:
        os.mkdir('D:/computacional/Data Science/Nowak/images')
    except:
        pass
    for k in range(n_iter):
        plt.cla()
        X, Y, graph = scenario.show_players()
        plt.title(f'b={B}')
        plt.pcolormesh(X, Y, graph, cmap='Greys', vmin=0, vmax=100)
        plt.savefig(f'D:/computacional/Data Science/Nowak/images/t={k}.png')
        for i in range(L):
            for j in range(L):
                player1 = scenario.board[i][j]
                for (I, J) in scenario.neighbours(player1):
                    player2 = scenario.board[I][J]
                    set_score(player1, player2)
        scenario.update_states()

    images = []
    for k in range(n_iter):
        filename = f'images/t={k}.png'
        images.append(imageio.imread(filename))
    imageio.mimsave(f'D:/computacional/Data Science/Nowak/{mode}_B={B}_L={L}.gif', images)
    shutil.rmtree('D:/computacional/Data Science/Nowak/images')




if __name__ == "__main__":
    main()