from GameObjects.Entity import *

class Background(Entity):
    tex = None
    def __init__(self):
        halfWWidth = (globs.worldWidth + 1) / 2
        halfWHeight = (globs.worldHeight + 1) / 2
        if Background.tex == None:
            Background.tex = ImageTexture2DArray(globs.backgroundTextures[1])
        super().__init__(halfWWidth, halfWHeight, 0, globs.worldWidth*2+halfWWidth, globs.worldHeight*2+halfWHeight, 1, 1, "Background", True)

    def update(self, elapsedTime):
        self.rotation += globs.backgroundRotationSpeed * elapsedTime
        self.setWorldMatrix()

    def draw(self):
        super().draw(Background.tex)