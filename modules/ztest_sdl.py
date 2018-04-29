#!usr/bin/python3.6
# -*- coding: <utf-8> -*-

from modules.easydependencies import setup_third_party

try:
    import sdl2.ext
    from sdl2 import SDL_GetKeyboardState
except ImportError:
    from modules.easydependencies import handle_importerror
    handle_importerror()

    import sdl2.ext

setup_third_party()
print(SDL_GetKeyboardState())

