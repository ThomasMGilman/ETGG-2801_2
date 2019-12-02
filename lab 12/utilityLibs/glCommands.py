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



def setup(vertexBuff, textureBuff, indexBuff = None):
    glEnable(GL_MULTISAMPLE)
    glClearColor(0, 0, 0, 1.0)

    vao = bindVao(vertexBuff, textureBuff, indexBuff)
    return vao


def clear():
    glClear(GL_COLOR_BUFFER_BIT)

def drawElement(mode, numToDraw, vao, tex, index = None, slice = 0):
    if tex != None:
        tex.bind(slice)

    glBindVertexArray(vao)

    if index == None:
        glDrawArrays(mode,              # GLenum Mode [GL_POINTS, GL_LINE_STRIP, GL_LINE_LOOP, GL_LINES, GL_LINE_STRIP_ADJACENCY, GL_LINES_ADJACENCY, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_TRIANGLES, GL_TRIANGLE_STRIP_ADJACENCY, GL_TRIANGLES_ADJACENCY and GL_PATCHES]
                     0,                 # Pointer to start of index in enabled array
                     numToDraw)         # num indicies to render
    else:
        glDrawElements(mode,            # GLenum Mode [GL_POINTS, GL_LINE_STRIP, GL_LINE_LOOP, GL_LINES, GL_LINE_STRIP_ADJACENCY, GL_LINES_ADJACENCY, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_TRIANGLES, GL_TRIANGLE_STRIP_ADJACENCY, GL_TRIANGLES_ADJACENCY and GL_PATCHES]
                       numToDraw,       # Number of elements to be rendered
                       GL_UNSIGNED_INT, # Type of values in indicies
                       index)           # Pointer to start of indicies

    glBindVertexArray(0)
    if tex!= None:
        tex.unbind(slice)


def setBlendEquation(op):
    ''' :param op:
    GL_FUNC_ADD                 = src + dest
    GL_FUNC_SUBTRACT            = src - dest
    GL_FUNC_REVERSE_SUBTRACT    = dest - src
    GL_MIN                      = min(src,dest)
    GL_MAX                      = max(src,dest)
    '''
    glBlendEquation(op)


def setClassicOpacity(classic = True):
    """Opacity is set to classic by default, pass False or 0 for Premultiplied Alpha"""
    mode = GL_SRC_ALPHA if classic else GL_ONE
    glBlendFunc(mode, GL_ONE_MINUS_SRC_ALPHA)
    setBlendEquation(GL_FUNC_ADD)