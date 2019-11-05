import random
import math

def seedRandom():
    random.seed()

def appendVec2(array, x, y):
    array.append(x)
    array.append(y)


def appendVec3(array, x, y, z):
    appendVec2(array, x, y)
    array.append(z)


def mirrorAppendVec2(array, x, y):
    appendVec2(array, x, y)
    appendVec2(array, -x, -y)


def createPoint(array, x, y):
    appendVec2(array, x, y)


def createRandPoints(array, numPoints, min = -1, max = 1):
    i = 0
    while i < numPoints:
        appendVec2(array, random.uniform(min, max), random.uniform(min, max))
        i += 1


def createCircle(array, radius, cx=None, cy=None):
    """create circle points surrounding the center point"""
    centerX = cx if cx != None else random.uniform(-1 + radius, 1 - radius)
    centerY = cy if cy != None else random.uniform(-1 + radius, 1 - radius)
    appendVec2(array, centerX, centerY)
    for i in range(359):
        x = centerX + radius * math.cos(i)
        y = centerY + radius * math.sin(i)
        appendVec2(array, x, y)


def createCircleIndexArray(array):
    for i in range(358):
        appendVec3(array, 0, i+2, i+1)



def createTriangle(array, ax = None, ay = None, bx = None, by = None, cx = None, cy = None):
    Ax = ax if ax != None else random.uniform(-1, 1)
    Ay = ay if ay != None else random.uniform(-1, 1)
    Bx = bx if bx != None else random.uniform(-1, 1)
    By = by if by != None else random.uniform(-1, 1)
    Cx = cx if cx != None else random.uniform(-1, 1)
    Cy = cy if cy != None else random.uniform(-1, 1)

    appendVec2(array, Ax, Ay)
    appendVec2(array, Bx, By)
    appendVec2(array, Cx, Cy)


def createTriangleIndexArray(array):
    appendVec3(array, 0, 1, 2)


def createSquare(array, Height, Width = None, cx = None, cy = None, centerOrigin = False):
    """To specify a rectangle, pass a value for the width"""
    if Width == None:
        Width = Height
    halfHeight = Height * .5
    halfWidth = Width * .5
    originX = cx if cx != None else random.uniform(-1 + halfWidth, 1 - halfWidth)
    originY = cy if cy != None else random.uniform(-1 + halfHeight, 1 - halfHeight)

    if not centerOrigin:
        appendVec2(array, originX, originY)                             # Bottom Left corner
        appendVec2(array, originX + Width, originY)                     # Bottom Right corner
        appendVec2(array, originX + Width, originY + Height)            # TopRight corner
        appendVec2(array, originX, originY + Height)                    # TopLeft corner
    else:
        appendVec2(array, originX, originY)                             # Center Point
        appendVec2(array, originX + halfWidth, originY + halfHeight)    # TopRight corner
        appendVec2(array, originX - halfWidth, originY + halfHeight)    # TopLeft corner
        appendVec2(array, originX - halfWidth, originY - halfHeight)    # BottomLeft corner
        appendVec2(array, originX + halfWidth, originY - halfHeight)    # BottomRight corner


def createSquareIndexArray(array, centerOrigin = False):
    """Square/Rectangle is comprised of two triangles which is made up of 4 vertices"""
    if not centerOrigin:
        appendVec3(array, 0, 1, 2)
        appendVec3(array, 0, 2, 3)
    else:
        appendVec3(array, 0, 1, 2)
        appendVec3(array, 0, 2, 3)
        appendVec3(array, 0, 3, 4)
        appendVec3(array, 0, 4, 1)


def createSquareTextureArray(array, maxCoord = 1):
    appendVec2(array, 0, 0)
    appendVec2(array, maxCoord, 0)
    appendVec2(array, maxCoord, maxCoord)
    appendVec2(array, 0, maxCoord)


def createHexagon(array, size, x=None, y=None):
    """size cant be any larger than 1 as the size of the screen is from -1 to 1
        Hexagon is made of 6 triangles, so needs 7 points"""
    midPointDis = size# * 1.25
    cornerDis = size * .60

    centerX = x
    centerY = y
    if x==None: centerX = random.uniform(-1 + midPointDis, 1 - midPointDis)
    if y==None: centerY = random.uniform(-1 + midPointDis, 1 - midPointDis)

    appendVec2(array, centerX, centerY)                         #Center
    appendVec2(array, centerX + cornerDis, centerY + size)      #TopRight
    appendVec2(array, centerX - cornerDis, centerY - size)      #BottomLeft
    appendVec2(array, centerX + midPointDis, centerY)           #Right
    appendVec2(array, centerX - midPointDis, centerY)           #Left
    appendVec2(array, centerX + cornerDis, centerY - size)      #BottomRight
    appendVec2(array, centerX - cornerDis, centerY + size)      #TopLeft


def createHexIndexArray(Iarray):
    """ Hexagon vArray is size 7
          6 ____________ 1
          //\\       // \\
         //  \\     //   \\
        //    \\   //     \\
    4  //______\\ //_______\\  3
      //________ 0 _________\\
       \\      // \\       //
        \\    //   \\     //
         \\  //     \\   //
        2 \\//_______\\ // 5

    """
    appendVec3(Iarray, 0, 1, 6) #TopTriangle
    appendVec3(Iarray, 0, 3, 1) #TopRight
    appendVec3(Iarray, 0, 5, 3) #BottomRight
    appendVec3(Iarray, 0, 2, 5) #Bottom
    appendVec3(Iarray, 0, 4, 2) #BottomLeft
    appendVec3(Iarray, 0, 6, 4) #TopLeft

