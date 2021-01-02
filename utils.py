from enum import Enum


Direction = Enum('Directioin', ('W', 'N', 'E', 'S'))


def get_all_lowest_level_subclasses(parent_class, subclasses=None):
    lowest_level_classes = []
    if not subclasses:
        subclasses = parent_class.__subclasses__()
    for clazz in subclasses:
        subclasses = clazz.__subclasses__()
        if subclasses:
            lowest_level_classes += get_all_lowest_level_subclasses(clazz, subclasses=subclasses)
        else:
            lowest_level_classes.append(clazz)
    return lowest_level_classes


class Cell:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.position = Point(x, y)
        self.tiles = []

    def check_overlaps():
        pass

    def add(self, tile):
        self.tiles.append(tile)

    def __repr__(self) -> str:
        return f'Cell<Position: {self.position}, Tiles: {self.tiles}>'

    def draw(self):
        for tile in self.tiles:
            tile.draw()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert(type(other) is Point)
        self.x += other.x
        self.y += other.y
        return self

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __eq__(self, other) -> bool:
        assert(type(other) is Point), "Can only compare against Point's."
        return self.x == other.x and self.y == other.y

    def range(self, direction: Direction, amount: int):
        points = []
        x_mod = 0
        y_mod = 0

        if direction == Direction.W:
            x_mod = -1
        elif direction == Direction.E:
            x_mod = 1
        elif direction == Direction.N:
            y_mod = -1
        elif direction == Direction.S:
            y_mod = 1

        for i in range(1, amount + 1):
            points.append(
                Point(self.x + x_mod * i, self.y + y_mod * i)
            )
        return points

    def sprite_index(self) -> int:
        assert(self.x <= 31)
        assert(self.y <= 31)
        return self.x + 31 * self.y
