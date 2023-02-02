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

def findLife(inputSeed):
    nSteps = 1000 #number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 #by default say 1000, so if you don't find it you return 1000
    #Creare un toroide --> lanciarlo --> 
    game = Toroid(seed = inputSeed, dimension = [15,15], native = 37.5) #game to play 
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
    return lifespan


def many_nativities():
    nativities = np.linspace(5,99,100) #100 nativities between 5 and 99
    averages = np.array([])
    for index in len(nativities):
        lives = [] #10 lives to make an average    
        for i in range(10):
            newLife = findLife(1000*(index+1)+i)
            lives.append(newLife)
        averages.append(np.mean(lives))

    return nativities, averages

def main():

    nativities = [37.5, 25, 50]
    outputNames = ["lifespan_15_375.txt","lifespan_15_25.txt","lifespan_15_50.txt"]

    time_init = time.time()
    for index in range(len(nativities)):
        nSeeds = 100 # numero di seeds
        lifes = np.array([])
        for i in range(nSeeds):
            newLife = findLife(1000*(index+1) + i)
            lifes = np.append(lifes, newLife)    
        
        nameOutputFile = outputNames[index]
        outputFile =  open(nameOutputFile, "w")
        for life in lifes:
            outputFile.write(str(life))
            outputFile.write("\n")
        outputFile.close()
    print("Time:", time.time()-time_init)

main()
