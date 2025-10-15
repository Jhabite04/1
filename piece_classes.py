
from typing import List, Dict, Tuple
from settings import *
import pygame
from board import *

class Piece(pygame.sprite.Sprite):
    """ Piece类
        实例具有移动位置，判断吃子等方法.
        包含几个批量的控制棋子的类的方法，以及控制吃子的方法 """

    @classmethod
    def reset(cls):
        """ 初始化类变量 """
        cls.pos_list = [{}, {}]
        cls.piece_picked = [None]  # 储存被选中的Piece对象
        cls.game_over = [None]
        cls.turn = [0]
        cls.click_pos = [None]
        cls.reponse_num = 0

    def __init__(self, group, name, team: bool, *pos):

        super().__init__(group)

        self._pos = pos  # pos为行列数,左上角为0,0
        self.team = team  # team传入0或1
        self.name = name
        self._value = animal.index(self.name)+1  # 用ANIMAL列表中的顺序来代表棋子的价值，用来判断吃子
        self.pos_list[self.team][self.pos] = self
        self.starting_pos = pos  # Store the initial position
        self.captured = False

        # 图形
        self._image = pygame.Surface((48, 48))
        self.rect = self._image.get_rect(topleft=self.real_pos)
        self._font_surface = font.render(self.name, True, TEAM[self.team], 'white')

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        """ 将self._pos更新至cls.board """

        self.pos_list[self.team].pop(self.pos, 0)
        self._pos = pos
        self.pos_list[self.team][self.pos] = self
        self.rect = self.image.get_rect(topleft=self.real_pos)

        self.pos_list[not self.team].pop(self.pos, 1)

        if self.pos == LAIR[not self.team]:
            self.game_over[0] = True
        if not self.all_pos()[not self.team]:
            self.game_over[0] = True

        return self.pos

    @property
    def real_pos(self):
        """ Pieces' actual positons in the window """
        return (self.pos[0] * 50 + 1, self.pos[1] * 50 + 1)

    @property
    def value(self):
        # Set trapped piece to value 0
        if self.pos in TRAP[not self.team]:
            return 0
        else:
            return self._value

    @property
    def image(self):
        """ Image """
        self._image.fill("white")
        self._image.blit(self._font_surface, (10, 4))
        if self.piece_picked[0] == self:
            pygame.draw.rect(self._image, "gold", (0, 0, 48, 48), 3)
        return self._image

    def input(self, pos):
        """ 棋子响应传入坐标 """
        if pos:
            if self.turn[0] == self.team:
                # 被选中
                if self.piece_picked[0] == self:
                    if pos in self.moveable_area:
                        self.pos = pos
                        self.piece_picked[0] = None
                        self.turn[0] = not self.turn[0]
                        print("move", self.name, self.team, self.pos)
                    else:
                        self.piece_picked[0] = None
                        print("cancel", self.name, self.team)
                    self.click_pos[0] = None

                else:
                    if pos == self.pos:
                        self.click_pos[0] = None
                        self.piece_picked[0] = self
                        print("choose", self.name, self.team)

    def remove_from_group(self):
        if self.pos not in self.all_pos()[self.team]:
            if self.value == 8 and not self.captured:
                # If the piece value is 8 and it's captured for the first time, check if the starting position is empty
                if self.starting_pos not in self.all_pos()[0] and self.starting_pos not in self.all_pos()[1]:
                    self.captured = True
                    self.pos = self.starting_pos
                    print("reset to start", self.name, self.team, self.pos)
                else:
                    # Starting position is not empty, remove the piece
                    self.kill()
                    print("cannot reset, position occupied", self.name, self.team)
            else:
                self.kill()
                print("kill", self.name, self.team)

    def update(self):
        self.input(self.click_pos[0])
        self.remove_from_group()

    def compare_value(self, target_piece: 'Piece'):
        """ Compare the value of two pieces to determine if capturable. """

        # Trapped pieces can always be captured
        if target_piece.value == 0:
            print("is 1")
            return target_piece
        # Ant beats elephant
        elif self.value == 1 and target_piece.value == 12:
            print("is 2")
            return target_piece
        elif self.value == 12 and target_piece.value == 1:
            print("is 3")
            return self
        # Viper can kill (almost) anything
        elif self.value == 8 and target_piece.value != 13:
            print("is 4")
            return target_piece
        # Stink Bug not capturable by swallow, skink and eagle
        elif (self.value == 7 or self.value == 8 or self.value == 10) and target_piece.value == 3:
            print("is 5")
            return self
        # Beetle not capturable by beetle, spider and mantis
        elif (self.value == 4 or self.value == 5 or self.value == 6) and target_piece.value == 4:
            print("is 6")
            return self
        # Big beats small
        elif self.value >= target_piece.value:
            print("is 7")
            return target_piece
        elif self.value < target_piece.value:
            print("is 8")
            return self

    @property
    def moveable_area(self) -> list:
        """ 返回包含可移动的位置的列表"""
        self._moveable_area = []  # Resets target_area

        def get(*pos: tuple):
            # Avoid water and own pieces
            if pos not in WATER and pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
                if not (pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):

                    self._moveable_area.append(pos)

        get(self._pos[0], self._pos[1] + 1)
        get(self._pos[0], self._pos[1] - 1)
        get(self._pos[0] + 1, self._pos[1])
        get(self._pos[0] - 1, self._pos[1])

        # Extra movement for mantises
        if self.value == 6 and self.team == 0 and self._pos[1] <= 4:
            if self._pos[0] == 3 and self._pos[1] == 1:
                get(self._pos[0] + 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] - 1)
            elif self._pos[0] == 5 and self._pos[1] == 1:
                get(self._pos[0] + 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] + 1)
                get(self._pos[0] + 1, self._pos[1] - 1)
            else:
                get(self._pos[0] + 1, self._pos[1] + 1)
                get(self._pos[0] + 1, self._pos[1] - 1)
                get(self._pos[0] - 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] - 1)

        if self.value == 6 and self.team == 1 and self._pos[1] >= 4:
            if self._pos[0] == 3 and self._pos[1] == 7:
                get(self._pos[0] + 1, self._pos[1] - 1)
                get(self._pos[0] - 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] - 1)
            elif self._pos[0] == 5 and self._pos[1] == 7:
                get(self._pos[0] + 1, self._pos[1] - 1)
                get(self._pos[0] + 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] - 1)
            else:
                get(self._pos[0] + 1, self._pos[1] + 1)
                get(self._pos[0] + 1, self._pos[1] - 1)
                get(self._pos[0] - 1, self._pos[1] + 1)
                get(self._pos[0] - 1, self._pos[1] - 1)

        # Extra movement for spiders
        if self.value == 5 and self.team == 0 and self._pos[1] >= 4:
            get(self._pos[0] + 1, self._pos[1] + 1)
            get(self._pos[0] + 1, self._pos[1] - 1)
            get(self._pos[0] - 1, self._pos[1] + 1)
            get(self._pos[0] - 1, self._pos[1] - 1)

        if self.value == 5 and self.team == 1 and self._pos[1] <= 4:
            get(self._pos[0] + 1, self._pos[1] + 1)
            get(self._pos[0] + 1, self._pos[1] - 1)
            get(self._pos[0] - 1, self._pos[1] + 1)
            get(self._pos[0] - 1, self._pos[1] - 1)

        return self._moveable_area

    @classmethod
    def all_pos(cls) -> Tuple[List]:
        """ 返回指定队伍棋子的坐标 """
        team0_pos = list(cls.pos_list[0].keys())
        team1_pos = list(cls.pos_list[1].keys())
        return team0_pos, team1_pos, team0_pos + team1_pos

    @classmethod
    def all_piece(cls) -> Tuple[List['Piece']]:
        """ 返回包含所有棋子的元组 """
        team0_pieces = list(cls.pos_list[0].values())
        team1_pieces = list(cls.pos_list[1].values())
        return team0_pieces, team1_pieces, team0_pieces + team1_pieces

    @classmethod
    def piece_on(cls, pos) -> 'Piece':
        """ 通过传入坐标返回棋子对象 """
        if pos in cls.all_pos()[0]:
            return cls.pos_list[0][pos]
        elif pos in cls.all_pos()[1]:
            return cls.pos_list[1][pos]
        else:
            return None

    @classmethod
    def get_next_steps(cls, turn) -> List[tuple]:
        """ Obtain possible next move """
        next_steps = []
        for piece in cls.all_piece()[turn]:
            next_steps += map(lambda pos: (piece.pos, pos),
                              piece.moveable_area)
        return next_steps

    @staticmethod
    def convert_to_board(window_pos):
        """  Convert window positon to board positon"""
        return window_pos[0] // 50, window_pos[1] // 50


