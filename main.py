import pygame

from board import Toroid
from constants import *
from draw import Draw

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GoF')

# dimension = (ROWS, COLS) 
game = Toroid()
grid = game.create_grid()   # create the grid
draw = Draw(WIN, game)

def main():
    run = True
    time = 0
    clock = pygame.time.Clock()
    pause = False

    while run:
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

        grid = game.update()
        time += 1
        if (time/1000).is_integer():
            print(time)
        if time > 10000:
            run = False

    pygame.quit()

main()
