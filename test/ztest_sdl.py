#!usr/bin/python3.6
# -*- coding: <utf-8> -*-
from time import sleep

from orderedset import OrderedSet

from modules.easydependencies import setup_third_party
setup_third_party()
try:
    import sdl2.ext
    from sdl2 import *
except ImportError as e:
    from modules.easydependencies import handle_importerror
    handle_importerror(e)

    import sdl2.ext
    from sdl2 import *


def update_spriterenderer(factory, spriterenderer):
    sprite = factory.from_image(pic_path)
    spriterenderer.render(sprite)
    return sprite


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


def run():
    sdl2.ext.init()
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    spriterenderer = factory.create_sprite_render_system(window)
    update_spriterenderer(factory, spriterenderer)
    window.show()
    setup_third_party()
    running = True
    while running:
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






