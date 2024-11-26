from pico2d import *
import time
from Dig_ani import Dig_ani
from Gold import Gold
from GoldSpot import GoldSpot
from Happy import Happy
from Items import Items
from Map import Map
from Player import Player
from Sad import Sad
from Store import Store
from UI import UI
from Selection import Selection

class Ending():
    def __init__(self):
        self.x, self.y = 500, 300
        self.image = load_image('Ending.png')
        self.font = load_font('arial.ttf', 24)

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 1000, 600)

class Timer():
    def __init__(self):
        self.x, self.y = 900, 560
        self.image = load_image('Timer.png')
        self.font = load_font('arial.ttf', 30)
        self.start_time = get_time()
        self.paused = False
        self.paused_time = 0

    def update(self):
        global store_mode
        if store_mode:
            if not self.paused:
                self.paused = True
                self.paused_time = get_time() - self.start_time
        else:
            if self.paused:
                self.paused = False
                self.start_time = get_time() - self.paused_time

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)
        if not self.paused:
            remaining_time = max(0, 180 - (get_time() - self.start_time))
        else:
            remaining_time = max(0, 180 - self.paused_time)
        self.font.draw(self.x + 25, self.y, f'{remaining_time:.0f}', (255, 255, 255))


def handle_events():
    global running, player, store_mode, space_pressed_time, space_mode, selection, goldspot

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_p:
                store_mode = not store_mode
                if store_mode:
                    for spot in goldspot:
                        world.remove(spot)
                    goldspot = [GoldSpot() for _ in range(10)]
                    world.extend(goldspot)
                else:
                    for spot in goldspot:
                        world.remove(spot)
                    goldspot = [GoldSpot() for _ in range(10)]
                    world.extend(goldspot)
                    if player in world:
                        world.remove(player)
                    world.append(player)
            elif event.key == SDLK_SPACE and not space_mode:
                if store_mode:
                    buy_item()
                else:
                    space_pressed_time = time.time()
                    space_mode = True
                    start_dig_animation(player.x, player.y + 40)
            elif store_mode:
                handle_store_key(event)
        if not store_mode and not space_mode:
            player.handle_event(event)


def handle_store_key(event):
    global gold, items, store_mode, selection

    if event.key == SDLK_w:
        selection.move(0, 190)
    elif event.key == SDLK_s:
        selection.move(0, -190)
    elif event.key == SDLK_a:
        selection.move(-500, 0)
    elif event.key == SDLK_d:
        selection.move(500, 0)
    elif event.key == SDLK_SPACE:
        buy_item()


def buy_item():
    global gold, items, purchased_items, dig_time

    item_prices = [0, 5, 7, 12, 20]

    current_item_price = min([price for i, price in enumerate(item_prices) if purchased_items[i]], default=0)

    if selection.x == 250 and selection.y == 354 and not purchased_items[1]:
        if gold.count >= 5 and 5 > current_item_price:
            gold.count -= 5
            items.set_item(1)
            purchased_items[1] = True
            dig_time = 4
    elif selection.x == 750 and selection.y == 354 and not purchased_items[3]:
        if gold.count >= 12 and 12 > current_item_price:
            gold.count -= 12
            items.set_item(3)
            purchased_items[3] = True
            dig_time = 2
    elif selection.x == 250 and selection.y == 164 and not purchased_items[2]:
        if gold.count >= 7 and 7 > current_item_price:
            gold.count -= 7
            items.set_item(2)
            purchased_items[2] = True
            dig_time = 3
    elif selection.x == 750 and selection.y == 164 and not purchased_items[4]:
        if gold.count >= 20 and 20 > current_item_price:
            gold.count -= 20
            items.set_item(4)
            purchased_items[4] = True
            dig_time = 1


def start_dig_animation(x, y):
    global dig_ani
    dig_ani = Dig_ani(x, y)


def reset_world():
    global running, map, world, player, ui, gold, store, store_mode, space_mode, space_pressed_time
    global dig_ani, happy, sad, result_mode, result_time, selection, items, purchased_items, dig_time, goldspot, timer

    running = True
    store_mode = False
    space_mode = False
    space_pressed_time = 0
    result_mode = False
    result_time = 0
    world = []

    map = Map()
    world.append(map)

    goldspot = [GoldSpot() for _ in range(10)]
    world.extend(goldspot)

    player = Player()
    world.append(player)

    ui = UI()
    world.append(ui)

    gold = Gold()
    world.append(gold)

    store = Store()

    selection = Selection()

    items = Items()
    world.append(items)

    timer = Timer()
    world.append(timer)

    dig_ani = None
    happy = None
    sad = None

    purchased_items = [False] * 5
    dig_time = 5


def update_world():
    global space_mode, space_pressed_time, result_mode, result_time, happy, sad, dig_time, player

    if space_mode and not store_mode:
        if time.time() - space_pressed_time >= dig_time:
            gold_collected = False
            for spot in goldspot[:]:
                distance = ((player.x - spot.x) ** 2 + (player.y - spot.y) ** 2) ** 0.5
                if distance <= 50:
                    gold.increase()
                    happy = Happy(player.x, player.y + 40)
                    goldspot.remove(spot)
                    world.remove(spot)
                    gold_collected = True
                    break

            if not gold_collected:
                sad = Sad(player.x, player.y + 40)

            result_time = time.time()
            result_mode = 'happy' if gold_collected else 'sad'
            space_mode = False

    for o in world:
        o.update()

    if space_mode and dig_ani:
        dig_ani.update()

    if result_mode:
        if time.time() - result_time >= 0.5:
            result_mode = False
            happy = None
            sad = None

    if not goldspot:
        goldspot.extend([GoldSpot() for _ in range(10)])
        world.extend(goldspot)
        if player in world:
            world.remove(player)
        world.append(player)


def render_world():
    clear_canvas()
    if store_mode:
        store.draw()
        gold.draw_count_only()
        selection.draw()
        timer.draw()
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

#버그없음