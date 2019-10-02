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

    def draw(self, position, scale, texture, slice):
        glCommands.changeUniform(position, scale)
        glCommands.drawElement(glCommands.GL_TRIANGLES,
                               Entity.ibuffSize,
                               Entity.vao,
                               texture,
                               Entity.ibuffStart,
                               slice)