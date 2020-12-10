import pyxel
import copy
import random
from utils import find_subclasses
from tiles import (
    Direction, IsTile, Logic, OnTile, TextTile, PropertyTile, OperatorTile, NounTile
)

LEVEL_SIZE = (8, 8)

MOVE_ATTEMPTS = 10
VALID_COMMANDS = [
    [NounTile, (IsTile, HasTile, MakeTile), NounTile],
    [NounTile, IsTile, PropertyTile],
    [NounTile, OnTile, NounTile, IsTile, PropertyTile],
]


class Cell:
    def __init__(self, grid):
        self.grid = grid
        self.tiles = []

    def draw(self, x, y):
        for tile in self.tiles:
            tile.draw(x, y)


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(
                    Cell(self.grid)
                )
            self.grid.append(row)

    @staticmethod
    def get_move():
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            return Direction.W
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            return Direction.E
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            return Direction.N
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
            return Direction.S
        return None

    def move_tiles(self):
        move_direction = self.get_move()
        if move_direction:
            # run multiple random move attempts until all work
            move_counts = []
            possible_grids = []
            for _ in range(MOVE_ATTEMPTS):
                grid_copy = copy.deepcopy(self.grid)
                movers = self.get_player_tiles()
                random.shuffle(movers)
                mv_count = 0
                for mv in movers:
                    mv_count += int(mv.move(move_direction))
                move_counts.append(mv_count)
                possible_grids.append(grid_copy)

            best_move_i = move_counts.index(max(move_counts))
            self.grid = possible_grids[best_move_i]

    def _clear_rules(self):
        for logic_class in find_subclasses(Logic):
            logic_class.rules = []

    def _get_text_tiles(self, cells):
        tiles = []
        for cell in cells:
            for tile in cell.tiles:
                if issubclass(type(tile), TextTile):
                    tiles.append(tile)
                    break
        return tiles

    def _col_summary(self, num):
        return self._get_text_tiles(
            self._grid_summary([self.grid[i][num] for i in range(len(self.grid))])
        )

    def _row_summary(self, num):
        return self._get_text_tiles(
            self._grid_summary(self.grid[num])
        )

    def update_rules(self):
        self._clear_rules()
        for row_num in range(len(self.grid)):
            row_text_tiles = self._row_summary(row_num)
            


    def update(self):
        self.move_tiles()
        self.update_rules()


    def draw(self):
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                cell.draw(x, y)


class App:
    def __init__(self):
        pyxel.init(8*LEVEL_SIZE[0], 8*LEVEL_SIZE[1])
        self.grid = Grid(*LEVEL_SIZE)
        # TODO load level

        #
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(12)
        self.grid.update()
        self.grid.draw()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)


App()
