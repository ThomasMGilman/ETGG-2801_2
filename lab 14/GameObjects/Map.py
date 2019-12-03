from GameObjects.Mesh import *
from Program import *
import globs

class MapRoom:
    prog = None
    def __init__(self, pos, meshName):
        self.pos = pos.xyz
        self.worldMatrix = translation3(self.pos)
        self.mesh = None

        if MapRoom.prog == None:
            MapRoom.prog = Program("vs.txt", "fs.txt")

        self.setMesh(meshName)

    def setMesh(self, meshName):
        self.mesh = glCommands.setMesh(meshName)

    def setProg(self, prog):
        MapRoom.prog = prog

    def updateWorldMatrix(self):
        self.worldMatrix = translation3(self.pos)

    def setUniforms(self):
        MapRoom.prog.use()

        Program.setUniform("worldMatrix", self.worldMatrix)

        Program.updateUniforms()

    def draw(self):
        self.setUniforms()
        self.mesh.draw()