from pico2d import *
from Map import Map
from Player import Player
from UI import UI

class Store:
    def __init__(self):
        self.image = load_image('store_test.png')

    def draw(self):
        self.image.draw(500, 300, 1000, 600)

    def update(self):
        pass


def handle_events():
    global running
    global player
    global store_mode

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_p:  # Press 'p' to toggle store
                store_mode = not store_mode
        if not store_mode:
            player.handle_event(event)


def reset_world():
    global running
    global map
    global world
    global player
    global ui
    global store
    global store_mode

    running = True
    store_mode = False
    world = []

    map = Map()
    world.append(map)

    player = Player()
    world.append(player)

    ui = UI()
    world.append(ui)

    store = Store()

def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    if store_mode:
        store.draw()
    else:

        for o in world:
            o.draw()
    update_canvas()


open_canvas(1000, 600)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
