from typing import List
import pyxel

from baba.framework import Page
from baba.pages import Play, Credits
from baba.control import get_input, UP, DOWN, X


class Menu(Page):
    title: str = "BABA IS YOU-demake"
    options: List[Page] = [Play, Credits]
    cursor: int = 0

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
