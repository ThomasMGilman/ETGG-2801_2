from utilityLibs.ImageTexture2DArray import *
from utilityLibs.Buffer import *
from toolLibs.math3d import *
import os

class Mesh:

    def __init__(self, fname):
        self.fname = os.path.join("assets",fname)
        self.materialDict
        self.curMat
        V = []
        T = []
        I = []

        with open(fname) as fp:
            for line in fp:
                line = line.strip()
                if  line.startswith("#"):           #line is a Comment
                    continue

                elif line.startswith("mtlib"):      #Get Meshes material file name and get its textures
                    matfname = line[7:]
                    self.materialDict = self.parseMtl(matfname)

                elif line.startswith("v "):         #Get Meshes vertex points
                    vertices = line.split()
                    V.append(vec3(float(vertices[1]), float(vertices[2]), float(vertices[3])))

                elif line.startswith("vt"):
                    texturePoints = line.split()
                    T.append(vec2(float(texturePoints[1]), float(texturePoints[2])))

                elif line.startswith("usemtl"):
                    curMat = line.split()[1]
                    if curMat not in I:
                        I[curMat] = []

                elif line.startswith("f "):
                    L = line.split()
                    if len(L) != 4:
                        raise Exception("Not Triangles")

                    for VSpec in L[1:]:
                        L2 = VSpec.split('/')
                        if len(L2) != 3:
                            raise Exception("Expected vi / ti / ni, instead got: ", L2)

                        if L2[1] == "":
                            raise Exception("Expected vertex index, instead got None!!! L2 contains: ", L2)

                        vi = int(L2[0]) - 1
                        ti = int(L2[1]) - 1
                        I[curMat].append((vi, ti))

        tmp = array.array("I", [0])
        glGenVertexArrays(1, tmp)
        self.vao = tmp[0]

        vmap = {}               #key = (vi,ti), Val = index
        p = []
        t = []
        i = []
        numV = 0
        self.matDict = {}       #key = matName, Val = (startIndex, size)

        for mname in I:
            for vi,ti in I[mname]:
                key = (vi,ti)

                if key not in vmap:
                    vmap[key] = numV
                    numV += 1
                    p.append(V[vi].x)
                    p.append(V[vi].y)
                    p.append(V[vi].z)

                    t.append(T[ti].x)
                    t.append(T[ti].y)

                i.append(vmap[key])

            self.matDict[mname] = (len(i) * 4, len(I[mname]))

        pointBuf = Buffer(array.array("f", p))
        texBuf = Buffer(array.array("f", t))
        indexBuf = Buffer(array.array("I", i))
        glBindVertexArray(self.vao)

    """Add the new Materail to the dictionary"""
    def parseMtl(self, fname):
        MeshColors = {}
        with open(os.path.join("assets", fname)) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("newmtl"):
                    section = line[7:]
                elif line.startswith("map_Kd"):
                    texfile = line[7:]
                    MeshColors[section] = ImageTexture2DArray(texfile)
        return MeshColors

    def draw(self):
        glBindVertexArray(self.vao)
        for mname in self.matDict:
            self.materialDict[mname].bind(0)
            start, count = self.matDict[mname]

            glDrawElements(
                GL_TRIANGLES,
                count,
                GL_UNSIGNED_INT,
                start
            )