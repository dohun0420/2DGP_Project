from pico2d import *
import random
import time
from Dig_ani import Dig_ani
from Gold import Gold
from Happy import Happy
from Map import Map
from Player import Player
from Sad import Sad
from Store import Store
from UI import UI
from Selection import Selection


def handle_events():
    global running
    global player
    global store_mode
    global space_pressed_time
    global space_mode
    global selection

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
            elif store_mode:
                if event.key == SDLK_w:
                    selection.move(0, 190)
                elif event.key == SDLK_s:
                    selection.move(0, -190)
                elif event.key == SDLK_a:
                    selection.move(-500, 0)
                elif event.key == SDLK_d:
                    selection.move(500, 0)
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
    global happy
    global sad
    global result_mode
    global result_time
    global selection

    running = True
    store_mode = False
    space_mode = False
    space_pressed_time = 0
    result_mode = False
    result_time = 0
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

    selection = Selection()

    dig_ani = None
    happy = None
    sad = None

def update_world():
    global space_mode
    global space_pressed_time
    global result_mode
    global result_time
    global happy, sad

    if space_mode:
        if time.time() - space_pressed_time >= 5:
            if random.random() < 0.7:
                gold.increase()
                happy = Happy(player.x, player.y + 40)
                result_time = time.time()
                result_mode = 'happy'
            else:
                sad = Sad(player.x, player.y + 40)
                result_time = time.time()
                result_mode = 'sad'
            space_mode = False
        else:
            if dig_ani:
                dig_ani.update()

    if not space_mode:
        for o in world:
            o.update()

    if result_mode:
        if time.time() - result_time >= 0.5:
            result_mode = False
            happy = None
            sad = None

def render_world():
    clear_canvas()
    if store_mode:
        store.draw()
        gold.draw_count_only()
        selection.draw()
    else:
        for o in world:
            o.draw()
        if space_mode and dig_ani:
            dig_ani.draw()
        if result_mode:
            if result_mode == 'happy' and happy:
                happy.draw()
            elif result_mode == 'sad' and sad:
                sad.draw()
    update_canvas()

open_canvas(1000, 600)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
