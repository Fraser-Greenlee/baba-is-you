import pyxel
from tiles import (
    Direction
)

LEVEL_SIZE = (8, 8)


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

    def update(self):
        move_direction = self.get_move()
        # run multiple random move attempts until all work

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
        self.grid.draw()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)


App()
