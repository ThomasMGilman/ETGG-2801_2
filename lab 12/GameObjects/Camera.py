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
        self.lookAt(coi, vec3(0,0,1), vec3(0,1,0))
        self.setUniforms()

    def lookAt(self, eye, coi, up):
        self.eye    = eye.xyz
        self.coi    = coi.xyz
        self.look   = normalize(coi.xyz - self.eye)
        self.right  = normalize(cross(up, self.look))
        self.up     = cross(self.look, self.right)
        self.updateViewMatrix()

    def updateViewMatrix(self):
        self.viewMatrix = mat4(
            self.right.x,                   self.up.x,                  self.look.x,                0,
            self.right.y,                   self.up.y,                  self.look.y,                0,
            self.right.z,                   self.up.z,                  self.look.z,                0,
            -dot(self.eye, self.right),     -dot(self.eye, self.up),    -dot(self.eye, self.look),  1
        )

    def setupProjMatrix(self):
        self.hither = -1
        self.yon = 1
        self.fovH = (globs.WIN_WIDTH / globs.WIN_HEIGHT) * globs.FOV
        self.dH = 1 / (math.tan(self.fovH))
        self.dV = 1 / (math.tan(globs.FOV))
        self.P = -(1 + ((2 * self.yon) / (self.hither - self.yon)))
        self.Q = (2 * self.hither * self.yon) / (self.hither - self.yon)
        self.projMatrix = mat4(
            self.dH,    0,          0,              0,
            0,          self.dV,    0,              0,
            0,          0,          self.P,         1,
            0,          0,          self.Q,         0
        )

    def strafe(self, dr, du, dl):
        self.eye += (self.right * dr) + (self.up * du) + (self.look * dl)
        self.updateViewMatrix()

    def turn(self, amount):
        M = rotation3(self.up, amount)
        self.right = (vec4(self.right, 0)*M).xyz
        self.look = (vec4(self.look,0)*M).xyz
        self.updateViewMatrix()

    def roll(self, amount):
        M = rotation3(self.look, amount)
        self.right = (vec4(self.right, 0)*M).xyz
        self.up = (vec4(self.up, 0)*M).xyz
        self.updateViewMatrix()

    def pitch(self, amount):
        M = rotation3(self.right, amount)
        self.up = (vec4(self.up, 0)*M).xyz
        self.look = (vec4(self.look,0)*M).xyz
        self.updateViewMatrix()

    def tilt(self, amount):
        M = rotation3(self.look, amount)
        self.right = (vec4(self.right, 0)*M).xyz
        self.up = (vec4(self.up, 0)*M).xyz
        self.updateViewMatrix()

    def pan(self, dx, dy):
        self.coi.x += dx
        self.coi.y += dy
        self.updateViewMatrix()

    def setUniforms(self):
        # assuming shader does p * M and not M * p
        Program.setUniform("viewMatrix", self.viewMatrix)
        Program.setUniform("projMatrix", self.projMatrix)

