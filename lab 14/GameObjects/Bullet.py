from sdl2.sdlmixer import Mix_FadeInChannelTimed
from GameObjects.Entity import *
from GameObjects.ParticleSystem import *
import globs, random

class Bullet(Entity):
    tex = None
    mesh = None
    sound = None
    def __init__(self, pos, scale, movingDir):
        self.movDir = movingDir.xyz
        if Bullet.tex == None:
            Bullet.tex = ImageTexture2DArray(globs.Textures["bullet"][0], path=globs.Textures["bullet"][-1])

        if Bullet.mesh == None:
            Bullet.mesh = glCommands.setMesh("bullet")

        if Bullet.sound == None:
            Bullet.sound = glCommands.setSound("bullet")

        super().__init__(pos, scale, globs.bulletLife, globs.bulletSpeed, "Bullet")

        self.playSound()

    def update(self, elapsedTime):
        if self.State == globs.ALIVE:
            super().updatePos(self.movDir * elapsedTime * globs.bulletSpeed)
        super().update(elapsedTime)

    def draw(self):
        super().setProgUniforms()
        Bullet.mesh.draw()

    def playSound(self):
        Mix_FadeInChannelTimed(-1, Bullet.sound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py
