from collections import defaultdict
import pyxel


BOARD_SHAPE = (8, 8)
SPRITE_NAMES = {
    (16, 0): 'baba',
    (17, 0): 'flag',
    (18, 0): 'wall',
    (19, 0): 'rock',

    (24, 0): 'is',

    (8, 0): '_you',
    (9, 0): '_win',
    (10, 0): '_stop',
    (11, 0): '_push',

    (0, 11): 'BaBa',
    (0, 12): 'BaBa',
    (0, 13): 'BaBa',
    (0, 14): 'BaBa',
    (4, 0): 'Wall',
    (5, 0): 'Rock',
}
SPRITE_NAMES = defaultdict(lambda: '.', SPRITE_NAMES)
SPRITE_POS = {v: k for k, v in SPRITE_NAMES.items()}


class Board:
    def __init__(self):
        tilemap = pyxel.tilemap(0)
        self.grid = []
        for y in range(BOARD_SHAPE[1]):
            self.grid.append([])
            for x in range(BOARD_SHAPE[0]):
                sprite_index = tilemap.pget(x, y)
                self.grid[-1].append(SPRITE_NAMES[sprite_index])


    def draw(self):
        for _y, row in enumerate(self.grid):
            for _x, tilename in enumerate(row):
                x, y = _x*9, _y*9

                if tilename == '.':
                    continue
                u, v = SPRITE_POS[tilename]

                if tilename[0] == '_':
                    corner = pyxel.image(0).pget(u*8,v*8)
                    pyxel.rect(x, y+8, 9, 1, corner)
                    pyxel.rect(x+8, y, 1, 9, corner)

                pyxel.blt(x, y, 0, u*8, v*8, 8, 8)


class App:
    def __init__(self):
        pyxel.init(8*15, 8*15, title="BABA IS YOU")
        pyxel.load('../my_resource.pyxres')
        self.board = Board()
        pyxel.run(self.update, self.draw)

    def update(self):
        pyxel.cls(12)

    def draw(self):
        pyxel.cls(0)
        self.board.draw()



if __name__ == '__main__':
    app = App()
