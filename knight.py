from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine
from types import SimpleNamespace

pressed_keys = set()

FRAMES_PER_ACTION = 10
ACTION_PER_TIME = 1
ATK_FPA = 8
ATK_APT = 2
MPS = 10
PPM = 20
PPS = MPS * PPM
DMPS = MPS * 10
DPPS = DMPS * 10
G = 10
GPPS = G * PPM

animation_names = ['Dash To Idle', 'Dash', 'DownSlash', 'DownSlashEffect', 'Fall','Idle Hurt', 'Idle', 'Slash', 'SlashAlt','SlashEffect','SlashEffectAlt','UpSlash','UpSlashEffect','Walk', 'Land']
animation_frames = [3,11,14,5,5,11,8,14,14,5,5,14,5,6,2]



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
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def atk_timeout(e):
    return e[0] == 'TIMEOUT' and ((SDLK_RIGHT in pressed_keys and not (SDLK_LEFT in pressed_keys)) or (SDLK_LEFT in pressed_keys and not (SDLK_RIGHT in pressed_keys)))


time_out = lambda e: e[0] == 'TIMEOUT'
class Idle:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Idle')]
        self.knight.state = 'Idle'
    def exit(self,event):
        return True
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Idle'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)

class Walk:
    def __init__(self, knight):
        self.knight = knight
        self.alt_state = 0
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Walk')]
        self.knight.state = 'Walk'
        if event[0]!='TIMEOUT' and event[1].type==SDL_KEYDOWN and (event[1].key == SDLK_RIGHT or event[1].key == SDLK_LEFT):
            if event[1].key == SDLK_RIGHT:
                self.knight.dir = 1
                self.knight.move_dir = 1
            elif event[1].key == SDLK_LEFT:
                self.knight.dir = -1
                self.knight.move_dir = -1
        elif event[0]!='TIMEOUT' and event[1].type==SDL_KEYUP and (event[1].key == SDLK_RIGHT or event[1].key == SDLK_LEFT):
            if event[1].key == SDLK_RIGHT:
                self.knight.dir = -1
                self.knight.move_dir = -1
            elif event[1].key == SDLK_LEFT:
                self.knight.dir = 1
                self.knight.move_dir = 1
        elif event[0]=='TIMEOUT':
            if self.knight.move_dir == 1:
                self.knight.dir = 1
            elif self.knight.move_dir == -1:
                self.knight.dir = -1
    def exit(self,event):
        if event[1].type==SDL_KEYUP and (event[1].key==SDLK_LEFT or event[1].key==SDLK_RIGHT):self.knight.move_dir = 0
        return True
    def do(self):
        if self.alt_state == 0 : self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
        #움직임
        self.knight.sx =  PPS * game_framework.frame_time * self.knight.dir
    def draw(self):
        self.knight.image['Walk'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)



class Dash:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Dash')]
        self.knight.state = 'Dash'
        self.done_flag = False
        self.knight.sx = 0
    def exit(self, event):
        self.knight.sx = 0
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 3)
        if self.knight.frame >= 6 :
            self.knight.frame = 0
            self.knight.frames = animation_frames[animation_names.index('Dash To Idle')]
            self.done_flag = True
            #self.knight.state = 'Idle'
        if self.knight.frame >=self.knight.frames+1 and self.done_flag and self.knight.move_dir !=0:
            self.knight.StateMachine.handle_state_event(('TIMEOUT', None))
        if self.knight.frame >= self.knight.frames+1 and self.done_flag:
            self.knight.StateMachine.handle_state_event(('TIMEOUT', None))
        if not self.done_flag : self.knight.sx =  DPPS * game_framework.frame_time * self.knight.dir

    def draw(self):
        if not self.done_flag : self.knight.image['Dash'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)
        else : self.knight.image['Dash To Idle'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)


class jump:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Fall')]
        self.knight.state = 'Fall'
    def exit(self, event):
        return True
    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (self.knight.frames +1)
    def draw(self):
        self.knight.image['Fall'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)


