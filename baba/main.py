from collections import defaultdict

import pyxel

from baba.utils.const import Entity, rotate_180, rotate_p90, rotate_m90


SPRITE_NAMES = {
    (16, 0): 'baba',
    (17, 0): 'flag',
    (18, 0): 'wall',
    (19, 0): 'rock',
    (17, 1): 'grass',
    (20, 3): 'skull',
    (20, 2): 'key',
    (16, 2): 'lava',
    (19, 1): 'water',

    (24, 0): 'is',

    (8, 0): 'you',
    (11, 0): 'push',
    (9, 0): 'win',
    (10, 0): 'hot',
    (12, 0): 'melt',
    (11, 1): 'sink',

    (0, 11): Entity('Baba'),
    (3, 0): Entity('Flag'),
    (4, 0): Entity('Wall'),
    (5, 0): Entity('Rock'),
    (0, 4): Entity('Grass'),
    (4, 4): Entity('Skull'),
    (7, 4): Entity('Key'),
    (5, 4): Entity('Water'),
    (2, 4): Entity('Lava'),
}
SPRITE_NAMES = defaultdict(lambda: '.', SPRITE_NAMES)
SPRITE_POS = {v: k for k, v in SPRITE_NAMES.items()}

STEPS = ("^", "V", "<", ">")

# Rotations and counter rotations which need to be applied to the grid such that the move direction is up
rotate_0 = lambda x: x
# Null rotation
rots = (rotate_0, rotate_180, rotate_p90, rotate_m90)
rots = dict(zip(STEPS, rots))
crots = (rotate_0, rotate_180, rotate_m90, rotate_p90)
crots = dict(zip(STEPS, crots))


class GameEnd(Exception):
    pass


class UnableToMove(Exception):
    pass


class YouWin(GameEnd):
    pass


class YouLose(GameEnd):
    pass


class App:
    def __init__(self):
        pyxel.init(BOARD_SIZE * PIXELS_PER_CELL, BOARD_SIZE * PIXELS_PER_CELL, display_scale=5, title="BABA BOARD GAME")
        pyxel.load('../my_resource.pyxres')
        self.level = -1
        self.stop_banner = None
        self.next_level()
        pyxel.run(self.update, self.draw)

    def next_level(self):
        self.level += 1
        self.stop_banner = None
        if self.level > 2:
            self.stop_banner = self.show_end

        self.board = Board(self.level)
        if self.stop_banner is None:
            self.board.update()
        self.last_input = None
        self.all_steps = ''

    def undo(self):
        self.stop_banner = None
        self.board = Board(self.level)
        self.all_steps = self.all_steps[:-1]
        for step in self.all_steps:
            self.board.update(step)
            self.board.update()

    @staticmethod
    def show_win():
        pyxel.rect((BOARD_SIZE/2-2)*8, BOARD_SIZE/2*8-4, 4*8-1+16, 5+8, 3)
        pyxel.text((BOARD_SIZE/2-1)*8, BOARD_SIZE/2*8, 'YOU WIN', 10)

    @staticmethod
    def show_lose():
        pyxel.rect((BOARD_SIZE/2-2)*8, BOARD_SIZE/2*8-4, 4*8-1+16, 5+8, 1)
        pyxel.text((BOARD_SIZE/2-1)*8, BOARD_SIZE/2*8, 'YOU LOSE', 7)

    @staticmethod
    def show_end():
        pyxel.rect((BOARD_SIZE/2-2)*8, BOARD_SIZE/2*8-4, 4*8-1+16, 5+8, 3)
        pyxel.text((BOARD_SIZE/2-1)*8, BOARD_SIZE/2*8, 'THE END', 10)

    def update(self):
        inp = None
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            inp = '<'
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            inp = '>'
        elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            inp = '^'
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            inp = 'V'
        elif pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            inp = 'X'
        else:
            self.last_input = None

        if inp == self.last_input:
            inp = None

        if inp:
            if (self.stop_banner is None or self.stop_banner in [self.show_lose, self.show_win]) and inp == 'X':
                self.undo()

            elif self.stop_banner is None and inp in '<>^V':
                try:
                    self.board.update(inp)
                    self.board.update()
                except YouWin:
                    self.stop_banner = self.show_win
                except YouLose:
                    self.stop_banner = self.show_lose

                self.all_steps += inp

            elif self.stop_banner == self.show_win:
                self.next_level()

            self.last_input = inp

    def draw(self):
        pyxel.cls(0)
        self.board.draw()
        if self.stop_banner is not None:
            self.stop_banner()
