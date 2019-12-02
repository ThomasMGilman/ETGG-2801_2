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
        if globs.Meshes.__contains__(meshName):
            for file in globs.Meshes[meshName]:
                if file.endswith(".obj"):
                    self.mesh = Mesh(file, path=globs.Meshes[meshName][-1])
                    break
            if self.mesh == None:
                Exception("Could not find .obj in Mesh folder give!! FolderName: ", meshName, " Contents:",
                          globs.Meshes[meshName])
        else:
            Exception("Mesh Dictionary does not contain a mesh folder named: ", meshName)

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