import ctypes
from time import sleep

from modules.const import DIK_UP, DIK_Z
from modules.symdirectinput import press_key, release_key

already_pressed_keys = {1, 2, 4, 5}
pressed_keys_recvd = {0,2, 4, 8,9}
keys_to_press = pressed_keys_recvd.difference(already_pressed_keys)
keys_to_release = already_pressed_keys.difference(pressed_keys_recvd)
print(keys_to_press)
print(keys_to_release)

#z
while True:
    press_key(DIK_Z)
    sleep(0.1)
    release_key(DIK_Z)
    sleep(2)
