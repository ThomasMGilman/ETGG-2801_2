from Program import *
from gl import *
from glconstants import *
from Buffer import *
import array

class glCommands:
    def __init__(self):
        return

    def bindVao(self, vArray, iArray = None):
        vBuff = Buffer(vArray)
        # GenerateVAO
        tmp = array.array("I", [0])
        glGenVertexArrays(1, tmp)
        vao = tmp[0]
        glBindVertexArray(vao)

        # Tell GL about buffer layout and use the buffer
        # Bind index buffer to point at vertexbuffers indicies if available
        if iArray != None and len(iArray) != 0:
            ibuff = Buffer(iArray)
            ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)

        vBuff.bind(GL_ARRAY_BUFFER)

        glEnableVertexAttribArray(0)

        # which pipe, items per vertex, type per item, auto-normalize, data size per item in bytes, start in buffer
        # numPoints = len(arrayOfPoints)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)

    def setup(self, vertexBuff, indexBuff=None):
        glEnable(GL_MULTISAMPLE)
        glClearColor(0, 0, 0, 1.0)

        self.bindVao(vertexBuff)

        prog = Program("vs.txt", "fs.txt")
        prog.use()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self, mode, numToDraw, array):
        self.bindVao(array)
        glDrawArrays(mode, 0, numToDraw)
        glBindVertexArray(0)

    def drawElement(self, mode, numToDraw, varray, iarray, index):
        self.bindVao(varray, iarray)
        glDrawElements(mode, numToDraw, GL_UNSIGNED_INT, index)
        glBindVertexArray(0)