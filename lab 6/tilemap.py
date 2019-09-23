
import os.path


class Map:
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
                line=line[:-1]
             outputList.append(
                [int(q) for q in line.split(",")]
             )
        self.tileList = outputList
        ...load textures to a list called self.texList...
        ...create a vao for a square...
    def draw(self):
        glBindVertexArrays(self.vao)
        for i in range(len(self.tileList)):
            row = self.tileList[i]
            for j in range(len(row)):
                Program.setUniform("translation", ...something based on i and j... )
                Program.updateUniforms()
                self.texList[row[j]-1].bind(0)
                glDrawElements()a
        
