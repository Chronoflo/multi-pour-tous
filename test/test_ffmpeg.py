import platform
import sys

import ffmpeg

from modules.handyfunctions import get_modules_path, os_adapt
import ctypes

# _lib = ctypes.cdll.LoadLibrary(get_modules_path() + os_adapt("/../third_party/all/64/ffstream.dll"))

print(platform.architecture())