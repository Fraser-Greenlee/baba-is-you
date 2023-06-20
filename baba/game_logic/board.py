from typing import List

import pyxel

from baba.app import BOARD_SIZE
from baba.game_logic import Tile


TILEMAP = pyxel.tilemap(0)


def load_grid(level: int) -> List[List[Tile]]:
    grid = []
    start = level * BOARD_SIZE
    for y in range(BOARD_SIZE):
        grid.append([])
        for x in range(start, start + BOARD_SIZE):
            sprite_index = TILEMAP.pget(x, y)
            grid[-1].append(SPRITE_NAMES[sprite_index])



class Board:
    def __init__(self, level: int) -> None:
        self.level = level
        self.grid: List[List[Tile]] = load_grid(level)
