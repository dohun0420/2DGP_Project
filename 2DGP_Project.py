from pico2d import *

# Game object class here

class Map:
    def __init__(self):
        self.image = load_image('map.png')

    def draw(self):
        self.image.draw(400, 300, 800, 600)

    def update(self):
        pass


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
            self.image.clip_draw(self.frame * 33, 130, 33, 56, self.x, self.y, 100, 100)
        elif self.state == 'w':
            self.image.clip_draw(self.frame * 33, 86, 33, 46, self.x, self.y, 100, 100)
        elif self.state == 'd':
            self.image.clip_draw(self.frame * 33, 45, 33, 48, self.x, self.y, 100, 100)
        elif self.state == 'a':
            self.image.clip_draw(self.frame * 33, 0, 33, 57, self.x, self.y, 100, 100)

def handle_events():
    global running
    global player

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
        player.handle_event(event)


def reset_world():
    global running
    global map
    global world
    global player

    running = True
    world = []

    map = Map()
    world.append(map)

    player = Player()
    world.append(player)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(800, 600)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
