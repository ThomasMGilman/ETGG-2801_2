from sdl2.sdlmixer import Mix_FadeInChannelTimed
from GameObjects.Entity import *
import  globs

class Bullet(Entity):
    tex = None
    def __init__(self, x, y, direction, size = .1):
        self.pos = math3d.vec2(x, y)
        self.scale = math3d.vec2(size, size)
        self.dir = direction
        self.life = 750

        if Bullet.tex == None:
            Bullet.tex = ImageTexture2DArray.ImageTexture2DArray(globs.bulletTextures[0])

        super().__init__()

        self.playSound()

    def update(self, elapsedTime):
        bulletMovRate = (globs.bulletSpeed * elapsedTime)

        if self.dir == globs.FACING_LEFT:
            self.pos[0] -= bulletMovRate
        elif self.dir == globs.FACING_RIGHT:
            self.pos[0] += bulletMovRate
        else:
            self.pos[1] += bulletMovRate

        self.life -= elapsedTime

    def draw(self):
        super().draw(self.pos, self.scale, Bullet.tex, 0)

    def alive(self):
        return self.life > 0

    def playSound(self):
        Mix_FadeInChannelTimed(-1, globs.pulseSound, 0, 0, globs.pulseSoundTime)  #sounds found in globs.py