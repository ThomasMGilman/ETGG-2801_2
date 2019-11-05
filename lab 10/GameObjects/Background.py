from GameObjects.Entity import *

class Background(Entity):
    tex = None
    def __init__(self):
        halfWWidth = globs.worldWidth/2
        halfWHeight = globs.worldHeight/2
        if Background.tex == None:
            Background.tex = ImageTexture2DArray(globs.backgroundTextures[0])
        super().__init__(0,0,0,globs.worldWidth,globs.worldHeight, 1, 1, "Background")

    def update(self, elapsedTime):
        self.rotation += globs.backgroundRotationSpeed * elapsedTime
        self.setWorldMatrix()

    def draw(self):
        super().draw(Background.tex)