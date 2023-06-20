import pyxel

from baba.framework import Page


BOARD_SIZE = 16


class App:
    title: str = "BABA IS YOU"
    pages = {pg.__name__: pg for pg in Page.__subclasses__}
    BOARD_SIZE = 16
    current_page = None

    def __init__(self, start_page="Menu") -> None:
        pyxel.init(self.BOARD_SIZE*9, self.BOARD_SIZE*9, display_scale=5, title=self.title)
        pyxel.load('../my_resource.pyxres')
        self.open(start_page)
        pyxel.run(self.update, self.draw)

    def open(self, name: str):
        self.current_page = self.pages[name]()

    def update(self):
        self.current_page.update()

    def draw(self):
        self.current_page.draw()