class Flying(Piece):

    def __init__(self, name, team, *pos):
        super(Flying, self).__init__(name, team, *pos)

    def river_moveable(self, pos):
        """ Check if there's obstacle in the water """
        delta_x = (self.pos[0]-pos[0])
        if delta_x:
            dir_x = (pos[0]-self.pos[0])/abs(self.pos[0]-pos[0])
            if self.pos[1] == 4:
                for i in range(1, 3):
                    if self.piece_on((self.pos[0] + i * dir_x, self.pos[1])):
                        return None
            else:
                for i in range(1, 4):
                    if self.piece_on((self.pos[0]+i*dir_x, self.pos[1])):
                        return None
        else:
            dir_y = (pos[1] - self.pos[1]) / abs(self.pos[1] - pos[1])
            if self.pos[0] == 3 or self.pos[0] == 5:
                if self.piece_on((self.pos[0], self.pos[1] + dir_y)):
                    return None
            else:
                for i in range(1, 4):
                    if self.piece_on((self.pos[0], self.pos[1] + i * dir_y)):
                        return None
        return True

    @property
    def moveable_area(self):
        """ Obtain moveable tiles """
        self._moveable_area = []

        def get(*pos: tuple):
            # Avoid own pieces
            if pos in WATER:
                if self._pos[0] == 3 or self._pos[0] == 5:
                    pos = (self._pos[0] + (pos[0] - self._pos[0]) * 3,
                           self._pos[1] + (pos[1] - self._pos[1]) * 2)
                elif self._pos[1] == 4:
                    pos = (self._pos[0] + (pos[0] - self._pos[0]) * 3, self._pos[1])
                else:
                    pos = (self._pos[0] + (pos[0]-self._pos[0]) * 4,
                           self._pos[1] + (pos[1]-self._pos[1]) * 4)

                if not self.river_moveable(pos):
                    return 0

            if pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
                if not (pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):
                    self._moveable_area.append(pos)

        get(self._pos[0], self._pos[1] + 1)
        get(self._pos[0], self._pos[1] - 1)
        get(self._pos[0] + 1, self._pos[1])
        get(self._pos[0] - 1, self._pos[1])
        return self._moveable_area


