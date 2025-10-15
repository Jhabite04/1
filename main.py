import sys
import pygame
import pygame_gui

from settings import *
from game_level import GameLevel
from menu import Start_menu
from board import *
import board

class Game(object):
    def __init__(self):

        
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption('Preyground')
        self.clock = pygame.time.Clock()

        #Controller
        self.level = GameLevel()
        self.start_menu_ = Start_menu()
        #游戏状态
        self.game_over = True

    @property
    def controller(self):
        if self.game_over:
            return self.start_menu_
        else:
            return self.level

    def run(self):

        self.controller.game_over = self.game_over 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.controller.reponse_click(event.pos)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.controller.reponse_button(event.ui_element)
            self.controller.manager.process_events(event)


        delta_time = self.clock.tick(20) / 1000
        self.controller.run(delta_time)

        self.game_over = self.controller.game_over

        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    while True:
        game.run()
