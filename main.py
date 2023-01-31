import pygame

from board import Toroid
from constants import *
from draw import Draw
import numpy as np
# from image_generator import gridFromImage

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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
game = Toroid(period=pattern_period[figure], seed=123)#, image=name_image)

game.grid = game.create_grid()   # create the grid

draw = Draw(WIN, game)
found_histo = []

drawing = True
iterations = 300

with open(file_name, 'a') as f:
    f.write(f'# Width = {WIDTH}, Height = {HEIGHT}, Seed = {seed}, Num of iterations = {iterations}'+'\n')

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

        found_histo = game.search_pattern(pattern=pattern, name=figure)
        game.grid = game.update()
        # pygame.time.delay(5000)
        time += 1
        # print(time)
        with open(file_name, 'a') as f:
            if found_histo:
                f.write(str(time) + '\t')
                f.write(str(found_histo) + '\n')
        
        # if (time/1000).is_integer():
        #     print(time)
        if time == iterations:
            print("Completed")
            run = False
        # if time == 7 or time == 15 or time == 16 or time == 21:
        #     pygame.time.delay(15000)
    
    pygame.quit()

# testgrid = Toroid( grid=pattern_zoo[figure] )

# print(testgrid.Ipad(3))

main()

