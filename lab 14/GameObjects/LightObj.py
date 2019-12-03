"""from GameObjects import Shapes
from utilityLibs import glCommands
from toolLibs import math3d"""
from Program import *
#import array

class LightObj:
    #vao = None
    def __init__(self, pos, color):
        self.pos = pos.xyz
        self.color = color

        """if LightObj.vao == None:
            v = []
            Shapes.createPoint(v, self.pos.x, self.pos.y, self.pos.z)
            LightObj.vao = glCommands.bindVao(array.array("f", v))"""

    def setUniforms(self):
        Program.setUniform("lightPosition", self.pos)
        Program.setUniform("lightColor", self.color.xyz)

    """def draw(self):
        self.setUniforms()
        glCommands.drawElement(glCommands.GL_POINT, 1, LightObj.vao, None)"""