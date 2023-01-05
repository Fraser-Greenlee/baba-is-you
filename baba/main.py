from collections import defaultdict
from copy import deepcopy

import pyxel

from baba.rules import (
    rulefinder,
    ruleparser,
)
from baba.utils import (
    rotate_180, rotate_p90, rotate_m90,
    isentity, istext, isempty, empty_NM,
    flatten,
)

BOARD_SHAPE = (8, 8)
SPRITE_NAMES = {
    (16, 0): 'baba',
    (17, 0): 'flag',
    (18, 0): 'wall',
    (19, 0): 'rock',

    (24, 0): 'is',

    (8, 0): 'you',
    (9, 0): 'win',
    (10, 0): 'stop',
    (11, 0): 'push',

    (0, 11): 'Baba',
    (0, 12): 'Baba',
    (0, 13): 'Baba',
    (0, 14): 'Baba',
    (4, 0): 'Wall',
    (5, 0): 'Rock',
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
    def __init__(self):
        tilemap = pyxel.tilemap(0)
        self.grid = []
        for y in range(BOARD_SHAPE[1]):
            self.grid.append([])
            for x in range(BOARD_SHAPE[0]):
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
                        if cell.lower() == a and new_grid[j][k] is cell:
                            new_grid[j][k] = b.upper()

        return new_grid

    def attempt_to_move(self, pile, behaviours):
        """Attempt to move a pile of cells in accordance with their behaviour"""

        if len(pile) == 0:  # Empty pile
            raise UnableToMove

        if isempty(pile[0]):  # Trivial pile
            return pile
        elif len(pile) == 1:  # One-element pile
            raise UnableToMove

        # Larger pile
        pushable = lambda cell: (isentity(cell) and behaviours[cell.lower()]["push"]) or (
            istext(cell) and behaviours["text"]["push"]
        )
        if not pushable(pile[0]):
            raise UnableToMove

        if isempty(pile[1]):
            return (pile[1], pile[0], *pile[2:])
        else:
            budged = self.attempt_to_move(pile[1:], behaviours)
            return (budged[0], pile[0], *budged[1:])

    def runstep(self, step, behaviours):
        """Advance grid a single step, given the step and the current behaviours"""
        self.grid = rots[step](self.grid)
        N, M = len(self.grid), len(self.grid[0])
        new_grid = empty_NM(N, M)

        isyou = lambda cell: isentity(cell) and behaviours[cell.lower()]["you"]
        iswin = lambda cell: isentity(cell) and behaviours[cell.lower()]["win"]

        for j, row in enumerate(self.grid):
            for k, cell in enumerate(row):
                if isempty(cell):
                    continue  # Already empty

                if not isyou(cell):
                    new_grid[j][k] = cell
                    continue

                # Attempt to move
                pile = [new_grid[l][k] for l in reversed(range(j))]
                try:
                    shifted_pile = self.attempt_to_move(pile, behaviours)
                    for l, elem in enumerate(reversed(shifted_pile)):
                        new_grid[l][k] = elem

                    new_grid[j - 1][k] = cell
                except UnableToMove:
                    if len(pile) > 0 and iswin(pile[0]):
                        raise YouWin(
                            f"You are '{cell}' and you've walked onto a '{pile[0]}'"
                            " which is 'win'. Hooray! :D "
                        )
                    new_grid[j][k] = cell

        new_grid = crots[step](new_grid)
        return new_grid

    def update(self, step):
        rules = rulefinder(self.grid)
        behaviours, swaps = ruleparser(rules)

        # Check for you is win condition
        for noun in behaviours:
            if behaviours[noun]["you"] and behaviours[noun]["win"]:
                raise YouWin(f"You are '{noun}' and you are 'win'. Hooray! :D")

        # Do the swap
        self.grid = self.swap(self.grid, swaps)

        entities_present = {j.lower() for j in flatten(self.grid) if isentity(j)}
        if not any(behaviours[e]["you"] for e in entities_present):
            raise YouLose("Nothing is 'you'. Game over.")

        # Timestep the grid
        if step:
            self.runstep(step, behaviours)
        step += 1

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
        step = None
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            step = '<'
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            step = '>'
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            step = '^'
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            step = 'v'

        if step:
            self.board.update(step)

    def draw(self):
        pyxel.cls(0)
        self.board.draw()
