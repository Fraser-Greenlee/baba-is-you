import pyxel
import copy
import random
from utils import find_subclasses
from tiles import (
    AndTile, Direction, DirectionToXY, HasNoun, HasTile, IsNoun, IsProperty, IsTile, Logic, MakeTile, OnTile, TextTile, PropertyTile, NounTile
)

LEVEL_SIZE = (8, 8)

MOVE_ATTEMPTS = 10
# Basic parse tree but should work well enough
L0_PARSE_PATHS = {
    NounTile: {
        IsTile: {
            NounTile: IsNoun,
            PropertyTile: {
                None: IsProperty,
                AndTile: {
                    PropertyTile: {
                        None: IsProperty,
                        AndTile: {PropertyTile: IsProperty},
                    },
                }
            }
        },
        HasTile: {NounTile: HasNoun},
        MakeTile: {NounTile: HasNoun},
    }
}
L1_PARSE_PATHS = {
    OnTile: {NounTile: L0_PARSE_PATHS},
    **L0_PARSE_PATHS
}
PARSE_PATHS = {
    NounTile: {
        AndTile: {
            L1_PARSE_PATHS
        },
        **L1_PARSE_PATHS
    }
}


class Cell:
    def __init__(self, grid):
        self.grid = grid
        self.tiles = []

    def check_overlaps():
        pass

    def add(self, tile):
        self.tiles.append(tile)

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

    def add_tile(self, x, y, tile):
        self.grid[y][x].add(tile)

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

    def get_grid_positions(self, start_x, start_y, direction, amount):
        dir_x, dir_y = DirectionToXY[direction]
        if dir_x:
            steps = list(range(start_x, start_x + amount))
            positions = []
            for step in steps:
                positions.append(step, start_y)
            return positions
        elif dir_y:
            steps = list(range(start_y, start_y + amount))
            positions = []
            for step in steps:
                positions.append(start_x, step)
            return positions
        return []

    def move_a_tile(self, tile, direction, amount):
        start_x, start_y = tile.get_coords()
        for i, x, y in enumerate(self.get_grid_positions(start_x, start_y, direction, amount)):
            cell = self.grid[y][x]
            for cell_tile in cell.tiles:
                if cell_tile.no_overlap and not cell_tile.push(direction):
                    # hit a blocked/STOP tile
                    return False
            # actually move the tile
            tile.cell.remove(tile)
            cell.add(tile)
            cell.check_overlaps()

    def move_tiles(self):
        move_direction = self.get_move()
        if move_direction:
            # run multiple random move attempts until all work
            move_counts = []
            possible_grids = []
            for _ in range(MOVE_ATTEMPTS):
                grid_copy = Grid()
                grid_copy.grid = copy.deepcopy(self.grid)
                movers = grid_copy.get_player_tiles()
                random.shuffle(movers)
                mv_count = 0
                for mv in movers:
                    mv_count += int(
                        grid_copy.move_a_tile(
                            mv, *mv.logic.on_move(move_direction, 1)
                        )
                    )
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

    @staticmethod
    def is_valid_command(command):
        pass

    @staticmethod
    def could_be_valid(command):
        pass

    def get_valid_text_commands(self, text_groups):
        all_commands = []
        for text_tiles in text_groups:
            last_valid = []
            current_command = []
            for tile in text_tiles:
                new_command = current_command + [tile]
                if self.is_valid_command(new_command):
                    last_valid = new_command
                    current_command = new_command
                elif self.could_be_valid(new_command):
                    current_command = new_command
                else:
                    current_command = []
                    if last_valid:
                        all_commands.append(last_valid)
        return all_commands

    def _col_text_summary(self, num):
        return self._get_text_tiles(
            self.get_valid_text_commands([self.grid[i][num] for i in range(len(self.grid))])
        )

    def _row_text_summary(self, num):
        return self._get_text_tiles(
            self.get_valid_text_commands(self.grid[num])
        )

    def execute_commands(commands):
        # TODO apply Exec classes to relevent Logic subclasses
        pass

    def update_rules(self):
        self._clear_rules()
        valid_text_commands = []
        for row_num in range(len(self.grid)):
            valid_text_commands += self._row_text_summary(row_num)
        for col_num in range(len(self.grid[0])):
            valid_text_commands += self._col_text_summary(col_num)
        self.execute_commands(valid_text_commands)

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
        # TODO find out how to load a level from that sprite screen
        import pdb; pdb.set_trace()
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(12)
        self.grid.draw()
        self.grid.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)


App()
