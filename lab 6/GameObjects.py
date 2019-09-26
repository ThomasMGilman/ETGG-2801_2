from Shapes import *
from sdl2.keycode import *
from Program import *
from utilityLibs import Textures
from utilityLibs import glCommands
from toolLibs import math3d

ON_GROUND = 0
RISING = 1
FALLING = 2

FACING_LEFT = 3
FACING_RIGHT = 4

def changeUniform(translationVec, scalingVec = math3d.vec2(1,1)):
    Program.setUniform("translation", translationVec)
    Program.setUniform("scaling", scalingVec)
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

class mapSquare:
    vbuff = None
    tbuff = None
    ibuff = None
    tex = None
    def __init__(self, x, y, size):
        self.pos = math3d.vec2(x, y)
        self.size = size
        if mapSquare.vbuff == None or mapSquare.tbuff == None or mapSquare.ibuff == None:
            mapSquare.vbuff     = array.array("f")
            mapSquare.tbuff     = array.array("f")
            mapSquare.ibuff     = array.array("I")
            mapSquare.tex = Textures.ImageTexture2DArray(globs.mapTextures)
            createSquare(mapSquare.vbuff, self.size, self.pox.x, self.pos.y)
            createSquareIndexArray(mapSquare.ibuff)
            glCommands.setup(mapSquare.vbuff, mapSquare.ibuff, mapSquare.tbuff)


class Bullet:
    vbuff = None
    tbuff = None
    ibuff = None
    tex = None
    def __init__(self, x, y, direction, size = .05):
        self.pos = math3d.vec2(x, y)
        self.dir = direction
        self.life = 750

        if Bullet.vbuff == None and Bullet.ibuff == None:
            Bullet.vbuff    = array.array("f")
            Bullet.tbuff    = array.array("f")
            Bullet.ibuff    = array.array("I")
            Bullet.tex      = Textures.ImageTexture2DArray("Bullet.png")
            createCircle(Bullet.vbuff, size, 0, 0+size)
            createCircleIndexArray(Bullet.ibuff)
            glCommands.setup(Bullet.vbuff, Bullet.ibuff, Bullet.tbuff)

        self.playSound()

    def update(self, elapsedTime):
        bulletMovRate = globs.bulletSpeed * elapsedTime
        if self.dir == FACING_LEFT:
            self.pos[0] -= bulletMovRate
        elif self.dir == FACING_RIGHT:
            self.pos[0] += bulletMovRate
        self.life -= elapsedTime

    def draw(self):
        Bullet.tex.bind(0)
        changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(Bullet.ibuff), Bullet.vbuff, Bullet.ibuff, 0)

    def alive(self):
        return self.life > 0

    def playSound(self):
        Mix_FadeInChannelTimed(-1, globs.pulseSound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py


class Player:
    def __init__(self, x, y, size):
        self.pos = math3d.vec2(x, y)    #set players start position
        self.crouchScale = math3d.vec2(1, .5)
        self.crouching = False
        self.direction = 0              #-1:Left, 1:Right
        self.lastFired = 0
        self.state = ON_GROUND
        self.life = 10
        self.size = size
        self.halfSize = size / 2
        self.vbuff = array.array("f")
        self.tbuff = array.array("f")
        self.ibuff = array.array("I")
        self.tex = Textures.ImageTexture2DArray(*globs.playerTextures);

        createSquare(self.vbuff, size, size, x, y)
        createSquareTextureArray(self.tbuff)
        createSquareIndexArray(self.ibuff)
        glCommands.setup(self.vbuff, self.ibuff, self.tbuff)

        print("NumSLices to texture: "+str(self.tex.slices))

    def draw(self):
        #print(str(self.pos))
        self.tex.bind(0)
        if self.crouching:
            changeUniform(self.pos, self.crouchScale)
        else:
            changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(self.ibuff), self.vbuff, self.ibuff, 0)

    def update(self, elapsedTime):
        if (SDLK_d or SDLK_RIGHT) in globs.keyset:
            self.direction = FACING_RIGHT
            self.pos[0] += globs.playerSpeed * elapsedTime

        if (SDLK_a or SDLK_LEFT) in globs.keyset:
            self.direction = FACING_LEFT
            self.pos[0] -= globs.playerSpeed * elapsedTime

        if (SDLK_s or SDLK_DOWN) in globs.keyset:
            self.crouching = True
        else:
            self.crouching = False

        if self.state == RISING:
            self.pos[1] += globs.playerSpeed * elapsedTime

        elif self.state == FALLING:
            self.pos[1] -= globs.playerSpeed * elapsedTime

        if SDLK_SPACE in globs.keyset and self.lastFired <= 0:               #fireBullet
            bulletPosY = self.pos[1]+self.halfSize
            if self.crouching: bulletPosY *= .5
            globs.objectsToDraw.append(Bullet(self.pos[0], bulletPosY, self.direction))
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