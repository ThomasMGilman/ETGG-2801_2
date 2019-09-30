from toolLibs import math3d
from utilityLibs import glCommands, ImageTexture2DArray
from sdl2.sdlmixer import Mix_FadeInChannelTimed
from GameObjects import Shapes
import  globs, array

class Bullet:
    vbuff = None
    tbuff = None
    ibuff = None
    vao = None
    tex = None
    def __init__(self, x, y, direction, size = .05):
        self.pos = math3d.vec2(x, y)
        self.dir = direction
        self.life = 750

        if Bullet.vbuff == None and Bullet.ibuff == None:
            Bullet.vbuff    = array.array("f")
            Bullet.tbuff    = array.array("f")
            Bullet.ibuff    = array.array("I")
            Bullet.tex      = ImageTexture2DArray.ImageTexture2DArray(globs.bulletTextures[0])
            Shapes.createSquare(Bullet.vbuff, size, size, x, y)
            Shapes.createSquareTextureArray(Bullet.tbuff)
            Shapes.createSquareIndexArray(Bullet.ibuff)
            Bullet.vao = glCommands.setup(Bullet.vbuff, Bullet.tbuff, Bullet.ibuff)

        self.playSound()

    def update(self, elapsedTime):
        bulletMovRate = globs.bulletSpeed * elapsedTime
        if self.dir == globs.FACING_LEFT:
            self.pos[0] -= bulletMovRate
        elif self.dir == globs.FACING_RIGHT:
            self.pos[0] += bulletMovRate
        self.life -= elapsedTime

    def draw(self):
        glCommands.changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_TRIANGLES, len(Bullet.ibuff), Bullet.vao, self.tex, 0, 0)

    def alive(self):
        return self.life > 0

    def playSound(self):
        Mix_FadeInChannelTimed(-1, globs.pulseSound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py