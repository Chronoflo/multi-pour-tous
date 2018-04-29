#!usr/bin/python3.6
# -*- coding: <utf-8> -*-

from modules.easydependencies import  setup_third_party
try:
    setup_third_party()
    import sdl2.ext
except ImportError:
    from modules.easydependencies import install_requirements
    install_requirements()

    import sdl2.ext