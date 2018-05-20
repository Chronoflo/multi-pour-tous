from modules.handyfunctions import *
from modules.const import *
setup_third_party()
import sdl2.ext

path = get_modules_path() + os_adapt("/const.py")
with open(path, 'r') as f:
    data = f.read()

data = take_part(take_part(take_part(data, AFTER, '&', RIGHT), AFTER, '[', RIGHT), LEFT, ',', RIGHT)

dic_DIK = [take_part(i, AFTER, ' ', RIGHT) for i in data.split(',')]
ii = 0
def get_next():
    global running
    global ii
    try:
        print(dic_DIK[ii])
    except IndexError:
        running = False
    ii += 1
answers = []

sdl2.ext.init()
window = sdl2.ext.Window("Capture", (800,600), flags=SDL_WINDOW_SHOWN)

get_next()
running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
            break
        if event.type == sdl2.SDL_KEYDOWN:
            answers.append(event.key.keysym.sym)
            print(event.key.keysym.sym)
            get_next()

sdl_to_dik = {}
for s,d in zip(answers, dic_DIK):
    sdl_to_dik[s] = d

to_write = ',\n'.join(str(sdl_to_dik).split(','))

with open(path, 'a') as f:
    f.write(to_write)


