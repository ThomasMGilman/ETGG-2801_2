from Program import *
from GameObjects import Shapes
from utilityLibs import glCommands
from utilityLibs.ImageTexture2DArray import *
from toolLibs.math3d import *
import globs

class ParticleSystem:
    prog = None
    vao = None
    tex = None
    vSize = None
    def __init__(self, startPos):
        self.life = globs.particleLife
        self.currentTime = 0
        self.startTime = 0
        self.worldMatrix = translation2(startPos)

        if ParticleSystem.vao == None:
            vbuff = array.array("f")
            tbuff = array.array("f")
            Shapes.createRandPoints(vbuff, globs.particleCount)  #Create randomVelocities
            tbuff = Shapes.createSquareTextureArray(tbuff)
            ParticleSystem.vao = glCommands.setup(vbuff, tbuff)
            ParticleSystem.vSize = len(vbuff)
            ParticleSystem.tex = ImageTexture2DArray(globs.starTextures[0])

            ParticleSystem.prog = Program("particleVS.txt", "particleFS.txt")

    def update(self, elapsedTime):
        self.currentTime += elapsedTime
        if self.currentTime > self.life:
            self.life = 0

    def draw(self):
        if self.alive():
            oldprog = ParticleSystem.prog.current
            ParticleSystem.prog.use()
            alpha = 1 - (self.currentTime / self.life)

            Program.setUniform("totalElapsed", self.currentTime)
            Program.setUniform("pointSize", globs.particleSize)
            Program.setUniform("worldMatrix", self.worldMatrix)
            Program.setUniform("speedDivisor", globs.speedDivisor)
            Program.setUniform("alpha", alpha)
            Program.updateUniforms()

            glEnable(GL_BLEND)
            glCommands.drawElement(glCommands.GL_POINTS, ParticleSystem.vSize, ParticleSystem.vao, ParticleSystem.tex)
            glDisable(GL_BLEND)

            if oldprog != None:
                oldprog.use()

    def alive(self):
        return self.life > 0

