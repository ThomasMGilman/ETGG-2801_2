import random
import array

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
def createRandHexagon(array, size):
    if size > 1:
        return False
    centerX = random.uniform(-1 + size, 1 - size)
    centerY = random.uniform(-1 + size, 1 - size)

    appendVec2(array, centerX, centerY)                        #Center
    mirrorAppendVec2(array, centerX + size/2, centerY + size)  #TopRight BottomLeft
    mirrorAppendVec2(array, centerX + size, centerY)           #Right Left
    mirrorAppendVec2(array, centerX + size/2, centerY - size)  #BottomRight TopLeft

#Hexagon vArray is size 7
def createHexIndexArray(Iarray):
        appendVec3(Iarray, 0, 1, 6)
        appendVec3(Iarray, 0, 3, 1)
        appendVec3(Iarray, 0, 5, 3)
        appendVec3(Iarray, 0, 2, 5)
        appendVec3(Iarray, 0, 4, 2)
        appendVec3(Iarray, 0, 6, 4)
