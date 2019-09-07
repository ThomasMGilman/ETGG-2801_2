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

def createRandPoints(array, numPoints):
    i = 0
    while i < numPoints:
        appendVec2(array, random.uniform(-1, 1), random.uniform(-1, 1))
        i += 1
    return array

#create circle points surrounding the center point
def createCircle(array, radius, cx=None, cy=None):
    if cx==None: centerX = random.uniform(-1 + radius, 1 - radius)
    else: centerX = cx
    if cy==None: centerY = random.uniform(-1 + radius, 1 - radius)
    else: centerY = cy
    appendVec2(array, centerX, centerY)
    for i in range(359):
        x = centerX + radius * math.cos(i)
        y = centerY + radius * math.sin(i)
        appendVec2(array, x, y)

def createCircleIndexArray(array):
    for i in range(358):
        appendVec3(array, 0, i+2, i+1)


#size cant be any larger than 1 as the size of the screen is from -1 to 1
#Hexagon is made of 6 triangles, so needs 7 points
def createHexagon(array, size, x=None, y=None):
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
def createHexIndexArray(Iarray):
        appendVec3(Iarray, 0, 1, 6) #TopTriangle
        appendVec3(Iarray, 0, 3, 1) #TopRight
        appendVec3(Iarray, 0, 5, 3) #BottomRight
        appendVec3(Iarray, 0, 2, 5) #Bottom
        appendVec3(Iarray, 0, 4, 2) #BottomLeft
        appendVec3(Iarray, 0, 6, 4) #TopLeft
