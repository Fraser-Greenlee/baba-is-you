import pyxel

from baba.framework import Page
from baba.control import get_input, X
from baba.pages import Menu


class Credits(Page):
    def update(self):
        inp = get_input()

        if inp == X:
            self.open(Menu.__class__)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 10, "Made by FraserGreenlee", 1)
        pyxel.text(0, 20, "Using Pyxel", 1)
        pyxel.text(0, 30, "Heavily inspired by BABA IS YOU", 1)
