import re
from typing import Optional, Tuple
import pyxel

from utils import Direction, Point, get_all_lowest_level_subclasses, Cell


class LogicMixin:
    '''
        Classes to apply logic to each tile type.
    '''
    rules = []
    solid = False

    def __init__(self):
        raise Exception('Handle parse paths.')

    @staticmethod
    def parse_tiles(tiles):
        raise NotImplementedError()

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


def get_nouns_before_term(command, term):
    return [
        cmd for cmd in command[:command.index(term)] if type(cmd) in ALL_NOUN_TILE_CLASSES
    ]


def get_propertiies_after_term(command, term):
    return [
        cmd for cmd in command[command.index(term):] if type(cmd) in ALL_PROPERTY_TILE_CLASSES
    ]


def tile_matches(pattern, tiles):
    tiles_str = ' '.join(str(t) for t in tiles)

    tile_indices = {}
    length = 0
    for tile in tiles:
        tile_indices[l] = tile
        length += str(tile) + 1

    tiles = []
    for match in re.finditer(pattern, tiles_str):
        tiles.append(tile_indices[match.start()])
    return tiles


class IsNoun(LogicMixin):
    def __init__(self, new_noun):
        self.new_noun = new_noun
        super().__init__()

    @staticmethod
    def parse_tiles(tiles):
        chage_from_nouns = tile_matches(r'(noun)? and (noun) is', tiles)
        chage_to_nouns = tile_matches(r' is (noun)', tiles)

        for change_from in chage_from_nouns:
            # TODO apply IsNoun methods
            import pdb; pdb.set_trace()

    def update(self, tile):
        new_tile = self.new_noun()
        new_tile.direction = tile.direction
        return new_tile


class IsProperty(LogicMixin):
    @staticmethod
    def parse_tiles(tiles):
        import pdb; pdb.set_trace()


class Has(LogicMixin):
    noun = NotImplemented

    @staticmethod
    def parse_tiles(tiles):
        import pdb; pdb.set_trace()

    def on_destroy(self):
        return self.noun()


class Make(LogicMixin):
    noun = NotImplemented

    def update(self, tile):
        new_tile = self.noun()
        new_tile.direction = tile.direction
        return tile, new_tile


class Shift(LogicMixin):
    def overlap(self, tile, overlaps):
        for other in overlaps:
            other.move(tile.direction, 1)


class You:
    pass


class P1(You):
    pass


class P2(You):
    pass


class Sink:
    def overlap(self, tile, overlaps):
        for other in overlaps:
            other.destroy()
            self.destroy()
            break


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


class LavaLogic(Logic):
    pass


class BrickLogic(Logic):
    pass


class IceLogic(Logic):
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
    cell = None

    def __init__(self, cell: Cell, drection: Optional[Direction] = None) -> None:
        self.cell = cell
        if drection:
            self.direction = drection

    def is_index(self, index: int) -> Optional[Direction]:
        if index == self.sprite_pos.x + 32 * self.sprite_pos.y:
            return self.direction

    def destroy(self):
        pass

    def draw(self):
        pyxel.blt(
            self.cell.position.x * 8, self.cell.position.y * 8,
            0, self.sprite_pos.x * 8, self.sprite_pos.y * 8,
            8, 8, 12
        )


class EmptyTile(Tile):
    logic = EmptyLogic

    def is_index(self, index: int) -> Optional[Direction]:
        if index == 0:
            return self.direction

    def draw(self):
        pass


DIRECTIION_MAP = [Direction.N, Direction.W, Direction.E, Direction.S]


class DirectionalTile(Tile):
    start_sprite: Point = NotImplemented

    def is_index(self, index: int) -> Tuple[bool, Direction]:
        start_index = self.start_sprite.x + 32 * self.start_sprite.y
        indices = [start_index + 32 * i for i in range(4)]
        if index in indices:
            match = indices.index(index)
            return DIRECTIION_MAP[match]

    def draw(self):
        sprite_pos = Point(self.start_sprite.x, self.start_sprite.y)
        for i, direction in enumerate(DIRECTIION_MAP):
            if self.direction == direction:
                sprite_pos.y += i
                break
        pyxel.blt(
            self.cell.position.x * 8, self.cell.position.y * 8,
            0, sprite_pos.x * 8, sprite_pos.y * 8,
            8, 8, 12
        )


class BaBaTile(DirectionalTile):
    logic = BabaLogic
    start_sprite = Point(1, 2)


class KeKeTile(DirectionalTile):
    logic = KekeLogic
    start_sprite = Point(5, 2)


class FlagTile(Tile):
    logic = FlagLogic
    sprite_pos = Point(2, 2)


class WallTile(Tile):
    logic = WallLogic
    sprite_pos = Point(3, 2)


