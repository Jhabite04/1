import pygame
import json
import time
from settings import *
import piece_classes
from board import *
import board

class GameLevel(Controller):
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.piece_sprites = PieceGroup()

        self.setup()

        self.game_over = True

        """ GUI """
        self.manager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_LENGTH*9+2), starting_language='en')
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 0), (100, 50)),
                                                        text='Exit',
                                                        manager=self.manager)

    def setup(self):
        
        self.board = board.Board(self.all_sprites, 9, 9)

        
        piece_classes.Piece.reset()
        with open("pieces.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for i in data['piece']:
            piece_classes.Piece(self.piece_sprites,
                        i["name"], i["team"], *eval(i["pos"]))
        for i in data['flying']:
            piece_classes.Flying(self.piece_sprites,
                            i["name"], i["team"], *eval(i["pos"]))
        for i in data['amphibious']:
            piece_classes.Amphibious(self.piece_sprites,
                        i["name"], i["team"], *eval(i["pos"]))

    def check_game_over(self):
        if piece_classes.Piece.game_over[0]:
            self.game_over = True
            self.__init__()

    def blit_game_over(self):
        self.display_surface.fill('white')
        game_over_surface = font.render("game over", True, "black", "white")
        self.display_surface.blit(game_over_surface, (0, 0))
        pygame.display.update()
        time.sleep(1)

    def run(self, delta_time):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
        self.piece_sprites.draw(self.display_surface)
        self.piece_sprites.update()
        self.check_game_over()

        self.manager.update(delta_time)
        self.manager.draw_ui(self.display_surface)

    def response_click(self, pos):
        piece_classes.Piece.click_pos[0] = piece_classes.Piece.convert_to_board(pos)

    def response_button(self, ui_element):
        if ui_element == self.back_button:
            self.game_over = True
            self.__init__()
            print("back")

class PieceGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        for sprite in self.sprites():
            if sprite != sprite.piece_picked[0]:
                sprite.update(*args, **kwargs)
        for sprite in self.sprites():
            if sprite == sprite.piece_picked[0]:
                sprite.update(*args, **kwargs)
