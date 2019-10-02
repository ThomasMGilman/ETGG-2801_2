from sdl2.keycode import *
from GameObjects import Bullet
from GameObjects.Entity import *
import globs

class Player(Entity):
    vbuff = None
    tbuff = None
    ibuff = None
    vao = None
    tex = None
    def __init__(self, x, y, size):
        self.pos = math3d.vec2(x, y)    #set players start position
        self.Height = size
        self.Width = size
        self.halfWidth = self.Width/2
        self.playerScale = math3d.vec2(self.Height, self.Width)
        self.direction = 0              #-1:Left, 1:Right
        self.lastFired = 0              #Time since last Fired
        self.state = globs.ON_GROUND    #State player is in
        self.life = 10                  #amount of life left

        super().__init__()
        if Player.tex == None:
            Player.tex = ImageTexture2DArray.ImageTexture2DArray(*globs.playerTextures);

    def draw(self):
        super().draw(self.pos, self.playerScale, Player.tex, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.direction = globs.FACING_RIGHT
            self.pos[0] += globs.playerSpeed * elapsedTime

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.direction = globs.FACING_LEFT
            self.pos[0] -= globs.playerSpeed * elapsedTime

        if (SDLK_s or SDLK_DOWN) in globs.keyset:
            if self.playerScale[1] != self.halfWidth:
                self.playerScale = math3d.vec2(self.Height, self.halfWidth)
        elif self.playerScale[1] != self.Width:
            self.playerScale = math3d.vec2(self.Height, self.Width)

        if self.state == globs.RISING:
            self.pos[1] += globs.playerSpeed * elapsedTime

        elif self.state == globs.FALLING:
            self.pos[1] -= globs.playerSpeed * elapsedTime

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            bulletPosY = self.pos[1]+(self.playerScale[1]*.25)
            globs.objectsToDraw.append(Bullet.Bullet(self.pos[0], bulletPosY, self.direction))
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

    def alive(self):
        return self.life > 0