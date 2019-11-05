from GameObjects.Entity import *
from Program import *
import globs, os.path

class Map(Entity):
    texList = None
    def __init__(self):
        with open(os.path.join("assets","map.tmx")) as fp:
            data = fp.read()
        i = data.find("<data ")
        j = data.find("</data>")
        tiles = data[i:j]
        i = tiles.find(">")
        tiles = tiles[i+1:].strip()
        L = tiles.split("\n")
        outputList=[]
        for line in L:
            if line.endswith(","):
                line = line[:-1]
            outputList.append(
                [int(q) for q in line.split(",")]
            )

        self.tileList = outputList
        self.size = 2 / len(self.tileList)
        self.originPos = vec2(-1, -1)

        super().__init__(-1, -1, 0, self.size, self.size, 1, 0, "TileMap")

        if Map.texList == None:
            Map.texList = []
            for i in range(len(globs.mapTextures)):
                Map.texList.append(ImageTexture2DArray(globs.mapTextures[i]))

    def draw(self):#FIX HERE
        tileHeight = len(self.tileList)
        for i in range(tileHeight):
            tmpI = tileHeight-i-1
            row = self.tileList[tmpI]
            tileWidth = len(row)
            self.pos.y = self.originPos.y + (i * (2 / tileHeight))
            for j in range(tileWidth):
                self.pos.x = self.originPos.x + (j * (2 / tileWidth))
                self.setWorldMatrix()
                super().draw(self.texList[row[j]-1], 0)
