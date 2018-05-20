#!usr/bin/python3.6
# -*- coding: <utf-8> -*-
import subprocess
from time import sleep

from modules.const import stream_addr, stream_port

try:
    from modules.easydependencies import setup_third_party
    setup_third_party()
    from modules.handyfunctions import get_frames_folder, os_adapt, get_modules_path, to_command, InfiniteTimer
    import sdl2.ext
    from sdl2 import *
    from sdl2.ext import colorpalettes
except ImportError as e:
    from modules.easydependencies import handle_importerror
    handle_importerror(e)

    from modules.easydependencies import setup_third_party
    setup_third_party()
    from modules.handyfunctions import get_frames_folder, os_adapt, get_modules_path, to_command, InfiniteTimer
    import sdl2.ext
    from sdl2 import *
    from sdl2.ext import colorpalettes


kb_state = SDL_GetKeyboardState(None)


class DynamicBG:
    """Un arrière-plan dynamique qui change de couleur dans un sens, puis dans l'autre."""
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
    """Retourne le chemin de la police donnée."""
    return get_modules_path() + os_adapt("/../setup/fonts/") + font_name


# Initialise des couleurs et un gestionnaire de polices
my_colors = {'red': (255, 0, 0, 255),
             'nice_blue': (58, 74, 188, 255),
             'nice_gray': (50, 50, 50, 255)}
for k, v in my_colors.items():
    my_colors[k] = sdl2.ext.Color(*v)

font_manager = sdl2.ext.FontManager(get_font("OpenSans-Regular.ttf"), "OpenSans")
font_manager.add(get_font("Pacifico.ttf"), "Pacifico")


class Stream:
    def __init__(self, on_kbupdt=None):
        self._disp_proc = None
        self.running = False
        self.pressed_keys = set()
        self.on_kb = on_kbupdt

    def recv_and_disp(self, address=stream_addr, port=stream_port, soft_name="The Pong Game",
                             on_kbupdt=None, enable_display=True):
        """
        Affiche un stream vidéo reçu par udp.

        :param address: L'adresse source du stream
        :param port: Le port source du stream
        :param soft_name: Le nom du logiciel source
        :param on_kbupdt: La fonction à appeler en cas de mise à jour du clavier
        :return:
        """
        if on_kbupdt is not None:
            self.on_kb = on_kbupdt
        if enable_display:
            self._disp_proc = subprocess.Popen(
                 to_command(
                     'ffmpeg -re -f mpegts -i udp://{}:{} -f sdl2 "{}"'.format(
                        address, port, soft_name
                     )), stdin=subprocess.PIPE)
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

        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_INFORMATION, "Initialisation".encode("utf8"),
                                 "Veuillez patienter jusqu'à l'affichage du stream.".encode("utf8"),
                                 sdlwindow)
        # Crée la factory qui servira à créer les sprites et le renderer qui les affichera
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        renderer = factory.create_sprite_render_system(window)

        # Crée un sprite "background" et un sprite texte affiché dessus
        background = factory.from_color(my_colors['nice_blue'], (window_w, window_h))
        background_txt = factory.from_text("Cliquer ici pour envoyez vos entrées.",
                                           fontmanager=font_manager, alias="Pacifico",
                                           size=int(window_h * 0.5))
        background_txt.position = (window_w // 2 - background_txt.size[0] // 2,
                                   window_h // 2 - background_txt.size[1] // 2)

        # Display window with background and text
        window.show()
        renderer.render((background, background, background_txt))

        self.running = True
        while self.running:
            # Vérifie que l'affichage à distance est bien actif, sinon quitte
            if self._disp_proc is not None:
                if self._disp_proc.poll() is not None:
                    self.running = False
            evnts = sdl2.ext.get_events()
            for event in evnts:
                if event.type == SDL_QUIT:
                    self.running = False
                    break
                if event.type == sdl2.SDL_KEYDOWN:
                    prev_pressed_keys = set(self.pressed_keys)
                    self.pressed_keys.add(event.key.keysym.sym)
                    if self.pressed_keys.difference(prev_pressed_keys):
                        print("lol")
                        if self.on_kb is not None:
                            self.on_kb(self.pressed_keys)
                elif event.type == sdl2.SDL_KEYUP:
                    prev_pressed_keys = set(self.pressed_keys)
                    self.pressed_keys.remove(event.key.keysym.sym)
                    if prev_pressed_keys.difference(self.pressed_keys):
                        if self.on_kb is not None:
                            self.on_kb(self.pressed_keys)
            SDL_Delay(50)
            sleep(0)

        SDL_DestroyWindow(sdlwindow)
        SDL_Quit()
        if self._disp_proc is not None:
            self._disp_proc.kill()
        return 0

    def stop(self):
        self.running = False
        if self._disp_proc is not None:
            if self._disp_proc.poll() is None:
                self._disp_proc.communicate(b'q')
                self._disp_proc.kill()


if __name__ == '__main__':
    stream = Stream()
    stream.recv_and_disp(enable_display=False)






