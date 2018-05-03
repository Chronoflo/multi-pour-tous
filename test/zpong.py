import sys
from math import cos

from modules.handyfunctions import get_modules_path, ensure_path, os_adapt
from modules.easydependencies import setup_third_party
try:
    setup_third_party()
    import sdl2.ext
except ImportError:
    from modules.easydependencies import install_requirements
    install_requirements()

    import sdl2.ext

pic_folder = get_modules_path() + '/../pictures/'
LEFT = -1
RIGHT = 1


def create_sprite(pic_path, window):
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sprite = factory.from_image(pic_path)
    spriterenderer = factory.create_sprite_render_system(window)
    spriterenderer.render(sprite)
    return sprite


def move_sprite(sprite, x, y):
    sprite.position = sprite.x + x, sprite.y + y


WHITE = sdl2.ext.Color(255, 255, 255)


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if collitems:
            self.ball.velocity.vx = -self.ball.velocity.vx

            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = - self.ball.velocity.vy

        if (self.ball.sprite.y <= self.miny or
                self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxy):
            self.ball.velocity.vy = - self.ball.velocity.vy

        if (self.ball.sprite.x <= self.minx or
                self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx):
            self.ball.velocity.vx = - self.ball.velocity.vx


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class TrackingAIController(sdl2.ext.Applicator):
    def __init__(self, miny, maxy):
        super(TrackingAIController, self).__init__()
        self.componenttypes = PlayerData, Velocity, sdl2.ext.Sprite
        self.miny = miny
        self.maxy = maxy
        self.ball = None

    def process(self, world, componentsets):
        for pdata, vel, sprite in componentsets:
            if not pdata.ai:
                continue

            centery = sprite.y + sprite.size[1] // 2
            if pdata.side * self.ball.velocity.vx < 0:
                # ball is moving away from the AI
                if centery < self.maxy // 2:
                    vel.vy = 3
                elif centery > self.maxy // 2:
                    vel.vy = -3
                else:
                    vel.vy = 0
            else:
                bcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
                if bcentery < centery:
                    vel.vy = -3
                elif bcentery > centery:
                    vel.vy = 3
                else:
                    vel.vy = 0


class PlayerData(object):
    def __init__(self, side):
        super(PlayerData, self).__init__()
        self.ai = False
        self.speed = 15
        self.side = side


class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False, side=1):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData(side)
        self.playerdata.ai = ai


class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()

    world = sdl2.ext.World()

    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)
    spriterenderer = SoftwareRenderer(window)
    aicontroller = TrackingAIController(0, 600)
    world.add_system(movement)
    world.add_system(collision)
    world.add_system(spriterenderer)
    world.add_system(aicontroller)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    player1 = Player(world, sp_paddle1, 0, 250, side=LEFT)
    player2 = Player(world, sp_paddle2, 780, 250, side=RIGHT)
    ball = Ball(world, sp_ball, 390, 290)
    ball.velocity.vx = -10

    collision.ball = ball
    aicontroller.ball = ball

    players_speed = 12
    player1.playerdata.speed = players_speed
    player2.playerdata.speed = players_speed
    i = 0
    running = True
    while running:
        create_sprite(pic_folder + 'smiley.bmp', window)
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    player2.velocity.vy = -player2.playerdata.speed
                elif event.key.keysym.sym == sdl2.SDLK_z:
                    player1.velocity.vy = -player1.playerdata.speed
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    player2.velocity.vy = player2.playerdata.speed
                elif event.key.keysym.sym == sdl2.SDLK_s:
                    player1.velocity.vy = player1.playerdata.speed
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_z, sdl2.SDLK_s):
                    player1.velocity.vy = 0
                elif event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    player2.velocity.vy = 0
        sdl2.SDL_Delay(10)
        world.process()
        window.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(run())
