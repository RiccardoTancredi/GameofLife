from board import Toroid
from constants import *
import numpy as np
import os

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

              "pulsar":3,

              "glider":4  #spaceships
              }

iterations = 100

all_dimensions = [[15, 15], [18, 18]]
all_seeds = [123, 124]
def main():
    for dimensions in all_dimensions:
        for seed in all_seeds:
            folder_name = "data/"+str(dimensions[0])+"_"+str(dimensions[1])
            if not os.path.exists(folder_name):  
                os.makedirs(folder_name) 
            file_name = folder_name+"/"+str(seed)+'.csv'
            game = Toroid(seed=seed, dimension=dimensions)
            game.grid = game.create_grid()   # create the grid
            found_histo = []
            f = open(file_name, 'a')
            for index in range(len(pattern_zoo.keys())):
                f.write(f'{list(pattern_zoo.keys())[index]}')
                if index != len(pattern_zoo.keys())-1:
                    f.write(';')
            f.write('\n')

            run = True
            time = 0 
            
            while run:
                for figure in pattern_zoo.keys():
                    pattern = pattern_zoo[figure]
                    found_histo = game.search_pattern(pattern=pattern) 
                    if found_histo:
                        f.write(str(found_histo))    
                    else: 
                        f.write(str(0))

                    if figure != list(pattern_zoo.keys())[-1]:
                            f.write(';')

                game.grid = game.update()

                time += 1
                
                f.write('\n')
                # if (time/1000).is_integer():
                #     print(time)
                if time == iterations:
                    print(f"Completed: dim={dimensions}; seed={seed}")
                    f.close()
                    run = False

main()

