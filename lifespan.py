#Evaluates lifespan for various seeds and stores it to .txt file for further analysis

from board import Toroid
from constants import *
import numpy as np
import time

iterations = 1000

def grid_to_bin(matrice): # takes a grid and gives in output a string encoding the dead (with 0) alive (with 1) cells (it is more efficient than confronting numpy arrays)
    dimensions = matrice.shape
    output = ''
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            output = output + str(matrice[i][j])

    return output


def findLife(inputSeed, nativity): #runs game on input seed with selected nativity and returns lifespan
    nSteps = 1000 # number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 # by default say 1000, so if you don't find it you return 1000
    # The idea is to create a a toroid and look at its evolution (saving it every step)
    game = Toroid(seed = inputSeed, dimension = [15,15], native = nativity) # Initializes game to play
    stepsTaken = 0
    trovato = False #Boolean value to check if it has already entered a loop
    while stepsTaken < nSteps and not trovato:
        stringaNuova = grid_to_bin(game.grid) #calcola la configurazione attuale
        configurations = np.append(configurations, stringaNuova)
        game.grid = game.update() # updates the grid
        # Checks if equals
        if stepsTaken > 0:
            for j in range(len(configurations)-1):
                if(configurations[j] == stringaNuova):
                    lifespan = j
                    trovato = True

        stepsTaken += 1
    return lifespan, (stepsTaken-lifespan-1) # returns lifespan and period


def main():

    nativities = [12.5, 25, 37.5, 50, 62.5] # nativities considered
    outputNames = ["vite/lifespan_15_125.txt" ,"vite/lifespan_15_250.txt", "vite/lifespan_15_375.txt", "vite/lifespan_15_500.txt", "vite/lifespan_15_625.txt"]
    outputNames1 = ["vite/periodicity_15_125.txt" ,"vite/periodicity_15_250.txt", "vite/periodicity_15_375.txt", "vite/periodicity_15_500.txt", "vite/periodicity_15_625.txt"]

    time_init = time.time()
    for index in range(len(nativities)):
        nSeeds = 10000 # number of seeds on which to run the simulation
        lifes = np.array([])
        periods = np.array([])
        for i in range(nSeeds):
            newLife, periodicity = findLife(1000*(index+1) + i, nativities[index]) # returns lifetime and period of the determined initial grid
            lifes = np.append(lifes, newLife)
            periods = np.append(periods, periodicity)
        
        nameOutputFile = outputNames[index]
        outputFile =  open(nameOutputFile, "w")
        for life in lifes:
            outputFile.write(str(life))
            outputFile.write("\n")
        outputFile.close()

        nameOutputFile1 = outputNames1[index] 
        outputFile1 =  open(nameOutputFile1, "w")
        for period in periods:
            outputFile1.write(str(period))
            outputFile1.write("\n")
        outputFile1.close()
        print("Time at the end of the iteration ", index, " is:", time.time()-time_init)
main()
