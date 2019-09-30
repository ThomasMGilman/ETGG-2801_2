from Program import *
from utilityLibs import Buffer
from toolLibs import math3d
import array

def bindVao(vArray, tArray, iArray = None):
    vBuff = Buffer.Buffer(vArray)
    # GenerateVAO
    tmp = array.array("I", [0])
    glGenVertexArrays(1, tmp)
    vao = tmp[0]
    glBindVertexArray(vao)

    # Tell GL about buffer layout and use the buffer
    # Bind index buffer to point at vertexbuffers indicies if available
    if iArray != None and len(iArray) != 0:
        ibuff = Buffer.Buffer(iArray)
        ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)

    vBuff.bind(GL_ARRAY_BUFFER)

    glEnableVertexAttribArray(0)

    # which pipe, items per vertex, type per item, auto-normalize, data size per item in bytes, start in buffer
    # numPoints = len(arrayOfPoints)
    glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)

    # If a texture is passed, apply it to be associated to the vbuff
    if tArray == None:
        SystemError("Need to provide texture for object")
    else:
        tbuff = Buffer.Buffer(tArray)
        tbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 2*4, 0)
        glBindVertexArray(0)

    return vao



def setup(vertexBuff, indexBuff = None, textureBuff = None):
    glEnable(GL_MULTISAMPLE)
    glClearColor(0, 0, 0, 1.0)

    vao = bindVao(vertexBuff, indexBuff, textureBuff)

    prog = Program("vs.txt", "fs.txt")
    prog.use()

    return vao


def clear():
    glClear(GL_COLOR_BUFFER_BIT)

def changeUniform(translationVec, scalingVec = math3d.vec2(1,1)):
    Program.setUniform("translation", translationVec)
    Program.setUniform("scaling", scalingVec)
    Program.updateUniforms()

def draw(mode, numToDraw, vao, tex):
    glBindVertexArray(vao)
    tex.bind(0)
    glDrawArrays(mode, 0, numToDraw)
    glBindVertexArray(0)
    tex.unbind(0)


def drawElement(mode, numToDraw, vao, tex, index):
    glBindVertexArray(vao)
    tex.bind(0)
    glDrawElements(mode, numToDraw, GL_UNSIGNED_INT, index)
    glBindVertexArray(0)
    tex.unbind(0)