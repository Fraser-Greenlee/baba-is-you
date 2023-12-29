from collections import defaultdict
from copy import deepcopy

import pyxel

from baba.rules import (
    rulefinder,
    ruleparser,
)
from baba.utils import (
    PROPERTIES, Entity, rotate_180, rotate_p90, rotate_m90,
    isentity, istext, isempty, empty_NM,
    flatten,
)

BOARD_SIZE = 8
PIXELS_PER_CELL = 9
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


class Board:
    def __init__(self, level):
        tilemap = pyxel.tilemap(0)
        self.grid = []
        map_start = level * BOARD_SIZE
        for y in range(BOARD_SIZE):
            self.grid.append([])
            for x in range(map_start, map_start + BOARD_SIZE):
                sprite_index = tilemap.pget(x, y)
                self.grid[-1].append(SPRITE_NAMES[sprite_index])

    @staticmethod
    def swap(grid, swaps):
        """Apply all the swaps to the grid"""

        stationary = (a for a, b in swaps if a == b)
        swaps = ((a, b) for a, b in swaps if a != b and a not in stationary)

        new_grid = deepcopy(grid)
        for a, b in swaps:
            for j, row in enumerate(grid):
                for k, cell in enumerate(row):
                    if isentity(cell):
                        # If the rule applies to the cell, and no other rule has been applied yet
                        if cell.lower() == a and new_grid[j][k] == cell:
                            if b == 'empty':
                                new_grid[j][k] = '.'
                            else:
                                new_grid[j][k] = Entity(b.capitalize())

        return new_grid

    def attempt_to_move(self, pile, behaviours):
        """Attempt to move a pile of cells in accordance with their behaviour"""

        if len(pile) == 0:  # Empty pile
            raise UnableToMove

        if isempty(pile[0]):  # Trivial pile
            return pile
        elif len(pile) == 1:  # One-element pile
            raise UnableToMove

        def _is(cell, property):
            if istext(cell):
                cell = "text"
            elif cell == '.':
                cell = 'empty'
            return behaviours[cell.lower()][property]
        ispush = lambda cell: _is(cell, "push")
        issink = lambda cell: _is(cell, "sink")
        ishot = lambda cell: _is(cell, "hot")
        ismelt = lambda cell: _is(cell, "melt")

        # Larger pile
        def could_move():
            return (
                isempty(pile[1])
            ) or (
                ispush(pile[1])
            ) or (
                issink(pile[0])
            ) or (
                issink(pile[1])
            ) or (
                ishot(pile[0]) and ismelt(pile[1])
            ) or (
                ismelt(pile[0]) and ishot(pile[1])
            )

        if not could_move():
            raise UnableToMove

        if issink(pile[0]) or issink(pile[1]):
            return ('.', '.', *pile[2:])

        if ishot(pile[1]) and ismelt(pile[0]):
            return ('.', pile[1], *pile[2:])
        if ismelt(pile[1]) and ishot(pile[0]):
            return ('.', pile[0], *pile[2:])

        if isempty(pile[1]):
            return ('.', pile[0], *pile[2:])

        budged = self.attempt_to_move(pile[1:], behaviours)
        return (budged[0], pile[0], *budged[1:])

    def runstep(self, step, behaviours):
        """Advance grid a single step, given the step and the current behaviours"""
        grid = rots[step](self.grid)
        N, M = len(grid), len(grid[0])
        new_grid = empty_NM(N, M)

        isyou = lambda cell: isentity(cell) and behaviours[cell.lower()]["you"]
        iswin = lambda cell: isentity(cell) and behaviours[cell.lower()]["win"]

        for j, row in enumerate(grid):
            for k, cell in enumerate(row):
                if isempty(cell):
                    continue  # Already empty

                if not isyou(cell):
                    new_grid[j][k] = cell
                    continue

                cell.dir = step

                # Attempt to move
                pile = [cell] + [new_grid[l][k] for l in reversed(range(j))]
                try:
                    shifted_pile = self.attempt_to_move(pile, behaviours)
                    for l, elem in enumerate(reversed(shifted_pile)):
                        new_grid[l][k] = elem

                except UnableToMove:
                    if len(pile) > 1 and iswin(pile[1]):
                        raise YouWin(
                            f"You are '{cell}' and you've walked onto a '{pile[0]}'"
                            " which is 'win'. Hooray! :D "
                        )
                    new_grid[j][k] = cell

        new_grid = crots[step](new_grid)
        return new_grid

    def update(self, step=None):
        rules = rulefinder(self.grid)
        behaviours, swaps = ruleparser(rules)

        # Check for you is win condition
        for noun in behaviours:
            if behaviours[noun]["you"] and behaviours[noun]["win"]:
                raise YouWin(f"You are '{noun}' and you are 'win'. Hooray! :D")

            if behaviours[noun]["hot"] and behaviours[noun]["melt"]:
                swaps.append((noun, 'empty'))

        # Do the swap
        self.grid = self.swap(self.grid, swaps)

        entities_present = {j.lower() for j in flatten(self.grid) if isentity(j)}
        if not any(behaviours[e]["you"] for e in entities_present):
            raise YouLose("Nothing is 'you'. Game over.")

        # Timestep the grid
        if step:
            self.grid = self.runstep(step, behaviours)

    def draw(self):
        for _y, row in enumerate(self.grid):
            for _x, tilename in enumerate(row):
                x, y = _x * PIXELS_PER_CELL, _y * PIXELS_PER_CELL

                if tilename == '.':
                    continue
                u, v = SPRITE_POS[tilename]

                if tilename in PROPERTIES:
                    # pad property tiles with top left corner color
                    corner = pyxel.image(0).pget(u*8, v*8)
                    pyxel.rect(x, y + PIXELS_PER_CELL - 1, PIXELS_PER_CELL, 1, corner)
                    pyxel.rect(x + PIXELS_PER_CELL - 1, y, 1, PIXELS_PER_CELL, corner)

                if tilename == 'Baba':
                    v += '>V^<'.index(tilename.dir)

                pyxel.blt(x, y, 0, u*8, v*8, 8, 8)


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
