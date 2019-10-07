from Program import *
from toolLibs import math3d
from GameObjects import Shapes
from utilityLibs import glCommands
from utilityLibs.ImageTexture2DArray import *
import globs

class ParticleSystem:
    prog = None
    vao = None
    tex = None
    pointCount = None
    position = None
    def __init__(self, startPos = None):
        self.life = globs.particleLife
        self.currentTime = 0
        self.startTime = 0
        if startPos != None:
            ParticleSystem.position = startPos

        if ParticleSystem.vao == None:
            ParticleSystem.prog = Program(os.path.join("shaders", "particleVS.txt"), os.path.join("shaders", "particleFS.txt"))
            vbuff = array.array("f")
            tbuff = array.array("f")
            Shapes.createRandPoints(vbuff, globs.particleCount)  #Create randomVelocities
            tbuff = Shapes.createSquareTextureArray(tbuff)
            ParticleSystem.vao = glCommands.setup(vbuff, tbuff)
            ParticleSystem.pointCount = len(vbuff)

    def update(self, elapsedTime):
        self.currentTime += elapsedTime
        if self.currentTime > self.life:
            self.life = 0

    def draw(self):
        glEnable(GL_BLEND)
        glCommands.drawElement(glCommands.GL_POINTS, ParticleSystem.pointCount, ParticleSystem.vao, ParticleSystem.tex)
        glDisable(GL_BLEND)

    def alive(self):
        return self.life > 0

