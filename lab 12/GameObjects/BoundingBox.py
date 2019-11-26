class BoundingBox:
    """Bounding Box takes 2 points for a box object"""
    def __init__(self, llPoint, urPoint):
        self.lowerLeftPoint = llPoint.xy
        self.upperRightPoint = urPoint.xy

    def collidingWith(self, otherBox):
        if(self.rangeOverlapX(self.lowerLeftPoint.x, self.upperRightPoint.x,
                                otherBox.lowerLeftPoint.x, otherBox.upperRightPoint.x) and
            self.rangeOverlapY(self.upperRightPoint.y, self.lowerLeftPoint.y,
                                otherBox.upperRightPoint.y, otherBox.lowerLeftPoint.y)):
            return True
        return False

    def moveX(self, delta):
        self.lowerLeftPoint.x += delta
        self.upperRightPoint.x += delta

    def moveY(self, delta):
        self.lowerLeftPoint.y += delta
        self.upperRightPoint.y += delta

    """Grid of Window
     _______1_______
    |       |       |
    |       |       |
    -1----- 0 ------1
    |       |       |
    |______-1_______|
    """
    def rangeOverlapX(self, maxA, minA, maxB, minB):
        if ((maxA >= maxB and maxA <= minB) or
            (minA >= maxB and minA <= minB)):
            return True
        return False

    def rangeOverlapY(self, maxA, minA, maxB, minB):
        if((maxA <= maxB and maxA >= minB) or
            (minA <= maxB and minA >= minB)):
            return True
        return False