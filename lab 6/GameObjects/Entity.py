from utilityLibs import glCommands, ImageTexture2DArray
from toolLibs import math3d
from GameObjects import Shapes
import array, globs

class Entity:
    vao = None
    ibuffSize = None
    ibuffStart = None
    def __init__(self):
        if Entity.vao == None:
            print("making vao")
            vbuff = array.array("f")
            tbuff = array.array("f")
            ibuff = array.array("f")
            Entity.ibuffSize = len(ibuff)
            Entity.ibuffStart = 0

            Shapes.createSquare(vbuff, 1, 1) #create vbuff of square that is 1 by 1
            Shapes.createTriangleIndexArray(ibuff)
            Shapes.createSquareTextureArray(tbuff)
            Entity.vao = glCommands.setup(vbuff, tbuff, ibuff)

    def draw(self, texture):
        glCommands.drawElement(glCommands.GL_TRIANGLES, Entity.ibuffSize, Entity.vao, texture, 0, 0)