class LavaTile(Tile):
    logic = LavaLogic
    sprite_pos = Point(2, 4)


class BrickTile(Tile):
    logic = BrickLogic
    sprite_pos = Point(2, 11)


class IceTile(Tile):
    logic = IceLogic
    sprite_pos = Point(2, 10)


class RockTile(Tile):
    logic = RockLogic
    sprite_pos = Point(4, 2)


class GrassTile(Tile):
    logic = GrassLogic
    sprite_pos = Point(2, 3)


class TileTile(Tile):
    logic = TileLogic
    sprite_pos = Point(3, 3)


class WaterTile(Tile):
    logic = WaterLogic
    sprite_pos = Point(4, 3)


class DoorTile(Tile):
    logic = DoorLogic
    sprite_pos = Point(3, 4)


class PillarTile(Tile):
    logic = PillarLogic
    sprite_pos = Point(4, 4)


class BoxTile(Tile):
    logic = BoxLogic
    sprite_pos = Point(4, 5)


class TextTile(Tile):
    logic = TextLogic


class PropertyTile(TextTile):
    pass

    def __str__(self) -> str:
        return 'property'


class YouTextTile(PropertyTile):
    sprite_pos = Point(1, 1)


class WinTextTile(PropertyTile):
    sprite_pos = Point(2, 1)


class StopTextTile(PropertyTile):
    sprite_pos = Point(3, 1)


class PushTextTile(PropertyTile):
    sprite_pos = Point(4, 1)


class MoveTextTile(PropertyTile):
    sprite_pos = Point(5, 1)


class P1TextTile(PropertyTile):
    sprite_pos = Point(6, 1)


class P2TextTile(PropertyTile):
    sprite_pos = Point(7, 1)


class PullTextTile(PropertyTile):
    sprite_pos = Point(1, 7)


class ShiftTextTile(PropertyTile):
    sprite_pos = Point(2, 7)


class DeadTextTile(PropertyTile):
    sprite_pos = Point(3, 7)


class SinkTextTile(PropertyTile):
    sprite_pos = Point(4, 7)


class JumpTextTile(PropertyTile):
    sprite_pos = Point(5, 7)


class OperatorTile(TextTile):
    pass


class OnTile(OperatorTile):
    sprite_pos = Point(0, 0)

    def __str__(self) -> str:
        return 'on'


class IsTile(OperatorTile):
    sprite_pos = Point(0, 1)

    def __str__(self) -> str:
        return 'is'


class HasTile(OperatorTile):
    sprite_pos = Point(0, 2)

    def __str__(self) -> str:
        return 'has'


class NotTile(OperatorTile):
    sprite_pos = Point(0, 3)

    def __str__(self) -> str:
        return 'not'


class MakeTile(OperatorTile):
    sprite_pos = Point(0, 4)

    def __str__(self) -> str:
        return 'make'


class AndTile(OperatorTile):
    sprite_pos = Point(0, 5)

    def __str__(self) -> str:
        return 'and'


class NounTile(TextTile):
    def __str__(self) -> str:
        return 'noun'
    pass


class BaBaTextTile(NounTile):
    sprite_pos = Point(1, 0)


class FlagTextTile(NounTile):
    sprite_pos = Point(2, 0)


class WallTextTile(NounTile):
    sprite_pos = Point(3, 0)


class IceTextTile(NounTile):
    sprite_pos = Point(1, 8)


class RockTextTile(NounTile):
    sprite_pos = Point(4, 0)


class KekeTextTile(NounTile):
    sprite_pos = Point(5, 0)


class BoxTextTile(NounTile):
    sprite_pos = Point(1, 6)


class PillarTextTile(NounTile):
    sprite_pos = Point(2, 6)


class DoorTextTile(NounTile):
    sprite_pos = Point(3, 6)


class GrassTextTile(NounTile):
    sprite_pos = Point(4, 6)


class TileTextTile(NounTile):
    sprite_pos = Point(5, 6)


class WaterTextTile(NounTile):
    sprite_pos = Point(6, 6)


class LavaTextTile(NounTile):
    sprite_pos = Point(7, 6)


ALL_TILE_CLASSES = get_all_lowest_level_subclasses(Tile)
ALL_TEXT_TILE_CLASSES = get_all_lowest_level_subclasses(TextTile)
ALL_NOUN_TILE_CLASSES = get_all_lowest_level_subclasses(NounTile)
ALL_PROPERTY_TILE_CLASSES = get_all_lowest_level_subclasses(PropertyTile)


def tile_for_index(cell: Cell, index: int) -> Tile:
    for tile_class in ALL_TILE_CLASSES:
        try:
            optional_direction = tile_class(None).is_index(index)
        except Exception as error:
            import pdb; pdb.set_trace()
        if optional_direction:
            return tile_class(cell, optional_direction)
