import sys

from modules.handyfunctions import get_modules_path, ensure_path, os_adapt

try:
    import sdl2.ext
except ImportError:
    from modules.easydependencies import install_requirements
    install_requirements()

    import sdl2.ext

ressources_path = get_modules_path() + '/../pictures'
ensure_path(ressources_path)
RESOURCES = sdl2.ext.Resources(__file__, os_adapt(ressources_path))

sdl2.ext.init()

window = sdl2.ext.Window("Hello World!", size=(640, 480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite = factory.from_image(RESOURCES.get_path("smiley.bmp"))

spriterenderer = factory.create_sprite_render_system(window)
spriterenderer.render(sprite)

# will cause the renderer to draw the sprite 10px to the right and
# 20 px to the bottom
sprite.position = 10, 20

# will cause the renderer to draw the sprite 55px to the right and
# 10 px to the bottom
sprite.position = 55, 10

processor = sdl2.ext.TestEventProcessor()
processor.run(window)

sdl2.ext.quit()