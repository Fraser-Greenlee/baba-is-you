import pyxel
import copy
import random
from tiles import (
    Direction, Logic, ALL_TEXT_TILE_CLASSES, tile_for_index
)
from utils import Cell, Point, get_all_lowest_level_subclasses
from config import (
    MOVE_ATTEMPTS,
    END_SPRITE_INDEX,
    check_command
)


class Grid:
    @staticmethod
    def get_bounds(tilemap) -> Point:
        max_bounds = Point(0, 0)
        for y in range(10):
            for x in range(max_bounds.x, 10):
                if tilemap.get(x, y) == END_SPRITE_INDEX:
                    if x > max_bounds.x:
                        max_bounds.x = x
                    if y > max_bounds.y:
                        max_bounds.y = y
        assert max_bounds != Point(0, 0), 'No END tile found.'
        return max_bounds

    def __init__(self):
        tilemap = pyxel.tilemap(0)
        max_point = Point(15, 15)
        self.width = max_point.x
        self.height = max_point.y
        self.grid = []
        for y in range(max_point.y):
            row = []
            for x in range(max_point.x):
                cell = Cell(self, x, y)
                sprite_index = tilemap.get(x, y)
                tile = tile_for_index(cell, sprite_index)
                if tile:
                    cell.add(tile)
                row.append(cell)
            self.grid.append(row)
        self.update_rules()

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
        pass

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
                grid_copy = copy.deepcopy(self)
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
        for logic_class in get_all_lowest_level_subclasses(Logic):
            logic_class.rules = []

    def get_valid_text_commands(self, cells):
        all_commands = []
        last_valid = []
        current_command = []
        for cell in cells:
            tile = cell.tiles[0]
            # TODO does this check work?
            if type(tile) not in ALL_TEXT_TILE_CLASSES:
                current_command = []
                if last_valid:
                    all_commands.append(last_valid)
                continue
            new_command = current_command + [tile]
            is_valid, could_be_valid = check_command(new_command)
            if is_valid:
                last_valid = new_command
                current_command = new_command
            elif could_be_valid:
                current_command = new_command
            else:
                current_command = []
                if last_valid:
                    all_commands.append(last_valid)
        return all_commands

    def _col_text_summary(self, num):
        return self.get_valid_text_commands([self.grid[i][num] for i in range(len(self.grid))])

    def _row_text_summary(self, num):
        return self.get_valid_text_commands(self.grid[num])

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
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell.draw()


class App:
    def __init__(self):
        pyxel.init(8*15, 8*15, caption="BABA IS YOU")
        pyxel.load('my_resource.pyxres')
        self.grid = Grid()
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(12)
        self.grid.update()

    def draw(self):
        pyxel.cls(0)
        self.grid.draw()


App()
