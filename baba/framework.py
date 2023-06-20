
class Page:
    name: str  # Overwrite this

    def update(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()
