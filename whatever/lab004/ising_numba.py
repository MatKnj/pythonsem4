import numpy as np
import matplotlib.pyplot as plt

import numba as nb

from matplotlib.animation import FuncAnimation
from IPython.display import HTML




#losowanie tablicy

@nb.njit
def los_tablica(n):

    tablica = np.random.randint(0, 2, (n, n))

    for i in range(n):
        for j in range(n):
            if tablica[i][j] == 0:
                tablica[i][j] = -1


    return tablica


#delta E / mikrokrok

@nb.njit
def mikrokrok(state, i, j, J, B, beta):
    height, width = state.shape

    count = 0

    for di in range(-1, 2):
        for dj in range(-1, 2):
            if not (di == 0 and dj == 0):

                ni = (i + di) % height
                nj = (j + dj) % width

                count += state[ni][nj]


    delta = 2 * state[i][j] * (J * count + B)

    if delta < 0:
        return -1 * state[i][j]

    else:
        if np.random.rand() <= np.exp(-1 * beta * delta):
            return -1 * state[i][j]

        else:
            return state[i][j]
        

#magnetyzacja

@nb.njit
def magnetyzacja(state): 
    
    height, width = state.shape 

    return np.sum(state)/(height*width)



#energia

@nb.njit
def energiaH(state, J, B):
    H = -1 * B * np.sum(state)

    height, width = state.shape

    sumy_sasiadow = 0

    for i in range(height):
        for j in range(width):

            count = 0

            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if not (di == 0 and dj == 0):

                        ni = (i + di) % height
                        nj = (j + dj) % width

                        count += state[ni][nj]

            sumy_sasiadow += count * state[i][j]


    H += -1 * J * sumy_sasiadow / 2

    return H


#makrokrok

@nb.njit
def makrokrok(state, J, B, beta):

    height, width = state.shape

    next_state = state.copy()

    for n in range(height * width):
        
        i = np.random.randint(0, height)
        j = np.random.randint(0, width)
        
        next_state[i][j] = mikrokrok(next_state, i, j, J, B, beta)


    return next_state


#symulacja

@nb.njit
def symulacja(M, N, J, B, beta):
    state = los_tablica(N)

    history = [state]
    E_history = [energiaH(state, J, B)]
    M_history = [magnetyzacja(state)]


    for i in range(M):
        state = makrokrok(state, J, B, beta)
        history.append(state)
        E_history.append(energiaH(state, J, B))
        M_history.append(magnetyzacja(state))


    return history, E_history, M_history