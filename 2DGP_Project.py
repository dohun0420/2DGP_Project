from pico2d import *
from Map import Map
from Player import Player
from Store import Store
from UI import UI
import random
import time

class Dig_ani:
    def __init__(self, x, y):
        self.image = load_image('dig_animation.png')
        self.frame = 0
        self.x, self.y = x, y
        self.frame_time = 0

    def draw(self):
        self.image.clip_draw(self.frame * 25 , 0, 25, 25, self.x, self.y, 25, 25)

    def update(self):
        self.frame_time += 0.01
        if self.frame_time >= 0.1:
            self.frame = (self.frame + 1) % 2
            self.frame_time = 0

class Gold:
    def __init__(self):
        self.image = load_image('Gold.png')
        self.font = load_font('arial.ttf', 24)
        self.count = 0

    def draw(self):
        self.image.draw(160, 543, 100, 70)
        self.font.draw(200, 543, f'X {self.count}', (255, 255, 255))

    def increase(self):
        if random.random() < 0.7:
            self.count += 1

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
            elif event.key == SDLK_p:  # Press 'p' to toggle store
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
        if time.time() - space_pressed_time >= 5:  # 5초 후
            gold.increase()  # 금 1개 증가 (50% 확률)
            space_mode = False  # 타이머 종료
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
