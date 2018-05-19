#!usr/bin/python3.6
# -*- coding: <utf-8> -*-
from time import sleep, time

from orderedset import OrderedSet

from modules.easydependencies import setup_third_party
from modules.handyfunctions import get_frames_folder, os_adapt, get_modules_path

setup_third_party()
try:
    import sdl2.ext
    from sdl2 import *
except ImportError as e:
    from modules.easydependencies import handle_importerror
    handle_importerror(e)

    import sdl2.ext
    from sdl2 import *

pic_path = get_frames_folder()
i_f = 1

def get_sprite(factory):
    global i_f
    f = factory
    number = str(i_f)
    i_f += 1
    tmp = ""
    for i in range(4 - len(number)):
        tmp += '0'
    number = tmp + number
    return f.from_image(os_adapt(pic_path + "/thumb" + number + '.bmp'))


kb_state = SDL_GetKeyboardState(None)
pressed_key = OrderedSet()


def check_kb(event):
    to_print = []
    if not kb_state[SDL_SCANCODE_Z]:
        to_print.append("z released")
    else:
        to_print.append("z pressed")
    if not kb_state[SDL_SCANCODE_LSHIFT]:
        to_print.append("shift released")
    else:
        to_print.append("shift pressed")


last = time()
delay = 1 / 60


def update_sprite(spriterenderer, factory):
    global last
    global delay
    current = time()
    if current - last >= delay:
        spriterenderer.render(get_sprite(factory))
        last = current


def run():
    sdl2.ext.init()
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    window = sdl2.ext.Window("CLIENT", size=(800, 600))
    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(factory.from_image(get_modules_path() + os_adapt("/../pictures/smiley.bmp")))
    window.show()
    setup_third_party()
    running = True
    while running:
        # update_sprite(spriterenderer, factory)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                pressed_key.add(event.key.keysym.sym)
                print(pressed_key)
            elif event.type == sdl2.SDL_KEYUP:
                pressed_key.remove(event.key.keysym.sym)
                print(pressed_key)


if __name__ == '__main__':
    run()






