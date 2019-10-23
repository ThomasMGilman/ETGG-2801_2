from sdl2.keycode import *
from GameObjects import Bullet
from GameObjects.Entity import *
import globs

class Player(Entity):
    tex = None
    def __init__(self, x, y, Width, Height):
        self.halfHeight = Width / 2
        self.lastFired = 0              #Time since last Fired
        self.jumpState = globs.ON_GROUND#State player is in

        super().__init__(x, y, 0, Width, Height, globs.playerLife, globs.playerSpeed)
        if Player.tex == None:
            Player.tex = ImageTexture2DArray(*globs.playerTextures);

    def draw(self):
        super().draw(self.pos, self.scale, Player.tex, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.dir = globs.FACING_RIGHT
            super().updateHorizontalPos(self.speed * elapsedTime)

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.dir = globs.FACING_LEFT
            super().updateHorizontalPos(-self.speed * elapsedTime)

        if (SDLK_s or SDLK_DOWN) in globs.keyset:
            if self.scale[1] != self.halfHeight:
                self.scale = vec2(self.Height, self.halfHeight)
                super().setWorldMatrix()
        elif self.scale[1] != self.Width:
            self.scale = vec2(self.Height, self.Width)
            super().setWorldMatrix()

        if self.jumpState == globs.RISING:
            super().updateVerticalPos(self.speed * elapsedTime)

        elif self.jumpState == globs.FALLING:
            super().updateVerticalPos(-self.speed * elapsedTime)

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            bulletPosY = self.pos[1]+(self.scale[1] * .25)
            globs.Bullets.append(Bullet.Bullet(self.pos[0], bulletPosY, self.dir))
            self.lastFired = globs.playerFireRate

        if SDLK_w in globs.keyset and self.jumpState == globs.ON_GROUND:
            self.jumpState = globs.RISING

        elif self.pos[1] >= globs.jumpPeak and self.jumpState == globs.RISING:
            self.pos[1] = globs.jumpPeak
            self.jumpState = globs.FALLING

        elif self.pos[1] <= 0 and self.jumpState == globs.FALLING:
            self.pos[1] = 0
            self.jumpState = globs.ON_GROUND

        self.lastFired -= elapsedTime