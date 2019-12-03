from GameObjects.Entity import *
import globs

class StarBackground:
    tex = None
    def __init__(self, x, y, width, height):
        if StarBackground.tex == None:
            StarBackground.tex = ImageTexture2DArray(*globs.starTextures)

        super().__init__(x, y, 0, width, height, 1, 0, "StarBackground")
