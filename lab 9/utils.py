from Buffer import *

#make a vao for a square with the given x and y size.
#optionally flip the texture y coordinates
def makeSquare(xsz,ysz,flipTextureY):
    vbuff = Buffer( array.array("f",[
        -xsz,-ysz, xsz,-ysz,  xsz,ysz,  -xsz,ysz ]))
    if flipTextureY:
        tbuff = Buffer( array.array("f", [
            0,1,  1,1,  1,0,   0,0 ] ))
    else:
        tbuff = Buffer( array.array("f", [
            0,0,  1,0,  1,1,   0,1 ] ))
    ibuff = Buffer(array.array("I",[ 0,1,2, 0,2,3 ]))
    tmp = array.array("I",[0])
    glGenVertexArrays(1,tmp)
    vao = tmp[0]
    glBindVertexArray(vao)
    ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)
    vbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer( 0, 2, GL_FLOAT, False, 2*4, 0 )
    tbuff.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer( 1, 2, GL_FLOAT, False, 2*4, 0 )
    glBindVertexArray(0)
    return vao
