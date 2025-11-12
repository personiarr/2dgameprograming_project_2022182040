from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine
from types import SimpleNamespace
attacked_sprite = [3,5,4,5,6]
idle_sprite = [0,6]


FRAMES_PER_ACTION = 10
ACTION_PER_TIME = 1
FT = FRAMES_PER_ACTION * ACTION_PER_TIME
def attack(e):
    return e[0] == 'ATTACKED'
def timeout(e):
    return e[0] == 'TIMEOUT'
class idle:
    def __init__(self, dummy):
        self.dummy = dummy

        self.size = 192
    def enter(self, event):
        self.frame = 0
        self.dt = 0
        self.i_w = getattr(self.dummy.image[self.frame], 'w', 0)
        self.i_h = getattr(self.dummy.image[self.frame], 'h', 0)
    def exit(self, event):
        pass
    def do(self):
        self.frame = idle_sprite[int(self.dt)%2]
        self.dt += game_framework.frame_time * FT
        self.i_w = getattr(self.dummy.image[self.frame], 'w', 0)
        self.i_h = getattr(self.dummy.image[self.frame], 'h', 0)
    def draw(self):
        self.dummy.image[int(self.frame)].clip_draw(0,0,self.i_w,self.i_h,self.dummy.x, self.dummy.y, self.size, self.size)

class attacked:
    def __init__(self, dummy):
        self.dummy = dummy

        self.size = 192
    def enter(self, event):
        self.frame = 0
        self.dt = 0
        self.i_w = getattr(self.dummy.image[self.frame], 'w', 0)
        self.i_h = getattr(self.dummy.image[self.frame], 'h', 0)
    def exit(self, event):
        pass
    def do(self):
        self.frame = attacked_sprite[int(self.dt)%5]
        self.dt+= game_framework.frame_time * FT
        self.i_w = getattr(self.dummy.image[self.frame], 'w',0)
        self.i_h = getattr(self.dummy.image[self.frame], 'h', 0)
        if self.dt > 10:
            self.dummy.StateMachine.handle_state_event(('TIMEOUT', None))
    def draw(self):
        self.dummy.image[int(self.frame)].clip_draw(0,0,self.i_w,self.i_h,self.dummy.x, self.dummy.y, self.size, self.size)

class Dummy:
    image = None

    def __init__(self):
        if Dummy.image is None:
            Dummy.image = []
            for i in range(0,7):
                Dummy.image.append(load_image(f'./dummy_sprite/Training Dummy Anim_00{i}.png'))
        self.x, self.y = 800, 150 + 96
        self.IDLE = idle(self)
        self.ATTACKED = attacked(self)
        self.size = 192

        self.state = 'IDLE'
        self.StateMachine = StateMachine(
                                         self.IDLE,
                                         {
         self.IDLE :{attack : self.ATTACKED},
         self.ATTACKED :{timeout : self.IDLE, attack : self.ATTACKED}

        })
    def handle_event(self, event):
        self.StateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - (self.size / 2), self.y - (self.size / 2), self.x + (self.size / 2), self.y + (self.size / 2)

    def handle_collision(self, group, other):
        if group == "attack:dummy":
            self.StateMachine.handle_state_event(('ATTACKED',None ))



    def update(self):
        self.StateMachine.update()

    def draw(self):
        self.StateMachine.draw()