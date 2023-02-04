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

def findLife(inputSeed, nativity, dimensione):
    nSteps = 1000 #number of steps in which we look at evolution
    configurations = np.array([])
    lifespan = 1000 #by default say 1000, so if you don't find it you return 1000
    #Creare un toroide --> lanciarlo --> 
    game = Toroid(seed = inputSeed, dimension = [dimensione, dimensione], native = nativity) #game to play 
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


def many_nativities(risoluzione, per_la_media, dimensione):
    nativities = np.linspace(5,99,risoluzione) #100 nativities between 5 and 99
    output = []
    time_init = time.time()
    for index in range(len(nativities)):
        lives = [] #10 lives to make an average    
        for i in range(per_la_media):
            newLife = findLife(2000*(index+2)+i+542, nativities[index], dimensione)
            lives.append(newLife)
        print("At the : ", index, "° iteration, the average is: ", np.mean(lives),"\tTime run:", time.time()-time_init)
        output.append(lives)
    return nativities, output

def main():
    time_init = time.time()
    nativity_steps = 50
    average_steps = 300
    nat, out = many_nativities(nativity_steps, average_steps, dimensione=15) # 50, 300
    print("Time:", time.time()-time_init)

    #stampa per ogni riga di out un file con gli elementi
    for i in range(nativity_steps):
        nameOutputFile = "nativities/" + str(i) + ".txt"
        outputFile =  open(nameOutputFile, "w")
        for j in range(average_steps):
            stringa = str(out[i][j])
            outputFile.write(stringa)
            outputFile.write("\n")
        outputFile.close()

    nameOutputFile1 = "nativities/mean_evaluated.txt"
    outputFile1 =  open(nameOutputFile1, "w")
    for j in range(nativity_steps):
        stringa = str(nat[j]) + "\t" + str(np.mean(out[j]))
        outputFile1.write(stringa)
        outputFile1.write("\n")
    outputFile1.close()

main()
