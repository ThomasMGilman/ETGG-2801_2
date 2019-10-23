from GameObjects.Entity import *

class Enemy(Entity):
    tex = None
    def __init__(self, x, y, direction, Width, Height, texNum):
        if Enemy.tex == None:
            Enemy.tex = []
            for tex in globs.enemyTextures:
                Enemy.tex.append(ImageTexture2DArray(tex))

        self.texNum = texNum if texNum < len(Enemy.tex) else 0
        super().__init__(x, y, direction, Width, Height, globs.enemyLife, globs.enemySpeed, "Enemy"+str(self.texNum))

    def update(self, elapsedTime):
        super().update(elapsedTime)

        if (self.pos.x or self.pos.y) > 1 or (self.pos.x or self.pos.y) < -1:
            self.life = 0

    def draw(self):
        super().draw(Enemy.tex[self.texNum], 0)

    def alive(self):
        if (self.pos.x < -1 - self.Width and self.dir == globs.FACING_LEFT) \
            or (self.pos.x > 1 + self.Width  and self.dir == globs.FACING_RIGHT) \
            or (self.pos.y > 1 + self.Height and self.dir == globs.FACING_UP) \
            or (self.pos.y < -1 - self.Height and self.dir == globs.FACING_DOWN):
                self.life = 0
        return super().alive()