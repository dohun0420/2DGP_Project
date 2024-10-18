from pico2d import load_image


class Map:
    def __init__(self):
        self.image = load_image('map.png')

    def draw(self):
        self.image.draw(500, 300, 1000, 600)

    def update(self):
        pass
