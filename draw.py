import pygame

from constants import *

C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)

class Draw:
    def __init__(self, window, game):
        self.window = window
        self.game = game

        pygame.font.init()
        self.font = pygame.font.SysFont("monospace", 100)

    def update(self):
        self.draw_field()
        self.draw_cells()

        pygame.display.update()

    def draw_field(self):
        self.window.fill(C_BLACK)

    def draw_cells(self):
        for (row, col), cell in self.game.get_cells():
            color = BLACK if cell == 0 else WHITE
            self.draw_cell(color, row, col)

    def draw_cell(self, color, row, col):
        # print("Dentro draw la posizione vale: ", (row, col))
        if color == WHITE:
            image = C_WHITE
        else:
            image = C_BLACK
        pygame.draw.rect(self.window, image, pygame.Rect(col, row, 1.5*RADIUS, 1.5*RADIUS))