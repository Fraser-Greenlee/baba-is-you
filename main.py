import pyxel
from tiles import (
    EmptyTile
)

LEVEL_SIZE = (8, 8)


class Cell:
    def __init__(self, grid):
        self.grid = grid
        self.tiles = []


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

    def draw(self):
        for tile in self.tiles:
            tile.draw()


class App:
    def __init__(self):
        pyxel.init(8*LEVEL_SIZE[0], 8*LEVEL_SIZE[1])
        self.grid = Grid(*LEVEL_SIZE)
        # TODO load level

        #
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)


App()
