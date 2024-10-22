from pico2d import *

from Dig_ani import Dig_ani
from Gold import Gold
from Map import Map
from Player import Player
from Store import Store
from UI import UI
import time

class Happy:
    def __init__(self, x, y):
        self.image = load_image('Happy.png')
        self.x, self.y = x, y
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 500 , 0, 500, 500, self.x, self.y, 25, 25)

    def update(self):
        pass

class Sad:
    def __init__(self, x, y):
        self.image = load_image('Sad.png')
        self.x, self.y = x, y
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 225 , 0, 225, 225, self.x, self.y, 25, 25)

    def update(self):
        pass


def handle_events():
    global running
    global player
    global store_mode
    global space_pressed_time
    global space_mode

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_p:
                store_mode = not store_mode
            elif event.key == SDLK_SPACE and not space_mode:
                space_pressed_time = time.time()
                space_mode = True
                start_dig_animation(player.x, player.y + 40)
        if not store_mode and not space_mode:
            player.handle_event(event)

def start_dig_animation(x, y):
    global dig_ani
    dig_ani = Dig_ani(x, y)

def reset_world():
    global running
    global map
    global world
    global player
    global ui
    global gold
    global store
    global store_mode
    global space_mode
    global space_pressed_time
    global dig_ani

    running = True
    store_mode = False
    space_mode = False
    space_pressed_time = 0
    world = []

    map = Map()
    world.append(map)

    player = Player()
    world.append(player)

    ui = UI()
    world.append(ui)

    gold = Gold()
    world.append(gold)

    store = Store()

    dig_ani = None

def update_world():
    global space_mode
    global space_pressed_time

    if space_mode:
        if time.time() - space_pressed_time >= 5:
            gold.increase()
            space_mode = False
        else:
            if dig_ani:
                dig_ani.update()

    if not space_mode:
        for o in world:
            o.update()

def render_world():
    clear_canvas()
    if store_mode:
        store.draw()
    else:
        for o in world:
            o.draw()
        if space_mode and dig_ani:
            dig_ani.draw()
    update_canvas()

open_canvas(1000, 600)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
