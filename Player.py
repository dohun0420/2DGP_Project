from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_d, SDLK_a, SDLK_w, SDLK_s, SDL_KEYUP
from state_machine import StateMachine


class Idle:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.action = 2
            player.face_dir = -2
        elif right_down(e) or left_up(e):
            player.action = 1
            player.face_dir = -1
        elif left_down(e) or right_up(e):
            player.action = 0
            player.face_dir = -1
        elif up_down(e) or down_up(e):
            player.action = 2
            player.face_dir = -2
        elif down_down(e) or up_up(e):
            player.action = -2
            player.face_dir = 2


    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.dig()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 33, 130, 33, 56, player.x, player.y, 90, 80)

def start_event(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class Move:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.dir, player.action = 1, -1
        elif left_down(e) or right_up(e):
            player.dir, player.action = -1, 0
        elif up_down(e) or down_up(e):
            player.dir, player.action = 2, 1
        elif down_down(e) or up_up(e):
            player.dir, player.action = -2, 2

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.dig()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 3
        player.x += player.dir * 5

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 33, 130, 33, 56, player.x, player.y, 90, 80)


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Player.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Move, left_down: Move, up_down: Move, down_down: Move, right_up: Move, left_up: Move, up_up: Move, down_up: Move, space_down: Idle},
                Move: {right_down: Idle, left_down: Idle, up_down: Idle, down_down: Idle, right_up: Idle, left_up: Idle, up_up: Idle, down_up: Idle, space_down : Move}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        #if self.state == 's':
            #self.image.clip_draw(self.frame * 33, 130, 33, 56, self.x, self.y, 90, 80)
        #elif self.state == 'w':
            #self.image.clip_draw(self.frame * 33, 86, 33, 46, self.x, self.y, 90, 90)
        #elif self.state == 'd':
        #    self.image.clip_draw(self.frame * 33, 45, 33, 48, self.x, self.y, 90, 100)
        #elif self.state == 'a':
        #    self.image.clip_draw(self.frame * 33, 0, 33, 57, self.x, self.y, 90, 100)
        pass
    def dig(self):
        pass