class Amphibious(Piece):
    def __init__(self, name, team, *pos):
        super(Amphibious, self).__init__(name, team, *pos)

    @property
    def back_color(self):
        """ 根据是否在河中切换背景色 """
        if self.pos in WATER:
            self._back_color = 'deepskyblue'
        else:
            self._back_color = 'white'
        return self._back_color

    @property
    def image(self):
        self._image.fill(self.back_color)
        self._font_surface = font.render(self.name, True, TEAM[self.team], self.back_color)
        self._image.blit(self._font_surface, (10, 4))
        if self.piece_picked[0] == self:
            pygame.draw.rect(self._image, "gold", (0, 0, 48, 48), 2)
        return self._image

    @property
    def moveable_area(self):
        """ Obtain moveable tiles """
        self._moveable_area = []  # reset target_area

        def get(*pos: tuple):
            if not (pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):
                if self._pos not in WATER:
                    # Avoiding own pieces
                    if pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:
                        self._moveable_area.append(pos)
                else:
                    if pos not in self.all_pos()[self.team] and pos not in self.all_pos()[not self.team]:
                        self._moveable_area.append(pos)

        get(self._pos[0], self._pos[1] + 1)
        get(self._pos[0], self._pos[1] - 1)
        get(self._pos[0] + 1, self._pos[1])
        get(self._pos[0] - 1, self._pos[1])
        return self._moveable_area


if __name__ == "__main__":
    pass
