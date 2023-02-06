# We run the game with various seeds, starting from different nativities and check how to
# asintotic occupancy varies with respect to the nativity.

from board import Toroid
from constants import *
import numpy as np
import time

def grid_to_bin(matrice): #Converts grid to string of 0s and 1s
    dimensions = matrice.shape
    output = ''
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            output = output + str(matrice[i][j])

    return output


def findStableOccupancy(inputSeed, nativity, size): # runs a game with initial seed inputSeed and nativity = nativity
    nSteps = 1000 # number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 # by default say 1000, so if you don't find it you return 1000

    game = Toroid(seed = inputSeed, dimension = [size,size], native = nativity) # game to play 
    stepsTaken = 0
    trovato = False
    period=1

    while stepsTaken < nSteps and not trovato:
        stringaNuova = grid_to_bin(game.grid) #Evaluates the actual configurations
        configurations = np.append(configurations, stringaNuova)
        game.grid = game.update() # updates the grid
        # Checks if equals
        if stepsTaken > 0:
            for j in range(len(configurations)-1):
                if(configurations[j] == stringaNuova):
                    lifespan = j
                    trovato = True
                    period = stepsTaken-j

        stepsTaken += 1

    media = 0 #average across steps

    if not trovato:
        period = 100
        lifespan = 899
        print("I didn't find a period!") # added in case an initial grid doesnt't reach the convergence

    for i in range(period):
        media += configurations[lifespan+i].count('1')
        
    media /= period 
    return media # returns the mean over all the occupancies of the loop period


def main():
    nativities = list(np.linspace(2,98,40).astype(int))
    meanOccupancies = [] # Average occupancies for each gridsize after stability is reached
    devst = []
    nSeeds = 300
 
    # For each nativity run the game for 100 patterns and calculate mean 
    time_init, last_time = time.time(), 0
    for i in range(len(nativities)): # for each nativity
        occupancies = []
        for j in range(nSeeds):
            seed = 2000*i+j
            occupancies.append(findStableOccupancy(inputSeed= seed, nativity = nativities[i], size=15))
            print("Nativity: ", nativities[i], "\tSeed number: ", seed, "\tAt time", time.time() - time_init, "\t duration", time.time() - last_time)
            last_time = time.time()
        meanOccupancies.append(np.mean(occupancies))
        devst.append(np.std(occupancies))
    #Prints on a file dimension \t meanOccupancy
    nameOutputFile = "nativity_vs_occupancy.txt"
    outputFile =  open(nameOutputFile, "w")
    for (nat,occ,sigma) in zip(nativities,meanOccupancies, devst):
        outputFile.write(str(nat))
        outputFile.write("\t")
        outputFile.write(str(occ))
        outputFile.write("\t")
        outputFile.write(str(sigma))
        outputFile.write("\n")
    outputFile.close()


main()
