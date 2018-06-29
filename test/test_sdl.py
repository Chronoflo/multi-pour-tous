#!usr/bin/python3.6
# -*- coding: <utf-8> -*-
import subprocess

from modules.const import stream_addr, stream_port

try:
    from modules.easydependencies import setup_third_party
    setup_third_party()
    from modules.handyfunctions import get_frames_folder, os_adapt, get_modules_path, to_command, InfiniteTimer
    import sdl2.ext
    from sdl2 import *
    from sdl2.ext import colorpalettes
    from orderedset import OrderedSet
    from construct import *
except ImportError as e:
    from modules.easydependencies import handle_importerror
    handle_importerror(e)

    from modules.easydependencies import setup_third_party
    setup_third_party()
    from modules.handyfunctions import get_frames_folder, os_adapt, get_modules_path, to_command, InfiniteTimer
    import sdl2.ext
    from sdl2 import *
    from sdl2.ext import colorpalettes
    from orderedset import OrderedSet
    from construct import *


kb_state = SDL_GetKeyboardState(None)
pressed_key = OrderedSet()


class DynamicBG:
    """Make a dynamic background that changes colors"""
    def __init__(self, factory, renderer, ext_window, on_top_sprite=None, i=188, fps=60):
        self._factory = factory
        self._renderer = renderer
        self._on_top_sprite = on_top_sprite
        self._switch_on = True
        self.i = i
        self.blue_nuances = [factory.from_color(sdl2.ext.Color(58, 76, i), ext_window.size) for i in range(256)]

    def update(self):
        if self._switch_on:
            if self.i != 255:
                self.i += 1
            else:
                self._switch_on = False
        else:
            if self.i != 0:
                self.i -= 1
            else:
                self._switch_on = True
        self._renderer.render(self.blue_nuances[self.i])


def get_font(font_name):
    """Return the path of the given font_name."""
    return get_modules_path() + os_adapt("/../setup/fonts/") + font_name


my_colors = {'red': (255, 0, 0, 255),
             'nice_blue': (58, 74, 188, 255),
             'nice_gray': (50, 50, 50, 255)}
for k, v in my_colors.items():
    my_colors[k] = sdl2.ext.Color(*v)

font_manager = sdl2.ext.FontManager(get_font("OpenSans-Regular.ttf"))
font_manager.add(get_font("Pacifico.ttf"), "Pacifico")


def with_on_kb(display, sdlwindow, updt):
    running = True
    while running:
        # Vérifie que l'affichage à distance est bien actif, sinon quitte
        if display.poll() is not None:
            running = False
        evnts = sdl2.ext.get_events()
        for event in evnts:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                pressed_key.add(event.key.keysym.sym)
                updt()
            elif event.type == sdl2.SDL_KEYUP:
                pressed_key.remove(event.key.keysym.sym)
                updt()

    SDL_DestroyWindow(sdlwindow)
    SDL_Quit()
    if display is not None:
        display.kill()

    return True


def without_on_kb(display, sdlwindow):
    running = True
    while running:
        # Vérifie que l'affichage à distance est bien actif, sinon quitte
        if display.poll() is not None:
            running = False
        evnts = sdl2.ext.get_events()
        for event in evnts:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                pressed_key.add(event.key.keysym.sym)
            elif event.type == sdl2.SDL_KEYUP:
                pressed_key.remove(event.key.keysym.sym)

    SDL_DestroyWindow(sdlwindow)
    SDL_Quit()
    if display is not None:
        display.kill()

    return True


def recv_stream(address=stream_addr, port=stream_port, display_enabled=True, on_kb_update=None):
    display = None
    if display_enabled:
        display = subprocess.Popen(
             to_command(
                 #'ffmpeg -re -f mpegts -i udp://{}:{} -f sdl CLI'.format(
                 'ffmpeg -f gdigrab -i title="The Pong Game" -f sdl2 "The Pong Game"'.format(
                    address, port
                 )))
    setup_third_party()

    sdl2.ext.init()

    # Get informations about the usable area of the screen
    usable_bounds = SDL_Rect()
    SDL_GetDisplayUsableBounds(0, usable_bounds)

    # Creates window
    window_h = int(usable_bounds.h * 0.1)
    window = sdl2.ext.Window("CLIENT",
                             (usable_bounds.w, window_h),
                             (SDL_WINDOWPOS_CENTERED, usable_bounds.h - window_h),
                             SDL_WINDOW_BORDERLESS)
    window_w = window.size[0]
    window_h = window.size[1]
    sdlwindow = window.window

    # Crée la factory qui servira à créer les sprites et le renderer qui les affichera
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    renderer = factory.create_sprite_render_system(window)

    # Crée un sprite "background" à partir d'une couleur unie
    background = factory.from_color(my_colors['nice_blue'], (window_w, window_h))
    background_txt = factory.from_text("Cliquer ici pour envoyez vos entrées.",
                                       fontmanager=font_manager, alias="Pacifico",
                                       size=int(window_h * 0.5))
    background_txt.position = (window_w // 2 - background_txt.size[0] // 2,
                               window_h // 2 - background_txt.size[1] // 2)

    # Display window with background and text
    window.show()
    renderer.render((background, background, background_txt))

    if on_kb_update is not None:
        with_on_kb(display, sdlwindow, on_kb_update)
    else:
        without_on_kb(display, sdlwindow)

    return 0


if __name__ == '__main__':
    recv_stream()






