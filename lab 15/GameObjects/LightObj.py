from toolLibs import math3d
from Program import *

class LightObj:
    def __init__(self, pos, color, attenuation, positional = 1, spotAngle = -1.0, spotDir = math3d.vec3(0, 0, 1)):
        self.pos = math3d.vec4(pos.xyz, positional)
        self.color = color.xyz

        self.attenuation = attenuation.xyz
        self.spotDir = spotDir.xyz
        if spotAngle < -1 or spotAngle <= 0:
            self.spotLightAngle = -1.0
        else:
            self.spotLightAngle = spotAngle

    def setUniforms(self):
        Program.setUniform("lightPosition", self.pos)
        Program.setUniform("lightColor", self.color.xyz)
        Program.setUniform("attenuation", self.attenuation)
        Program.setUniform("cosineMaxSpotAngle", self.spotLightAngle)
        Program.setUniform("spotDirection", self.spotDir)