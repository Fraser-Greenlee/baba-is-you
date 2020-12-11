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

    def update(self, tile):
        pass

    def overlap(self, tile, overlaps):
        '''
            Act on tiles in `overlaps`
        '''
        pass

    def on_move(self, direction, amount):
        pass

    def on_destroy(self, tile):
        pass


class IsNoun:
    noun = NotImplemented

    def update(self, tile):
        new_tile = self.noun()
        new_tile.direction = tile.direction
        return new_tile


class IsProperty:
    # TODO apply property logic
    pass


class HasNoun:
    noun = NotImplemented

    def on_destroy(self):
        return self.noun()


class Shift:
    def overlap(self, tile, overlaps):
        for other in overlaps:
            other.move(tile.direction, 1)


class You:
    pass


class P1(You):
    pass


class P2(You):
    pass


class Defeat:
    def overlap(self, tile, overlaps):
        for other in overlaps:
            if issubclass(type(other), You):
                other.destroy()


class Win:
    def overlap(self, tile, overlaps):
        for other in overlaps:
            if issubclass(type(other), You):
                other.win()


class Stop:
    def on_move(self, direction, amount):
        return None, None


class EmptyLogic(Logic):
    pass


class TextLogic(Logic):
    solid = True


class BabaLogic(Logic):
    pass


class KekeLogic(Logic):
    pass


class FlagLogic(Logic):
    pass


class WallLogic(Logic):
    pass


class RockLogic(Logic):
    pass


class GrassLogic(Logic):
    pass


class TileLogic(Logic):
    pass


class WaterLogic(Logic):
    pass


class DoorLogic(Logic):
    pass


class PillarLogic(Logic):
    pass


class BoxLogic(Logic):
    pass


class Tile:
    direction = Direction.E
    sprite_pos = NotImplemented
    logic = NotImplemented
    want_to_move = [0, 0]  # What move does the tile make if nothing blocks it

    def move(self, direction, amount):
        '''
            Makes attempt to move this direction.
        '''
        direction, amount = self.logic.on_move(direction, amount)
        if direction is None:
            return None

        move_i = 0
        if direction in (Direction.W, Direction.E):
            move_i = 1

        move_coef = -1
        if direction in (Direction.N, Direction.E):
            move_coef = 1

        self.want_to_move[move_i] += amount * move_coef

    def destroy(self):
        pass

    def draw(self, x, y):
        pyxel.blt(
            x, y,
            self.sprite_pos[0], self.sprite_pos[1] * 8, self.sprite_pos[2] * 8,
            8, 8, 12
        )


class EmptyTile(Tile):
    logic = EmptyLogic

    def draw():
        pass


class DirectionalTileMixin:
    start_sprite = NotImplemented

    def draw(self, x, y):
        if self.direction == Direction.N:
            sprite_pos = [0, self.start_sprite[0], self.start_sprite[1]]
        elif self.direction == Direction.W:
            sprite_pos = [0, self.start_sprite[0], self.start_sprite[1] + 1]
        elif self.direction == Direction.E:
            sprite_pos = [0, self.start_sprite[0], self.start_sprite[1] + 2]
        elif self.direction == Direction.S:
            sprite_pos = [0, self.start_sprite[0], self.start_sprite[1] + 3]
        else:
            raise Exception('Unknown direction')

        pyxel.blt(
            x, y,
            sprite_pos[0], sprite_pos[1] * 8, sprite_pos[2] * 8,
            8, 8, 12
        )


class BaBaTile(Tile, DirectionalTileMixin):
    logic = BabaLogic
    start_sprite = [1, 2]


class KeKeTile(Tile, DirectionalTileMixin):
    logic = KekeLogic
    start_sprite = [5, 2]


class FlagTile(Tile):
    logic = FlagLogic
    sprite_pos = [0, 2, 2]


class WallTile(Tile):
    logic = WallLogic
    sprite_pos = [0, 3, 2]


class RockTile(Tile):
    logic = RockLogic
    sprite_pos = [0, 4, 2]


class GrassTile(Tile):
    logic = GrassLogic
    sprite_pos = [0, 2, 3]


class TileTile(Tile):
    logic = TileLogic
    sprite_pos = [0, 3, 3]


class WaterTile(Tile):
    logic = WaterLogic
    sprite_pos = [0, 4, 3]


class DoorTile(Tile):
    logic = DoorLogic
    sprite_pos = [0, 3, 4]


class PillarTile(Tile):
    logic = PillarLogic
    sprite_pos = [0, 4, 4]


class BoxTile(Tile):
    logic = BoxLogic
    sprite_pos = [0, 4, 5]


class TextTile(Tile):
    logic = TextLogic


class PropertyTile(TextTile):
    pass


class YouTextTile(PropertyTile):
    sprite_pos = [0, 1, 1]


class WinTextTile(PropertyTile):
    sprite_pos = [0, 2, 1]


class StopTextTile(PropertyTile):
    sprite_pos = [0, 3, 1]


class PushTextTile(PropertyTile):
    sprite_pos = [0, 4, 1]


class MoveTextTile(PropertyTile):
    sprite_pos = [0, 5, 1]


class P1TextTile(PropertyTile):
    sprite_pos = [0, 6, 1]


class P2TextTile(PropertyTile):
    sprite_pos = [0, 7, 1]


class PullTextTile(PropertyTile):
    sprite_pos = [0, 1, 7]


class ShiftTextTile(PropertyTile):
    sprite_pos = [0, 2, 7]


class DeadTextTile(PropertyTile):
    sprite_pos = [0, 3, 7]


class SinkTextTile(PropertyTile):
    sprite_pos = [0, 4, 7]


class JumpTextTile(PropertyTile):
    sprite_pos = [0, 5, 7]


class OperatorTile(TextTile):
    pass


class OnTile(OperatorTile):
    sprite_pos = [0, 0, 0]


class IsTile(OperatorTile):
    sprite_pos = [0, 0, 1]


class HasTile(OperatorTile):
    sprite_pos = [0, 0, 2]


class NotTile(OperatorTile):
    sprite_pos = [0, 0, 3]


class MakeTile(OperatorTile):
    sprite_pos = [0, 0, 4]


class AndTile(OperatorTile):
    sprite_pos = [0, 0, 5]


class NounTile(TextTile):
    pass


class BaBaTextTile(NounTile):
    sprite_pos = [0, 1, 0]


class FlagTextTile(NounTile):
    sprite_pos = [0, 2, 0]


class WallTextTile(NounTile):
    sprite_pos = [0, 3, 0]


class RockTextTile(NounTile):
    sprite_pos = [0, 4, 0]


class KekeTextTile(NounTile):
    sprite_pos = [0, 5, 0]


class BoxTextTile(NounTile):
    sprite_pos = [0, 1, 6]


class PillarTextTile(NounTile):
    sprite_pos = [0, 2, 6]


class DoorTextTile(NounTile):
    sprite_pos = [0, 3, 6]


class GrassTextTile(NounTile):
    sprite_pos = [0, 4, 6]


class TileTextTile(NounTile):
    sprite_pos = [0, 5, 6]


class WaterTextTile(NounTile):
    sprite_pos = [0, 6, 6]
