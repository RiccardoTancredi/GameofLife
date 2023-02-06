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


def findStableOccupancy(inputSeed, nativity, size): #runs a game with initial seed inputSeed and nativity = nativity
    nSteps = 1000 #number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 #by default say 1000, so if you don't find it you return 1000

    game = Toroid(seed = inputSeed, dimension = [size,size], native = nativity) #game to play 
    stepsTaken = 0
    trovato = False
    period=1

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
                    period = stepsTaken-j

        stepsTaken += 1

    media = 0 #average across steps

    if not trovato:
        period = 100
        lifespan = 899
        print("Non ho trovato un periodo!")


    for i in range(period):
        media += configurations[lifespan+i].count('1')
        
    media /= period
    return media


def main():
    grid_sizes = list(np.linspace(5,31,13).astype(int)) #grids dimensions
    meanOccupancies = [] #average occupancies for each gridsize after stability is reached
    dev_std = []
    nSeeds = 100
 
    #For each grid run the game for 100 patterns and calculate mean 

    # 1) Prima simuli nSeeds --> fai per ogni istante di tempo l'occupancy media --> media l'occupancy sugli ultimi 50 istanti
    # 2) SImula nSeeds --> per ogni seed guarda quando si stabilizza --> nel loop in cui è stabile fai la media delle occupancies --> media queste medie    

    time_init, last_time = time.time(), 0
    for i in range(len(grid_sizes)): #for each grid size
        occupancies = []
        for j in range(nSeeds):
            seed = 2000*i+j
            occupancies.append(findStableOccupancy(inputSeed= seed, nativity = 37.5, size=grid_sizes[i]))
            print("Grid size: ", grid_sizes[i], "\tSeed number: ", seed, "\tAt time", time.time() - time_init, "\t duration", time.time() - last_time)
            last_time = time.time()
        meanOccupancies.append(np.mean(occupancies))
        dev_std.append(np.std(occupancies))
    
    #Stampa su file dimensione \t meanOccupancy
    nameOutputFile = "dims_vs_occ2.txt"
    outputFile =  open(nameOutputFile, "w")
    for (dim,occ,sigma) in zip(grid_sizes,meanOccupancies, dev_std):
        outputFile.write(str(dim))
        outputFile.write("\t")
        outputFile.write(str(occ))
        outputFile.write("\t")
        outputFile.write(std(sigma))
        outputFile.write("\n")
    outputFile.close()


main()
