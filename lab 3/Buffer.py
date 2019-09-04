#glGenVertexArrays
#glBindVertexArrays
#Set info
#unbind
from gl import *
from glconstants import *
import array

class Buffer:
    def __init__(self, dataAsFloatArray):
        tmp = array.array("I", [0])
        glGenBuffers(1, tmp)
        self.buffID = tmp[0]

        glBindBuffer(GL_ARRAY_BUFFER, self.buffID)
        tmp = dataAsFloatArray.tobytes()
        glBufferData(GL_ARRAY_BUFFER, len(tmp), tmp, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bind(self, bindingPoint):
        glBindBuffer(bindingPoint, self.buffID)