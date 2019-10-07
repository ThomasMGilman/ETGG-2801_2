from sdl2.keycode import *
from GameObjects import Bullet
from GameObjects.Entity import *
import globs

class Player(Entity):
    tex = None
    def __init__(self, x, y, Width, Height):
        self.pos = math3d.vec2(x, y)    #set players start position
        self.halfHeight = Width / 2
        self.lastFired = 0              #Time since last Fired
        self.state = globs.ON_GROUND    #State player is in

        super().__init__(x, y, 0, Width, Height, globs.playerLife, globs.playerSpeed)
        if Player.tex == None:
            Player.tex = ImageTexture2DArray(*globs.playerTextures);

    def draw(self):
        super().draw(self.pos, self.scale, Player.tex, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.dir = globs.FACING_RIGHT
            self.pos[0] += self.speed * elapsedTime

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.dir = globs.FACING_LEFT
            self.pos[0] -= self.speed * elapsedTime

        if (SDLK_s or SDLK_DOWN) in globs.keyset:
            if self.scale[1] != self.halfHeight:
                self.scale = math3d.vec2(self.Height, self.halfHeight)
        elif self.scale[1] != self.Width:
            self.scale = math3d.vec2(self.Height, self.Width)

        if self.state == globs.RISING:
            self.pos[1] += self.speed * elapsedTime

        elif self.state == globs.FALLING:
            self.pos[1] -= self.speed * elapsedTime

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            bulletPosY = self.pos[1]+(self.scale[1] * .25)
            globs.objectsToDraw.append(Bullet.Bullet(self.pos[0], bulletPosY, self.dir))
            self.lastFired = globs.playerFireRate

        if SDLK_w in globs.keyset and self.state == globs.ON_GROUND:
            self.state = globs.RISING

        elif self.pos[1] >= globs.jumpPeak and self.state == globs.RISING:
            self.pos[1] = globs.jumpPeak
            self.state = globs.FALLING

        elif self.pos[1] <= 0 and self.state == globs.FALLING:
            self.pos[1] = 0
            self.state = globs.ON_GROUND

        self.lastFired -= elapsedTime