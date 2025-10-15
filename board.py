import pygame
from settings import *

animal = ["Ant", "Hallucigenia", "Stink Bug", "Beetle", "Spider", "Mantis", "Swallow", "Skink", "Viper", "Eagle", "Hippo", "Elephant"]

BOARD_ROW = 9
BOARD_COLUMN = 9
TEAM = ("white", "black")
WATER: tuple = (
    (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 3), (2, 4), (3, 5), (5, 3), (6, 4), (5, 5), (6, 3), (6, 5), (7, 7), (3, 4), (3, 5)
)
LAIR = ((4, 0), (4, 8))
TRAP = ((3, 0), (4, 1), (5, 0), (3, 8), (4, 7), (5, 8))

CELL_WIDTH, CELL_LENGTH = 50, 50
WINDOW_SIZE = (CELL_WIDTH * 9 + 200, CELL_LENGTH * 9 + 200)
DELTA_X = 7
DELTA_Y = 5

class Board(pygame.sprite.Sprite):
    def __init__(self,group,width,height):
        super().__init__(group)
        self.width = width
        self.height = height

        self.image = pygame.Surface((width*50,height*50))
        self.rect = self.image.get_rect()
        self.draw_board()

    def draw_board(self):

        self.image.fill('green')

        # Draw tile
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(self.image, "black", (x * 50, y * 50, 50, 50), 1)

        # Water
        for i in WATER:
            pygame.draw.rect(self.image,"deepskyblue",(i[0]*50, i[1] * 50, 50, 50), 0)

        # Trap
        for i in TRAP:
            pygame.draw.rect(self.image,"red",(i[0]*50, i[1] * 50, 50, 50), 1)

        # Lair
        for i in LAIR:
            pygame.draw.rect(self.image, "grey", (i[0]*50, i[1] * 50, 50, 50), 1)

    def update(self):
        pass
