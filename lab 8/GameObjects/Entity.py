from utilityLibs import glCommands
from utilityLibs.ImageTexture2DArray import *
from toolLibs import math3d
from GameObjects import Shapes
from GameObjects.BoundingBox import *
from Program import *
import array, globs

class Entity:
    prog = None
    vao = None
    ibuffSize = None
    ibuffStart = None
    def __init__(self, x, y, direction, Width, Height, life, speed):
        self.pos        = math3d.vec2(x,y)
        self.scale      = math3d.vec2(Width, Height)
        self.Width      = Width
        self.Height     = Height
        self.dir        = direction
        self.life       = life
        self.speed      = speed
        self.hitBox     = BoundingBox(self.pos, math3d.vec2(x+Width, y+Height))

        self.deathFadeT = globs.bulletLife
        self.state      = globs.ALIVE
        self.fadeTime   = 0

        if Entity.vao == None:
            vbuff = array.array("f")
            tbuff = array.array("f")
            ibuff = array.array("I")
            Entity.ibuffSize = len(ibuff)
            Entity.ibuffStart = 0

            Shapes.createSquare(vbuff, 1, 1, 0, 0)        #create vbuff of square that is 1 by 1 at center of screen
            Shapes.createSquareIndexArray(ibuff)
            Shapes.createSquareTextureArray(tbuff)
            Entity.vao = glCommands.setup(vbuff, tbuff, ibuff)

            Entity.ibuffSize = len(ibuff)
            Entity.ibuffStart = 0

            Entity.prog = Program("vs.txt", "fs.txt")

    def draw(self, position, scale, texture, slice):
        if self.alive():
            alpha = 1 - (self.fadeTime / self.deathFadeT)

            Entity.prog.use()
            Program.setUniform("alpha", alpha)
            Program.updateUniforms()

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glCommands.changeUniform(position, scale)           #setPosition and Scale
            glCommands.drawElement(glCommands.GL_TRIANGLES,     #Mode
                                   Entity.ibuffSize,            #number of indicies
                                   Entity.vao,                  #vao
                                   texture,                     #texture passed
                                   Entity.ibuffStart,           #start in indicies
                                   slice)                       #slice of image
            glDisable(GL_BLEND)

    def checkCollision(self, otherBox):
        if self.hitBox.collidingWith(otherBox):
            self.kill()
            return True
        return False

    def alive(self):
        return self.life > 0

    def update(self, elapsedTime):
        if self.state == globs.ALIVE:
            MovRate = (self.speed * elapsedTime)
            if self.dir == globs.FACING_LEFT:
                self.pos[0] -= MovRate
                self.hitBox.moveX(-MovRate)

            elif self.dir == globs.FACING_RIGHT:
                self.pos[0] += MovRate
                self.hitBox.moveX(MovRate)

            elif self.dir == (globs.FACING_UP or globs.RISING or globs.SHOOTING_UP):
                self.pos[1] += MovRate
                self.hitBox.moveY(MovRate)

            elif self.dir == (globs.FACING_DOWN or globs.FALLING or globs.SHOOTING_DOWN):
                self.pos[1] -= MovRate
                self.hitBox.moveY(-MovRate)

        elif self.state == globs.DYING:
            self.fadeTime += elapsedTime
            if self.fadeTime >= self.deathFadeT:
                self.life = 0

    def kill(self):
        self.state = globs.DYING
