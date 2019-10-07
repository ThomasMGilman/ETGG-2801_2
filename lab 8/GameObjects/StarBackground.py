from toolLibs import math3d
from utilityLibs import glCommands
from utilityLibs.ImageTexture2DArray import *
from GameObjects import Shapes
import globs, array

class StarBackground:
    vbuff = None
    tbuff = None
    vao = None
    tex = None
    def __init__(self, x, y):
        self.pos = math3d.vec2(x, y)
        if StarBackground.vbuff == None:
            StarBackground.vbuff = array.array("f")
            StarBackground.tbuff = array.array("f")
            Shapes.createRandPoints(StarBackground.vbuff, globs.numStars)
            Shapes.createSquareTextureArray(self.tbuff)
            StarBackground.vao = glCommands.setup(StarBackground.vbuff, StarBackground.tbuff)
            StarBackground.tex = ImageTexture2DArray(*globs.starTextures)

    def draw(self):
        glCommands.changeUniform(self.pos)
        glCommands.drawElement(glCommands.GL_POINTS, len(StarBackground.vbuff), StarBackground.vao, StarBackground.tex)

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
            mapSquare.tex = ImageTexture2DArray(globs.mapTextures)
            Shapes.createSquare(mapSquare.vbuff, self.size, self.pox.x, self.pos.y)
            Shapes.createSquareIndexArray(mapSquare.ibuff)
            glCommands.setup(mapSquare.vbuff, mapSquare.ibuff, mapSquare.tbuff)