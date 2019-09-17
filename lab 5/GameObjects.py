from Shapes import *
from sdl2.keycode import *
from Program import *
import math3d

ON_GROUND = 0
RISING = 1
FALLING = 2

FACING_LEFT = 3
FACING_RIGHT = 4

def changeUniform(translationVec):
    Program.setUniform("translation", translationVec)
    Program.updateUniforms()

class StarBackground:
    vbuff = None
    def __init__(self, x, y):
        self.pos = math3d.vec2(x, y)
        if StarBackground.vbuff == None:
            StarBackground.vbuff = array.array("f")
            StarBackground.vbuff = createRandPoints(StarBackground.vbuff, globs.numStars)
            glCommands.setup(StarBackground.vbuff)

    def draw(self):
        changeUniform(self.pos)
        glCommands.draw(glCommands.GL_POINTS, len(StarBackground.vbuff), StarBackground.vbuff)

    def alive(self):
        return True


class Bullet:
    vbuff = None
    ibuff = None
    def __init__(self, x, y, direction, size = .2):
        self.pos = math3d.vec2(x, y)
        self.dir = direction
        self.life = 750

        if Bullet.vbuff == None and Bullet.ibuff == None:
            Bullet.vbuff = array.array("f")
            Bullet.ibuff = array.array("I")
            createCircle(Bullet.vbuff, size, 0, 0)
            createCircleIndexArray(Bullet.ibuff)
            glCommands.setup(Bullet.vbuff, Bullet.ibuff)

        self.playSound()

    def update(self, elapsedTime):
        bulletMovRate = globs.bulletSpeed * elapsedTime
        if self.dir == FACING_LEFT:
            self.pos[0] -= bulletMovRate
        elif self.dir == FACING_RIGHT:
            self.pos[0] += bulletMovRate
        self.life -= elapsedTime

    def draw(self):
        print("bullet call this draw")
        changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(Bullet.ibuff), Bullet.vbuff, Bullet.ibuff, 0)

    def alive(self):
        return self.life > 0

    def playSound(self):
        Mix_FadeInChannelTimed(-1, globs.pulseSound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py


class Player:
    def __init__(self, x, y, size):
        self.pos = math3d.vec2(x, y)    #set players start position
        self.direction = 0              #-1:Left, 1:Right
        self.lastFired = 0
        self.state = ON_GROUND
        self.life = 10
        self.size = size
        self.vbuff = array.array("f")
        self.ibuff = array.array("I")
        createSquare(self.vbuff, size, size, x, y)
        createSquareIndexArray(self.ibuff)
        glCommands.setup(self.vbuff, self.ibuff)

    def draw(self):
        changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(self.ibuff), self.vbuff, self.ibuff, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.direction = FACING_RIGHT
            self.pos[0] += globs.playerSpeed * elapsedTime

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.direction = FACING_LEFT
            self.pos[0] -= globs.playerSpeed * elapsedTime

        if self.state == RISING:
            self.pos[1] += globs.playerSpeed * elapsedTime

        elif self.state == FALLING:
            self.pos[1] -= globs.playerSpeed * elapsedTime

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            globs.objectsToDraw.append(Bullet(self.pos[0], self.pos[1], self.direction))
            self.lastFired = globs.playerFireRate

        if SDLK_w in globs.keyset and self.state == ON_GROUND:
            self.state = RISING

        elif self.pos[1] >= globs.jumpPeak and self.state == RISING:
            self.pos[1] = globs.jumpPeak
            self.state = FALLING

        elif self.pos[1] <= 0 and self.state == FALLING:
            self.pos[1] = 0
            self.state = ON_GROUND

        self.lastFired -= elapsedTime

    def alive(self):
        return self.life > 0