#glGenVertexArrays
#glBindVertexArrays
#Set info
#unbind
from gl import *
from glconstants import *
import array

class Buffer:
    def __init__(self, arrayOfData, usage = GL_STATIC_DRAW, size = None):
        tmp = array.array("I", [0])
        glGenBuffers(1, tmp)
        self.buffID = tmp[0]

        glBindBuffer(GL_ARRAY_BUFFER, self.buffID)

        if arrayOfData == None:
            glBufferData(GL_ARRAY_BUFFER, size, None, usage)
        else:
            tmp = arrayOfData.tobytes()
            glBufferData(GL_ARRAY_BUFFER, len(tmp), tmp, usage)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def bind(self, bindingPoint):
        glBindBuffer(bindingPoint, self.buffID)