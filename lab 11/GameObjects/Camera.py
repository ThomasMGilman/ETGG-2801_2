from Program import *
from toolLibs.math3d import *

class Camera:
    def __init__(self, coi):
        self.coi        = None
        self.up         = None
        self.right      = None
        self.viewMatrix = None
        self.lookAt(coi, vec2(0,1))
        self.setUniforms()

    def lookAt(self, coi, up):
        self.coi    = vec3(coi.x, coi.y, 1)
        self.up     = vec3(up.x, up.y, 0)
        self.right  = vec3(up.y, -up.x, 0)
        self.updateViewMatrix()

    def updateViewMatrix(self):
        self.viewMatrix = mat3(
            self.right.x,                   self.up.x,                  0,
            self.right.y,                   self.up.y,                  0,
            -dot(self.coi, self.right),     -dot(self.coi, self.up),    1
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
