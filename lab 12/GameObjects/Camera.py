from Program import *
from toolLibs.math3d import *
import globs, math

class Camera:
    def __init__(self, coi):
        self.coi        = None
        self.up         = None
        self.right      = None
        self.viewMatrix = None
        self.setupProjMatrix()
        self.lookAt(coi, vec2(0,1))
        self.setUniforms()

    def lookAt(self, eye, coi, up):
        self.eye    = eye.xyz
        self.coi    = coi.xyz
        self.look   = normalize(coi.xyz - self.eye)
        self.right  = normalize(cross(up, self.look))
        self.up     = cross(self.look, self.right)
        self.updateViewMatrix()

    def updateViewMatrix(self):
        self.viewMatrix = mat3(
            self.right.x,                   self.up.x,                  0,
            self.right.y,                   self.up.y,                  0,
            -dot(self.coi, self.right),     -dot(self.coi, self.up),    1
        )

    def setupProjMatrix(self):
        self.hither = -1
        self.yon = 1
        self.fovH = (globs.WIN_WIDTH / globs.WIN_HEIGHT) * globs.fov
        self.dH = 1 / (math.tan(self.fovH))
        self.dV = 1 / (math.tan(globs.fov))
        self.P = -(1 + ((2 * self.yon) / (self.hither - self.yon)))
        self.Q = (2 * self.hither * self.yon) / (self.hither - self.yon)
        self.projMatrix = mat4(
            self.dH,    0,          0,              0,
            0,          self.dV,    0,              0,
            0,          0,          self.P,         1,
            0,          0,          self.Q,         0
        )

    def tilt(self, amount):
        M = rotation2(amount)
        self.right = self.right * M
        self.up = self.up * M
        self.updateViewMatrix()

    def pan(self, dx, dy):
        self.coi.x += dx
        self.coi.y += dy
        self.updateViewMatrix()

    def setUniforms(self):
        # assuming shader does p * M and not M * p
        Program.setUniform("viewMatrix", self.viewMatrix)
        Program.setUniform("projMatrix", self.projMatrix)

