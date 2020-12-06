import pyxel
from enum import Enum

Direction = Enum('W', 'N', 'E', 'S')


class Logic:
    '''
        Static classes to hold logic for each tile type.
    '''
    rules = []
    solid = False

    def __init__(self):
        raise Exception('Static class')


class EmptyLogic(Logic):
    pass


class TextLogic(Logic):
    solid = True


class BabaLogic(Logic):
    pass


class Tile:
    direction = Direction.E

    def draw():
        raise NotImplementedError()


class EmptyTile(Tile):
    logic = EmptyLogic

    def draw():
        pass


class TextTile(Tile):
    logic = TextLogic
    image_position = None

    def __init__(self, kind):
        pass


class IsTile(TextTile):

    def draw(self, x, y):
        # TODO how to get tile position?
        pyxel.blt(x, y, 0, 0, 8, 8, 8, 12)


class IsTile(TextTile):

    def draw(self, x, y):
        # TODO how to get tile position?
        pyxel.blt(x, y, 0, 0, 8, 8, 8, 12)
