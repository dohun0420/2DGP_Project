from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_d, SDLK_a, SDLK_w, SDLK_s, SDL_KEYUP


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Player.png')
        self.state = 's'

    def update(self):
        if 0 <= self.x + (self.dir_x * 5) <= 800:
            self.x += self.dir_x * 5
        if 0 <= self.y + (self.dir_y * 5) <= 330:
            self.y += self.dir_y * 5

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.dir_x += 1
                self.state = 'd'
            elif event.key == SDLK_a:
                self.dir_x -= 1
                self.state = 'a'
            elif event.key == SDLK_w:
                self.dir_y += 1
                self.state = 'w'
            elif event.key == SDLK_s:
                self.dir_y -= 1
                self.state = 's'
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                self.dir_x -= 1
            elif event.key == SDLK_a:
                self.dir_x += 1
            elif event.key == SDLK_w:
                self.dir_y -= 1
            elif event.key == SDLK_s:
                self.dir_y += 1

        self.frame = (self.frame + 1) % 3

    def draw(self):
        if self.state == 's':
            self.image.clip_draw(self.frame * 33, 130, 33, 56, self.x, self.y, 90, 90)
        elif self.state == 'w':
            self.image.clip_draw(self.frame * 33, 86, 33, 46, self.x, self.y, 90, 90)
        elif self.state == 'd':
            self.image.clip_draw(self.frame * 33, 45, 33, 48, self.x, self.y, 90, 90)
        elif self.state == 'a':
            self.image.clip_draw(self.frame * 33, 0, 33, 57, self.x, self.y, 90, 90)
