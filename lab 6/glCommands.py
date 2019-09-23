from Program import *
import Buffer
import array

def bindVao(vArray, iArray = None, tArray = None):
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
    if tArray != None:
        tbuff = Buffer(tArray)
        tbuff.bind(GL_ARRAY_BUFFER)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 2*4, 0)
        glBindVertexArray(0)



def setup(vertexBuff, indexBuff=None):
    glEnable(GL_MULTISAMPLE)
    glClearColor(0, 0, 0, 1.0)

    bindVao(vertexBuff)

    prog = Program("vs.txt", "fs.txt")
    prog.use()


def clear():
    glClear(GL_COLOR_BUFFER_BIT)


def draw(mode, numToDraw, array):
    bindVao(array)
    glDrawArrays(mode, 0, numToDraw)
    glBindVertexArray(0)


def drawElement(mode, numToDraw, varray, iarray, index):
    bindVao(varray, iarray)
    glDrawElements(mode, numToDraw, GL_UNSIGNED_INT, index)
    glBindVertexArray(0)