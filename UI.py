from pico2d import load_image


class UI:
    def __init__(self):
        self.image = load_image('UI.png')

    def draw(self):
        self.image.draw(130, 560, 300, 300)

    def update(self):
        pass
