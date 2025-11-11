from pico2d import *
import game_framework
from state_machine import StateMachine

FRAMES_PER_ACTION = 10
ACTION_PER_TIME = 1


animation_names = ['Dash To Idle', 'Dash', 'DownSlash', 'DownSlashEffect', 'Fall','Idle Hurt', 'Idle', 'Slash', 'SlashAlt','SlashEffect','SlashEffectAlt','UpSlash','UpSlashEffect','Walk']
animation_frames = [3,11,14,5,5,11,8,14,14,5,5,14,5,6]

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c
def alt_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LALT
time_out = lambda e: e[0] == 'TIMEOUT'
class Idle:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Idle')]
        self.knight.state = 'Idle'
    def exit(self,event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Idle'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class Walk:
    def __init__(self, knight):
        self.knight = knight
        self.alt_state = 0
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Walk')]
        self.knight.state = 'Walk'

    def exit(self,event):
        pass
    def do(self):
        if self.alt_state == 0 : self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)

    def draw(self):
        self.knight.image['Walk'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class Attack:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Slash')]
        self.knight.state = 'Slash'
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Slash'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class Dash:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Dash')]
        self.knight.state = 'Dash'
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Dash'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class jump:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Fall')]
        self.knight.state = 'Fall'
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Fall'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class AltAttack:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('SlashAlt')]
        self.knight.state = 'SlashAlt'
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Slash'][int(self.knight.frame)].draw(self.knight.x, self.knight.y)

class Knight:
    image = None
    def __init__(self):
        self.load_sprite()
        self.x, self.y = 400, 300
        self.state = 'Idle'
        self.frame = 0
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.DASH = Dash(self)
        self.JUMP = jump(self)
        self.ALTATTACK = AltAttack(self)  # Placeholder for Alt Attack state
        self.StateMachine = StateMachine(
            self.IDLE,
    {
                self.IDLE : {x_down: self.ATTACK, right_down: self.WALK, left_down: self.WALK, c_down : self.DASH, alt_down : self.JUMP},
                self.ATTACK : {x_down : self.ALTATTACK, time_out : self.IDLE},
                self.WALK : {x_down: self.ATTACK, time_out : self.IDLE, c_down : self.DASH, alt_down : self.JUMP},
                self.DASH : {time_out: self.IDLE},
                self.JUMP : {time_out: self.IDLE},
                self.ALTATTACK : {time_out: self.IDLE, x_down : self.ATTACK},

    }
        )



    def load_sprite(self):
        if Knight.image is None:
            Knight.image = {}
            for name, frames in zip(animation_names, animation_frames):
                clean_name = name.strip()
                Knight.image[clean_name] = []
                for i in range(frames+1):
                    filename = f"./knight_sprite/{clean_name}_{i:03d}.png"
                    try:
                        img = load_image(filename)
                    except Exception:
                        print(f"Missing file: `{filename}`")
                        img = None
                    Knight.image[clean_name].append(img)
    def draw(self):
        #self.image[self.state][int(self.frame)].draw(self.x, self.y)
        self.StateMachine.draw()
    def update(self):
        #frames = animation_frames[animation_names.index(self.state)]
        #self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % frames
        self.StateMachine.update()

    def handle_event(self, event):
        self.StateMachine.handle_state_event(('INPUT', event))



