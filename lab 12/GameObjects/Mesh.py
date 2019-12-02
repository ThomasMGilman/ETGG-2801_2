from utilityLibs.ImageTexture2DArray import *
from utilityLibs import glCommands
from toolLibs.math3d import *
import os

class Mesh:
    def __init__(self, f, path="assets"):
        self.fname = os.path.join(path,f)
        self.materialDict = {}
        curMat = None
        VertexPoints = []           # Vertex Vec3 Points for Mesh
        Normals = []
        TexturePoints = []          # Texture Vec2 Points for Mesh
        IndexPoints = {}            # Index Points in vertex points and texture points
        with open(self.fname) as fp:
            for line in fp:
                line = line.strip()
                if  line.startswith("#"):           # line is a Comment ignore it
                    continue

                elif line.startswith("mtllib"):      # Get Meshes material file name and get its textures
                    matfname = line[7:]
                    self.materialDict = self.parseMtl(matfname, path)

                elif line.startswith("v "):         # Get Meshes vertex points
                    vertices = line.split()
                    VertexPoints.append(vec3(float(vertices[1]), float(vertices[2]), float(vertices[3])))

                elif line.startswith("vt"):         # Get Meshes Texture points
                    texturePoints = line.split()
                    TexturePoints.append(vec2(float(texturePoints[1]), float(texturePoints[2])))

                elif line.startswith("vn"):         # Get Meshes Normal points
                    normalPoints = line.split()
                    Normals.append(vec3(float(normalPoints[1]), float(normalPoints[2]), float(normalPoints[3])))

                elif line.startswith("usemtl"):     # Set CurrentMaterial
                    curMat = line.split()[1]
                    if curMat not in IndexPoints:
                        IndexPoints[curMat] = []

                elif line.startswith("f "):         # Set CurrentMaterials Vertex Points, Texture Points, and Normals
                    fLine = line.split()
                    if len(fLine) != 4:
                        raise Exception("Not Triangles")

                    for VSpec in fLine[1:]:
                        pointPack = VSpec.split('/')
                        if len(pointPack) != 3:
                            raise Exception("Expected vi / ti / ni, instead got: ", pointPack)

                        if pointPack[1] == "":
                            raise Exception("Expected vertex index, instead got None!!! pointPack contains: ", pointPack)

                        vi = int(pointPack[0]) - 1              # Set Vertice Index
                        ti = int(pointPack[1]) - 1              # Set Texture Index
                        #ni = int(pointPack[2]) - 1              # Set Normal Index
                        IndexPoints[curMat].append((vi, ti))

        tmp = array.array("I", [0])       # Set vao
        glGenVertexArrays(1, tmp)
        self.vao = tmp[0]

        vmap = {}               # key = (vi,ti), Val = index
        p = []
        t = []
        # n = []
        i = []
        numV = 0
        self.matDict = {}       # key = matName, Val = (startIndex, size)

        for matName in IndexPoints:                 # Foreach key

            # Set Start starting point into point set, and number of indices for point set for material
            self.matDict[matName] = (len(i) * 4, len(IndexPoints[matName]))

            for vi, ti in IndexPoints[matName]:     # Foreach value pair
                key = (vi, ti)

                if key not in vmap:                         # Append key to dictionary if not already there
                    vmap[key] = numV
                    numV += 1

                    # Set Vertex Values, 3 floats per point
                    p.append(VertexPoints[vi].x)
                    p.append(VertexPoints[vi].y)
                    p.append(VertexPoints[vi].z)

                    # Set Texture Values, 2 floats per point
                    t.append(TexturePoints[ti].x)
                    t.append(TexturePoints[ti].y)

                    # Set Normal values, 3 floats per point
                    # n.append(Normals[ni].x)
                    # n.append(Normals[ni].y)
                    # n.append(Normals[ni].z)

                i.append(vmap[key])                        # Append Index into dictionary for point value set

        pointBuf    = array.array("f", p)           # Create Point Buffer
        texBuf      = array.array("f", t)           # Create Texture Buffer
        indexBuf    = array.array("I", i)           # Create Index buffer for index points
        self.vao = glCommands.setup(pointBuf, texBuf, indexBuf)

    def parseMtl(self, fname, path):
        """Add the new Materail to the dictionary"""
        MeshColors = {}
        with open(os.path.join(path, fname)) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("newmtl"):
                    section = line[7:]
                elif line.startswith("map_Kd"):
                    texfile = line[7:]
                    #print("Texture of:", texfile + " added")
                    MeshColors[section] = ImageTexture2DArray(texfile, path=path)
        return MeshColors

    def draw(self):
        glBindVertexArray(self.vao)
        #print(self.matDict)
        for mname in self.matDict:
            self.materialDict[mname].bind(0)        # Bind Texture
            start, count = self.matDict[mname]      # Set start index, and len of indicies
            #print("start:",start,"count:",count)

            glDrawElements(
                GL_TRIANGLES,
                count,
                GL_UNSIGNED_INT,
                start
            )