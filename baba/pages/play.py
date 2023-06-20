import pyxel

from baba.framework import Page
from baba.game_logic import Board
from baba.control import get_input, UP, DOWN, LEFT, RIGHT, X, Y


class Play(Page):
    def __init__(self, level: int = 0) -> None:
        self.board = Board(level)

    def update(self):
        inp = get_input()

        if inp == X:
            self.open(self.options[self.cursor])

        if inp == UP:
            self.cursor -= 1
        elif inp == DOWN:
            self.cursor += 1

    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 10, self.title, 1)
        for i, page in enumerate(self.options):
            col = 1 if i != self.cursor else 2
            pyxel.text(0, 10 + i * 10, page.__class__, col)
