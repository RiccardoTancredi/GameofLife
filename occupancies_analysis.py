#This file simulates various seeds and checks the average occupancy found when the seeds stabilize.

from board import Toroid
from constants import *
import numpy as np
import time

def grid_to_bin(matrice):
    dimensions = matrice.shape
    output = ''
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            output = output + str(matrice[i][j])

    return output


def findLife(inputSeed, nativity): #runs a game with initial seed inputSeed and nativity = nativity
    nSteps = 1000 #number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 #by default say 1000, so if you don't find it you return 1000
    #Creare un toroide --> lanciarlo --> 
    game = Toroid(seed = inputSeed, dimension = [15,15], native = nativity) #game to play 
    stepsTaken = 0
    trovato = False
    period=0
    while stepsTaken < nSteps and not trovato:
        stringaNuova = grid_to_bin(game.grid) #calcola la configurazione attuale
        configurations = np.append(configurations, stringaNuova)
        game.grid = game.update() #update la griglia
        #Checks if equals
        if stepsTaken > 0:
            for j in range(len(configurations)-1): #guarda quelli prima
                if(configurations[j] == stringaNuova):
                    lifespan = j
                    trovato = True
                    period = j-stepsTaken

        stepsTaken += 1
    return lifespan, period


def main():
    grid_sizes = [5,10,15,20,25,30] #grids dimensions
    occupancies = [] #average occupancies for each gridsize after stability is reached
    nSeeds = 100

    #For each grid run the game for 100 patterns and calculate mean 

    # 1) Prima simuli nSeeds --> fai per ogni istante di tempo l'occupancy media --> media l'occupancy sugli ultimi 50 istanti
    # 2) SImula nSeeds --> per ogni seed guarda quando si stabilizza --> nel loop in cui è stabile fai la media delle occupancies --> media queste medie    

    # for grid_size in grid_sizes:

    

main()
