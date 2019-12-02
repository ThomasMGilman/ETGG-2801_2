from sdl2.sdlmixer import Mix_FadeInChannelTimed
from GameObjects.Entity import *
from GameObjects.ParticleSystem import *
import globs, random

class Bullet(Entity):
    tex = None
    def __init__(self, pos, scale, dir):
        if Bullet.tex == None:
            Bullet.tex = ImageTexture2DArray(globs.bulletTextures[0])

        super().__init__(pos, scale, globs.bulletLife, globs.bulletSpeed, "Bullet")

        self.playSound()

    def update(self, elapsedTime):
        super().update(elapsedTime)
        self.life -= elapsedTime
        if not self.alive():
            self.kill()

    def draw(self):
        super().draw(Bullet.tex, 0)

    def playSound(self):
        Mix_FadeInChannelTimed(-1, globs.pulseSound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py

    def kill(self):
        globs.Particles.append(ParticleSystem(self.pos.xy))
        super().kill()
