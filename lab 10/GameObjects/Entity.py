from utilityLibs import glCommands
from utilityLibs.ImageTexture2DArray import *
from toolLibs.math3d import *
from GameObjects import Shapes
from GameObjects.BoundingBox import *
from Program import *
import array, globs

class Entity:
    prog = None
    vao = None
    centerVao = None
    ibuffCenterSize = None
    ibuffSize = None
    ibuffStart = None
    def __init__(self, x, y, direction, Width, Height, life, speed, name, centered = False):
        self.name = name
        self.pos        = vec2(x,y)
        self.scale      = vec2(Width, Height)
        self.rotation   = 0
        self.worldMatrix= None
        self.setWorldMatrix()

        self.Width      = Width
        self.Height     = Height
        self.dir        = direction
        self.life       = life
        self.speed      = speed
        self.hitBox     = BoundingBox(self.pos, vec2(x+Width, y+Height))

        self.deathFadeT = globs.bulletLife
        self.State      = globs.ALIVE
        self.fadeTime   = 0
        self.centered = centered

        if Entity.vao == None:
            vbuff = array.array("f")
            centerVbuff = array.array("f")

            tbuff = array.array("f")
            centerTBuff = array.array("f")

            ibuff = array.array("I")
            centerIBuff = array.array("I")

            Shapes.createSquare(vbuff, 1, 1, 0, 0)        #create vbuff of square that is 1 by 1 at center of screen
            Shapes.createSquare(centerVbuff, 1, 1, 0, 0, True)

            Shapes.createSquareIndexArray(ibuff)
            Shapes.createSquareIndexArray(centerIBuff, True)

            Shapes.createSquareTextureArray(tbuff)
            Shapes.createSquareTextureArray(centerTBuff, 1, True)

            Entity.vao = glCommands.setup(vbuff, tbuff, ibuff)
            Entity.centerVao = glCommands.setup(centerVbuff, centerTBuff, centerIBuff)

            Entity.ibuffSize = len(ibuff)
            Entity.ibuffCenterSize = len(centerIBuff)
            Entity.ibuffStart = 0

            Entity.prog = Program("vs.txt", "fs.txt")

    def setWorldMatrix(self):
        self.worldMatrix = rotation2(self.rotation) * scaling2(self.scale) * translation2(self.pos)#rotation2(self.rotation) * translation2(self.pos)
        #print(self.name, self.worldMatrix)

    def setProgUniforms(self):
        alpha = 1 - (self.fadeTime / self.deathFadeT)
        Entity.prog.use()
        Program.setUniform("worldMatrix", self.worldMatrix)
        Program.setUniform("alpha", alpha)
        Program.updateUniforms()

    def draw(self, texture, slice = 0):
        if self.alive():
            self.setProgUniforms()

            glEnable(GL_BLEND)
            if not self.centered:
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glCommands.drawElement(glCommands.GL_TRIANGLES,     # Mode
                                       Entity.ibuffSize,            # number of indicies
                                       Entity.vao,                  # vao
                                       texture,                     # texture passed
                                       Entity.ibuffStart,           # start in indicies
                                       slice)                       # slice of image
            else:
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glCommands.drawElement(glCommands.GL_TRIANGLES,     # Mode
                                       Entity.ibuffCenterSize,      # number of indicies
                                       Entity.centerVao,            # vao
                                       texture,                     # texture passed
                                       Entity.ibuffStart,           # start in indicies
                                       slice)                       # slice of image
            glDisable(GL_BLEND)

    def checkCollision(self, otherBox):
        if self.hitBox.collidingWith(otherBox):
            self.kill()
            return True
        return False

    def alive(self):
        return self.life > 0

    def updateVerticalPos(self, amount):
        self.pos[1] += amount
        self.hitBox.moveY(amount)
        self.setWorldMatrix()

    def updateHorizontalPos(self, amount):
        self.pos[0] += amount
        self.hitBox.moveX(amount)
        self.setWorldMatrix()

    def update(self, elapsedTime):
        if self.State == globs.ALIVE:
            MovRate = (self.speed * elapsedTime)
            if self.dir == globs.FACING_LEFT:
                self.updateHorizontalPos(-MovRate)

            elif self.dir == globs.FACING_RIGHT:
                self.updateHorizontalPos(MovRate)

            elif self.dir == (globs.FACING_UP or globs.RISING or globs.SHOOTING_UP):
                self.updateVerticalPos(MovRate)

            elif self.dir == (globs.FACING_DOWN or globs.FALLING or globs.SHOOTING_DOWN):
                self.updateVerticalPos(-MovRate)

        elif self.State == globs.DYING:
            self.fadeTime += elapsedTime
            if self.fadeTime >= self.deathFadeT:
                self.life = 0

    def kill(self):
        self.State = globs.DYING
