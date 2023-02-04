from board import Toroid
from constants import *
import numpy as np
import time

iterations = 1000

def grid_to_bin(matrice):
    dimensions = matrice.shape
    output = ''
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            output = output + str(matrice[i][j])

    return output


def findLife(inputSeed, nativity):
    nSteps = 1000 #number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 #by default say 1000, so if you don't find it you return 1000
    #Creare un toroide --> lanciarlo --> 
    game = Toroid(seed = inputSeed, dimension = [15,15], native = nativity) #game to play 
    stepsTaken = 0
    trovato = False
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

        stepsTaken += 1
    return lifespan, (stepsTaken-lifespan-1)


def main():

    nativities = [12.5, 25, 37.5, 50, 62.5]
    outputNames = ["vite/lifespan_15_125.txt" ,"vite/lifespan_15_250.txt", "vite/lifespan_15_375.txt", "vite/lifespan_15_500.txt", "vite/lifespan_15_625.txt"]
    outputNames1 = ["vite/periodicity_15_125.txt" ,"vite/periodicity_15_250.txt", "vite/periodicity_15_375.txt", "vite/periodicity_15_500.txt", "vite/periodicity_15_625.txt"]

    time_init = time.time()
    for index in range(len(nativities)):
        nSeeds = 10000 # numero di seeds
        lifes = np.array([])
        periods = np.array([])
        for i in range(nSeeds):
            newLife, periodicity = findLife(1000*(index+1) + i, nativities[index])
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
