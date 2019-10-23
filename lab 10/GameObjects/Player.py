from sdl2.keycode import *
from GameObjects import Bullet, Camera
from GameObjects.Entity import *
import globs

class Player(Entity):
    tex = None
    def __init__(self, x, y, Width, Height):
        self.halfHeight = Width / 2
        self.lastFired = 0              #Time since last Fired

        if Player.tex == None:
            Player.tex = ImageTexture2DArray(*globs.playerTextures);

        super().__init__(x, y, 0, Width, Height, globs.playerLife, globs.playerSpeed, "Player")
        self.CameraObj = Camera.Camera(self.pos)

    def draw(self):
        self.CameraObj.setUniforms()
        super().draw(Player.tex, 0)

    def fire(self):
        bulletPosY = self.pos[1] + (self.scale[1] * .25)
        globs.Bullets.append(Bullet.Bullet(self.pos[0], bulletPosY, self.dir))
        self.lastFired = globs.playerFireRate

    def updateCameraPos(self, x, y):
        self.CameraObj.pan(x, y)

    def update(self, elapsedTime):
        movAmount = 0
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:                      #Move Right
            self.dir = globs.FACING_RIGHT
            movAmount = self.speed * elapsedTime
            super().updateHorizontalPos(movAmount)
            self.updateCameraPos(movAmount, 0)

        if (SDLK_a or SDLK_LEFT) in globs.keyset:                       #Move Left
            self.dir = globs.FACING_LEFT
            movAmount = -self.speed * elapsedTime
            super().updateHorizontalPos(movAmount)
            self.updateCameraPos(movAmount, 0)

        if (SDLK_w or SDLK_UP) in globs.keyset:                         #Move UP
            self.dir = globs.FACING_UP
            movAmount = self.speed * elapsedTime
            super().updateVerticalPos(movAmount)
            self.updateCameraPos(0, movAmount)

        if (SDLK_s or SDLK_DOWN) in globs.keyset:                       #Move Down
            self.dir = globs.FACING_DOWN
            movAmount = -self.speed * elapsedTime
            super().updateVerticalPos(movAmount)
            self.updateCameraPos(0, movAmount)

        if (SDLK_LCTRL or SDLK_x) in globs.keyset:
            if self.scale[1] != self.halfHeight:
                self.scale = vec2(self.Height, self.halfHeight)
                super().setWorldMatrix()
        elif self.scale[1] != self.Width:
            self.scale = vec2(self.Height, self.Width)
            super().setWorldMatrix()

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:          #fireBullet
            self.fire()

        self.lastFired -= elapsedTime