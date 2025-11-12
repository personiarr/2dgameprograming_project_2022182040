import random
from pico2d import *
import state_machine
import game_framework
import game_world
import knight
from knight import Knight, Effect
from maps import Map
main_ch = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            main_ch.handle_event(event)
            if event.type == SDL_KEYDOWN:
                knight.pressed_keys.add(event.key)
            elif event.type == SDL_KEYUP:
                knight.pressed_keys.discard(event.key)


def init():
    global main_ch
    main_ch = Knight()
    game_world.add_object(main_ch, 1)
    map = Map()
    game_world.add_object(map, 0)

    game_world.add_collision_pairs("knight:ground", main_ch, map)

def update():
    game_world.update()
    # boy, ball 충돌 처리
    game_world.handle_collision()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

