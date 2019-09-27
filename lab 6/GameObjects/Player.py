from sdl2.keycode import *
from utilityLibs import glCommands, ImageTexture2DArray
from toolLibs import math3d
from GameObjects import Bullet, Shapes
import array, globs

class Player:
    def __init__(self, x, y, size):
        self.pos = math3d.vec2(x, y)    #set players start position
        self.crouchScale = math3d.vec2(1, .5)
        self.crouching = False
        self.direction = 0              #-1:Left, 1:Right
        self.lastFired = 0              #Time since last Fired
        self.state = globs.ON_GROUND    #State player is in
        self.life = 10                  #amount of life left
        self.size = size                #Scale of player
        self.halfSize = size / 2        #half scale of player
        self.vbuff = array.array("f")
        self.tbuff = array.array("f")
        self.ibuff = array.array("I")
        self.tex = ImageTexture2DArray.ImageTexture2DArray(*globs.playerTextures);

        Shapes.createSquare(self.vbuff, size, size, x, y)
        Shapes.createSquareTextureArray(self.tbuff)
        Shapes.createSquareIndexArray(self.ibuff)
        glCommands.setup(self.vbuff, self.ibuff, self.tbuff)

    def draw(self):
        #print(str(self.pos))
        self.tex.bind(0)
        if self.crouching:
            glCommands.changeUniform(self.pos, self.crouchScale)
        else:
            glCommands.changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(self.ibuff), self.vbuff, self.ibuff, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.direction = globs.FACING_RIGHT
            self.pos[0] += globs.playerSpeed * elapsedTime

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.direction = globs.FACING_LEFT
            self.pos[0] -= globs.playerSpeed * elapsedTime

        if (SDLK_s or SDLK_DOWN) in globs.keyset:
            self.crouching = True
        else:
            self.crouching = False

        if self.state == globs.RISING:
            self.pos[1] += globs.playerSpeed * elapsedTime

        elif self.state == globs.FALLING:
            self.pos[1] -= globs.playerSpeed * elapsedTime

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            bulletPosY = self.pos[1]+self.halfSize
            if self.crouching: bulletPosY *= .5
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