class Attack:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('Slash')]
        self.knight.state = 'Slash'
        self.effect = Effect(self.knight)
        self.alt_flag = False
        self.walk_flag = False
        game_world.add_object(self.effect, 2)
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + ATK_FPA * ATK_APT * game_framework.frame_time)
        if self.knight.frame >= 7 and not self.alt_flag:
            self.knight.StateMachine.handle_state_event(('TIMEOUT', None))
        elif self.knight.frame >= 7 and self.alt_flag:
            self.knight.StateMachine.handle_state_event(('INPUT', SimpleNamespace(type=SDL_KEYDOWN, key=SDLK_x)))
        #공격 딜레이, timeout 발생
    def draw(self):
        self.knight.image['Slash'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)
    def attack_delay(self,e):
        if e[0]!='INPUT': return False
        if e[1].type==SDL_KEYDOWN and e[1].key == SDLK_x:self.alt_flag = True
        return self.knight.frame >= 6 and e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x


class AltAttack:
    def __init__(self, knight):
        self.knight = knight
    def enter(self, event):
        self.knight.frame = 0
        self.knight.frames = animation_frames[animation_names.index('SlashAlt')]
        self.knight.state = 'SlashAlt'
        self.effect = Effect(self.knight, shape='SlashEffectAlt')
        game_world.add_object(self.effect, 2)
        self.alt_flag = False
    def exit(self, event):
        pass
    def do(self):
        self.knight.frame = (self.knight.frame + ATK_FPA * ATK_APT * game_framework.frame_time) % (self.knight.frames +1)
        if self.knight.frame >= 7 and not self.alt_flag:
            self.knight.StateMachine.handle_state_event(('TIMEOUT', None))
        elif self.knight.frame >= 7 and self.alt_flag:
            self.knight.StateMachine.handle_state_event(('INPUT', SimpleNamespace(type=SDL_KEYDOWN, key=SDLK_x)))
    def draw(self):
        self.knight.image['Slash'][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)
    def attack_delay(self,e):
        if e[0] != 'INPUT': return False
        if e[1].type==SDL_KEYDOWN and e[1].key == SDLK_x:self.alt_flag = True
        return self.knight.frame >= 6 and e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x


class Effect:
    def __init__(self, knight, shape=None):
        self.knight = knight
        self.frame = 0
        if shape == None : self.shape = self.knight.state + 'Effect'
        else : self.shape = shape
        self.frames = animation_frames[animation_names.index(self.shape)]
    def update(self):
        self.frame = (self.frame + ATK_FPA * ATK_APT * game_framework.frame_time)
        if self.frame >= self.frames:
            game_world.remove_object(self)
    def draw(self):
        self.knight.image[self.shape][int(self.knight.frame)].composite_draw(0, 'h' if self.knight.dir == 1 else '', self.knight.x, self.knight.y)


class Knight:
    image = None
    def __init__(self):
        self.load_sprite()
        self.x, self.y = 400, 300
        self.sx,self.sy = 0,0
        self.state = 'Idle'
        self.frame = 0
        self.dir = -1
        self.move_dir = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.DASH = Dash(self)
        self.JUMP = jump(self)
        self.ALTATTACK = AltAttack(self)  # Placeholder for Alt Attack state
        self.StateMachine = StateMachine(
            self.IDLE,
    {
                self.IDLE : {x_down: self.ATTACK, right_down: self.WALK, left_down: self.WALK, c_down : self.DASH, alt_down : self.JUMP, right_up : self.WALK, left_up : self.WALK},
                self.ATTACK : {self.ATTACK.attack_delay : self.ALTATTACK, atk_timeout : self.WALK, time_out : self.IDLE, },
                self.WALK : {x_down: self.ATTACK, time_out : self.IDLE, c_down : self.DASH, alt_down : self.JUMP, right_down : self.IDLE, left_down : self.IDLE, right_up : self.IDLE, left_up : self.IDLE},
                self.DASH : { self.dash_timeout_to_walk: self.WALK,time_out: self.IDLE,},
                self.JUMP : {time_out: self.IDLE},
                self.ALTATTACK : {self.ALTATTACK.attack_delay : self.ATTACK,atk_timeout : self.WALK, time_out: self.IDLE,},

    }
        )
    def dash_timeout_to_walk(self,e):
        return e[0] == 'TIMEOUT' and (self.move_dir != 0 or SDLK_RIGHT in pressed_keys or SDLK_LEFT in pressed_keys)


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
        if SDLK_RIGHT in pressed_keys and not (SDLK_LEFT in pressed_keys):
            self.move_dir = 1
        elif SDLK_LEFT in pressed_keys and not (SDLK_RIGHT in pressed_keys):
            self.move_dir = -1
        else:
            self.move_dir = 0
        self.x += self.sx
        self.y += self.sy
        self.sx, self.sy = 0,0
    def handle_event(self, event):
        self.StateMachine.handle_state_event(('INPUT', event))



