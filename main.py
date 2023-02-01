import pygame

from board import Toroid
from constants import *
from draw import Draw
import numpy as np
from image_generator import gridFromImage
from pattern_generator import patternGenerator

FPS = 60

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')

pattern_zoo = {"block" : np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]),
              "bee_hive" : np.array([[0.5, 0, 0, 0, 0, 0.5], [0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0], [0.5, 0, 0, 0, 0, 0.5]]),
              "loaf" : np.array([[0.5, 0, 0, 0, 0, 0.5], [0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], [0.5, 0, 0, 1, 0, 0], [0.5, 0.5, 0, 0, 0, 0.5]]),
              "boat" : np.array([[0.5, 0, 0, 0, 0.5], [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0.5]]),
              "tub" : np.array([[0.5, 0, 0, 0, 0.5], [0, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 0], [0.5, 0, 0, 0, 0.5]]),
              
              "blinker" : np.array([[0.5, 0, 0, 0, 0.5], [0.5, 0, 1, 0, 0.5], [0.5, 0, 1, 0, 0.5], [0.5, 0, 1, 0, 0.5], [0.5, 0, 0, 0, 0.5]]),
              "toad" : np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]),
              "beacon" : np.array([[0, 0, 0, 0, 0.5, 0.5], [0, 1, 1, 0, 0.5, 0.5], [0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0], [0.5, 0.5, 0, 1, 1, 0], [0.5, 0.5, 0, 0, 0, 0]]),

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

              "glider" : np.array([[0.5,0,0,0,0.5],[0.5,0,1,0,0],[0,0,0,1,0],[0,1,1,1,0],[0,0,0,0,0]])
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

              "glider": 4  #spaceships
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
        filein = "initial_patterns/prova2.txt"

        with open(filein) as file:
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
        print("Our library of images is:\n monalisa.txt \norecchino.txt\neinstein.txt\n...")

        figure = input("Which one do you choose?")
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

    elif comando == "random":
        inputSeed = input("Seed?")
        dim_ver = input("Vertical dimension?")
        dim_hor = input("Horizontal dimension?")
        inputDims =[int(dim_ver), int(dim_hor)]
        
        game = Toroid(seed=int(inputSeed), dimension=inputDims)
        return game
    
    else:
        print("Impara a scrivere! Ora farò come mi aggrada\n")
        game = Toroid(seed = np.random.randint(0, 1000), dimension = np.random.randint(10, 50, 2))
        return game

game = prendiInput()
WIN = pygame.display.set_mode((game.height*SQUARE_SIZE, game.length*SQUARE_SIZE))
draw = Draw(WIN, game)
found_histo = []

drawing = True
iterations = 300000

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
        pygame.time.delay(5000)
        time += 1
        # print(time)
        if (time/1000).is_integer():
            print(time)
        if time == iterations:
            print("Completed")
            run = False
        # if time == 7 or time == 15 or time == 16 or time == 21:
        #     pygame.time.delay(15000)
    
    pygame.quit()

# testgrid = Toroid( grid=pattern_zoo[figure] )

# print(testgrid.Ipad(3))

main()
