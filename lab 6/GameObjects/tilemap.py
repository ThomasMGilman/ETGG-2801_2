from utilityLibs import glCommands, ImageTexture2DArray
from toolLibs import math3d
from GameObjects import Bullet, Shapes
from Program import *
from glLibs.gl import *
from glLibs.glconstants import *
import array, globs, Program
import os.path

class Map:
    vbuff = None
    tbuff = None
    ibuff = None
    vao = None
    def __init__(self):
        with open(os.path.join("assets","map.tmx")) as fp:
            data = fp.read()
        i = data.find("<data ")
        j = data.find("</data>")
        tiles = data[i:j]
        i = tiles.find(">")
        tiles = tiles[i+1:].strip()
        L = tiles.split("\n")
        outputList=[]
        for line in L:
            if line.endswith(","):
                line = line[:-1]
            outputList.append(
                [int(q) for q in line.split(",")]
            )
        self.tileList = outputList
        self.pos = math3d.vec2(0, 0)
        self.size = 2 / len(self.tileList)
        self.texList = []
        if Map.vao == None:
            Map.vbuff = array.array("f")
            Map.tbuff = array.array("f")
            Map.ibuff = array.array("I")
            for i in range(len(globs.mapTextures)):
                self.texList.append(ImageTexture2DArray.ImageTexture2DArray(globs.mapTextures[i]))
            Shapes.createSquare(Map.vbuff, self.size, self.size, -1, -1)
            Shapes.createSquareTextureArray(Map.tbuff)
            Shapes.createSquareIndexArray(Map.ibuff)
            self.vao = glCommands.setup(Map.vbuff, Map.tbuff, Map.ibuff)

        #...load textures to a list called self.texList...
        #...create a vao for a square...
    def draw(self):
        glBindVertexArray(self.vao)
        tileHeight = len(self.tileList)
        for i in range(tileHeight):
            tmpI = tileHeight-i-1
            row = self.tileList[tmpI]
            tileWidth = len(row)
            yVal = self.pos.y + (i * (2 / tileHeight))
            for j in range(tileWidth):
                xVal =  self.pos.x + (j * (2 / tileWidth))
                glCommands.changeUniform(math3d.vec2(xVal, yVal))
                self.texList[row[j]-1].bind(0)
                glDrawElements(GL_TRIANGLES,
                                len(self.ibuff),
                                GL_UNSIGNED_INT,
                                0)
        
