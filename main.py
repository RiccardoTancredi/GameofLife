import pygame

from board import Toroid
from constants import *
from draw import Draw
import numpy as np
from image_generator import gridFromImage
from pattern_generator import patternGenerator

import os
import imageio


# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')

pattern_zoo = {"block" : np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]),
              "bee_hive" : np.array([[0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0]]),
              "loaf" : np.array([[0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0]]),
              "boat" : np.array([[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]),
              "tub" : np.array([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]),
              
              "blinker" : np.array([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]]),
              "toad" : np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]),
              "beacon" : np.array([[0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0]]),

              "pulsar" : np.array([
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0], 
                  [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], 
                  [0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),

              "glider" : np.array([[0,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,1,1,1,0],[0,0,0,0,0]]),
              "simil_replicator" : np.array([[0,0,0,0,0,0,0], [0,0,0,1,1,1,0], [0,0,1,0,0,1,0], [0,1,0,0,0,1,0], [0,1,0,0,1,0,0], [0,1,1,1,0,0,0], [0,0,0,0,0,0,0]]),
              "replicator" : np.array([
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
                [0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

              }

pattern_period = {"block" : 1, #still lifes
              "bee_hive" : 1,
              "loaf" : 1,
              "boat" : 1,
              "tub" : 1,

              "blinker" : 2, #oscillators
              "toad" : 2,
              "beacon" : 2,

              "pulsar": 3,

              "glider": 4,  #spaceships
              "simil_replicator" : 10,
              "replicator" : 12
              }

name_image = "images/monna_lisa.jpg"
figure = "glider"
file_name = 'data/'+figure+'.txt'
pattern = pattern_zoo[figure]
seed = 123


#Scrivi "Inizializzamo la griglia"
#Se input == random seed dims fraction --> fai griglia random di dimensioni dims con seed seed e frazione fraction
#Se input == "monalisa", ... --> fai griglia pescando l'immagine (già fatta, facciamo un archivio)
#Se input == fromTxt --> fai griglia leggendo le istruzioni da un file di testo: patternGenerator(patternArray, posArray, chirArray, dimensions, random = None)
#Possibilità di aggiungere pattern durante l'esecuzione?

def prendiInput():
    print("Let's initialize the grid\n")
    print("Choose among random, fromTxt and easterEgg")
    comando = input("What do you want to do?\n")

    if comando == "fromTxt":
        lines = []
        patterns = []
        positions = []
        chiralities = []

        filein = input("Which file do you want to open?\n")
        file_name = 'initial_patterns/'+filein+'.txt'

        with open(file_name) as file:
            for line in file:
                line = line.replace("\n","")
                lines.append(line)
        #first row contains dimensions is written as dimx \t dimy

        dimsString = lines[0].split(",")
        dims = [int(dimsString[0]), int(dimsString[1])]
        if_random = (lines[1] == "True")
        lines.pop(0)
        lines.pop(0)
        
        for line in lines:
            #each row contains patterns, positions, chirs
            elm = line.split(",")
            patterns.append(pattern_zoo[elm[0]]) #pattern name
            positions.append([int(elm[1]), int(elm[2])]) #pattern position, taken as int
            chiralities.append(elm[3] == "True") #chiralities taken as boolean value

        griglia = patternGenerator(patterns, positions, chiralities, dims, random = if_random)
        game = Toroid(grid = griglia)
        return game

    elif comando == "easterEgg": #pescala dall'archivio
        print("Our library of images is:\n monalisa\norecchino\neinstein\nquantum\n")

        figure = input("Which one do you choose?\n")
        file_name = 'images_txt/'+figure+'.txt'
        griglia = np.loadtxt(file_name, delimiter=" ")
        game = Toroid(grid = griglia)
        return game
    
    elif comando == "amogus": 
        print("Amogus took possess of your pc!\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nNow I'm moving here\n")
        file_name = 'images_txt/amogus.txt'
        griglia = np.loadtxt(file_name, delimiter=" ")
        game = Toroid(grid = griglia)
        return game

    elif comando == "parisi": 
        print("Questo gioco è complesso, ed ora me ne vado, PUF!")
        file_name = 'images_txt/parisi.txt'
        griglia = np.loadtxt(file_name, delimiter=" ")
        game = Toroid(grid = griglia)
        return game

    elif comando == "random":
        inputSeed = input("Seed?")
        dim_ver = input("Vertical dimension?")
        dim_hor = input("Horizontal dimension?")
        nativity = input("Nativity?")
        inputDims =[int(dim_ver), int(dim_hor)]
        
        game = Toroid(seed=int(inputSeed), dimension=inputDims, native=float(nativity))
        return game
    
    else:
        print("Impara a scrivere! Ora farò come mi aggrada\n")
        seedR = np.random.randint(0, 1000)
        dim_hor, dim_ver = np.random.randint(10, 50), np.random.randint(10, 50)
        game = Toroid(seed=seedR, dimension=[int(dim_ver), int(dim_hor)])
        return game

game = prendiInput()
#game = Toroid(seed= 101, dimension=[30,30],native=38)
WIN = pygame.display.set_mode((game.height*SQUARE_SIZE, game.length*SQUARE_SIZE))
draw = Draw(WIN, game)
found_histo = []

drawing = True
iterations = int(1e6)
FPS = 60

# TO CREATE THE GIFS DECOMMENT THIS CODE
# image_togif_list = [0]*iterations
# gif_name = "animation" #input("Insert name of animation.gif\n")
# gif_rate = [0.1]*iterations
# gif_rate[0] = 3 #first image stays longer in final gif (useful for easter eggs)


def main():

    run = True
    time = 0
    clock = pygame.time.Clock()
    pause = False

    while run:
        if drawing:
            clock.tick(FPS)
            draw.update() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pause = False

        # found_histo = game.search_pattern(pattern=pattern, name=figure)
        game.grid = game.update()
        if time == 0:
            pygame.time.delay(3000) # To show the initial pattern
        pygame.time.delay(100) # To slow down the simulation

        # TO CREATE THE GIFS DECOMMENT THIS CODE
        #image_togif_list[time] = "gif_stills/"+ "frame_" + str(time) + ".png"
        #pygame.image.save(WIN, image_togif_list[time])

        time += 1
        # print(time)
        if (time/1000).is_integer():
            print(time)
        if time == iterations:
            print("Completed")
            run = False
    
    pygame.quit()

    # TO CREATE THE GIFS DECOMMENT THIS CODE
    # images = []
    # for instant in image_togif_list:
    #     images.append(imageio.imread(instant))
    # imageio.mimsave(os.path.join('gifs/' + gif_name + '.gif'), images, duration = gif_rate) # modify duration as needed

# testgrid = Toroid( grid=pattern_zoo[figure] )
# print(testgrid.Ipad(3))

main()
