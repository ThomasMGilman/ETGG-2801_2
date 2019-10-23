from GameObjects.Entity import *

class Background(Entity):
    tex = None
    def __init__(self, x, y, Width, Height):
        if Background.tex == None:
            Background.tex = ImageTexture2DArray(*globs.backgroundTextures)

        super().__init__(x, y, 0, Width, Height, 1, 0, "Player")