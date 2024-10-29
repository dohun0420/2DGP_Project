from pico2d import load_image


class Store:
    def __init__(self):
        self.image = load_image('Store.png')

    def draw(self):
        self.image.draw(500, 300, 1000, 600)

    def update(self):
        pass


class Selection:
    def __init__(self):
        self.image = load_image('Selection.png')

    def draw(self):
        self.image.draw(100, 300)

    def update(self):
        pass