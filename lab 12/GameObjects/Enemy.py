from GameObjects.Entity import *

class Enemy(Entity):
    tex = None
    bossMesh = None
    def __init__(self, x, y, direction, Width, Height, texNum, boss = 0):
        if Enemy.tex == None:
            Enemy.tex = []
            for tex in globs.enemyTextures:
                Enemy.tex.append(ImageTexture2DArray(tex))

            Enemy.bossMesh = Mesh(globs.bossFilePath)

        self.texNum = texNum if texNum < len(Enemy.tex) else 0
        self.drawBoss = boss
        if boss:
            print("BossPos: ",x,y," moving: ",direction," size:",Width,Height)
        super().__init__(x, y, direction, Width, Height, globs.enemyLife, globs.enemySpeed, "Enemy"+str(self.texNum))

    def update(self, elapsedTime):
        super().update(elapsedTime)

        if self.pos.x > globs.worldWidth or self.pos.y > globs.worldHeight or self.pos.x < globs.minWorldX or self.pos.y < globs.minWorldX:
            self.life = 0
            if self.drawBoss:
                globs.bossInGame = False

    def draw(self):
        if not self.drawBoss:
            super().draw(Enemy.tex[self.texNum], 0)
        else:
            self.setProgUniforms()
            Enemy.bossMesh.draw()

    def alive(self):
        if (self.pos.x < -1 - self.Width and self.dir == globs.FACING_LEFT) \
            or (self.pos.x > globs.worldWidth + self.Width  and self.dir == globs.FACING_RIGHT) \
            or (self.pos.y > globs.worldHeight + self.Height and self.dir == globs.FACING_UP) \
            or (self.pos.y < -1 - self.Height and self.dir == globs.FACING_DOWN):
                self.life = 0
        return super().alive()