import pygame
import pygame_gui
from abc import ABCMeta, abstractmethod

pygame.init()

font = pygame.font.SysFont("Times New Roman", 20)



class Controller(metaclass = ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def response_click(self):
        pass

    @abstractmethod
    def response_button(self):
        pass

    @abstractmethod
    def run(self):
        pass

