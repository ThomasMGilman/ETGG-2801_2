import random

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

#size cant be any larger than 1 as the size of the screen is from -1 to 1
#Hexagon is made of 6 triangles, so needs 7 points
def createHexagon(array, size, x=0, y=0):
    if size > 1:
        return False
    midPointDis = size# * 1.25
    cornerDis = size * .60

    centerX = x
    centerY = y
    #if x==None: centerX = random.uniform(-1 + midPointDis, 1 - midPointDis)
    #if y==None: centerY = random.uniform(-1 + midPointDis, 1 - midPointDis)

    appendVec2(array, centerX, centerY)                         #Center
    mirrorAppendVec2(array, centerX + cornerDis, centerY + size)     #TopRight BottomLeft
    appendVec2(array, centerX + midPointDis, centerY)           #Right
    appendVec2(array, centerX - midPointDis, centerY)           #Left
    mirrorAppendVec2(array, centerX + cornerDis, centerY - size)     #BottomRight TopLeft

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
