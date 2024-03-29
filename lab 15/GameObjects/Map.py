from GameObjects.Mesh import *
from GameObjects.LightObj import *
from Program import *
import globs

class MapRoom:
    prog = None
    def __init__(self, pos, meshName, shininess):
        self.pos = pos.xyz
        self.worldMatrix = translation3(self.pos)
        self.mesh = None
        self.Light = LightObj(
                            vec3(0, .5, 1), # Position
                            vec3(.3, .7, 1),  # Color
                            vec3(.1,.6,1),  # Attenuation
                            1,              # Positional 0 or 1
                            -1,             # Spotlight angle -1 for omnidirectional
                            vec3(0,0,1))   # Spotlight Dir
        self.alpha = 1
        self.shininess = shininess
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
        Program.setUniform("shininess", self.shininess)
        Program.setUniform("alpha", self.alpha)
        Program.setUniform("ambientColor0", vec3(0.1, 0.1, 0.1))
        Program.setUniform("ambientColor1", vec3(.5, .5, .5))

        Program.updateUniforms()

    def draw(self):
        self.setUniforms()
        self.Light.setUniforms()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.mesh.draw()
        glDisable(GL_BLEND)