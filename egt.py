import numpy as np
import scipy as scp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random


def main():
    N = (41)**2     #Number of players squared
    b = 1         #Parameter

    x = np.linspace(0, int(np.sqrt(N))-1, int(np.sqrt(N)))
    y = np.linspace(0, int(np.sqrt(N))-1, int(np.sqrt(N)))

    X, Y = np.meshgrid(x, y)

    players = np.ndarray(shape=(N))
    graph = np.ndarray(shape=(N))
    replace = np.ndarray(shape=(N))

    neighbourhood = np.ndarray(shape=(N, N))

    for i in range(N):
        p = random.random()
        q = 0.9
        if p > q:
            players[i] = -1
        elif p < q:
            players[i] = 1


    score =np.ndarray(shape=(N))

    for i in range(N):  #Neighbourhood matrix values
        for j in range(N):
            if j in [(i + np.sqrt(N))%N, (i - np.sqrt(N))%N,
                     (i + np.sqrt(N) + 1)%N, (i - np.sqrt(N) + 1)%N,
                     (i + np.sqrt(N) - 1)%N, (i - np.sqrt(N) - 1)%N,
                     (i + 1)%N, (i - 1)%N]:
                neighbourhood[i][j] = 1
            else:
                neighbourhood[i][j] = 0

    plt.figure(figsize=(7,7))

    for _ in range(10000):
        
        if(_%100 == 0):
            b += 0.05
            plt.pause(1)

            for i in range(N):
                p = random.random()
                q = 0.9
                if p > q:
                    players[i] = -1
                    replace[i] = 0
                elif p < q:
                    players[i] = 1
                    replace[i] = 0
            
            players[int(N/2)] = -1

        for i in range(N):
            score[i] = 0

        for i in range(N):
            for j in range(N):
                if neighbourhood[i][j] == 1 and players[j] == 1:
                    if players[i] == 1:
                        score[i] += 1
                    elif players[i] == -1:
                        score[i] += b

        
        for i in range(N):
            max_value = 0
            neighbours = [(i + np.sqrt(N))%N, (i - np.sqrt(N))%N,
                        (i + np.sqrt(N) + 1)%N, (i - np.sqrt(N) + 1)%N,
                        (i + np.sqrt(N) - 1)%N, (i - np.sqrt(N) - 1)%N,
                        (i + 1)%N, (i - 1)%N, i%N]
            
            for j in range(8):
                k = int(random.choice(neighbours))
                neighbours.remove(k)
                if score[k] > max_value:
                    max_value = score[k]
                    replace[i] = players[k]
        
        for i in range(N):
            if replace[i] == 1 and players[i] == 1:
                graph[i] = 70
            elif replace[i] == 1 and players[i] == -1:
                graph[i] = 20
            elif replace[i] == -1 and players[i] == 1:
                graph[i] = 35
            elif replace[i] == -1 and players[i] == -1:
                graph[i] = 0
            elif players[i] == 1:
                graph[i] = 70
            elif players[i] == -1:
                graph[i] = 0
        
        for i in range(N):
            players[i] = replace[i]

        plotter=[]

        for i in range(int(np.sqrt(N))):
            plotter.append(graph[i*int(np.sqrt(N)):(i+1)*int(np.sqrt(N))])


        plt.cla()
        plt.title(f'{_} ; b = {b}')
        plt.pcolormesh(X, Y, plotter, cmap=cm.hsv, vmin = 0, vmax = 100)
        plt.pause(0.001)
    
        






if __name__ == "__main__":
    main()
