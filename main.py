import pyxel

LEVEL_SIZE = (8, 8)


class Cell:
    def __init__(self, grid):
        self.grid = grid

    def update():
        raise NotImplementedError()

    def draw():
        raise NotImplementedError()


class Empty(Cell):
    def update():
        pass

    def draw():
        pass


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Empty(self.grid))
            self.cells.append(row)


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
