class BoundingBox:
    """Bounding Box takes 2 points for a box object"""
    def __init__(self, llPoint, urPoint):
        self.lowerLeftPoint = llPoint.xy
        self.upperRightPoint = urPoint.xy

    def collidingWith(self, otherBox):
        if(self.rangeOverlap(self.lowerLeftPoint.x, self.upperRightPoint.x,
                                otherBox.lowerLeftPoint.x, otherBox.upperRightPoint.x) and
            self.rangeOverlap(self.upperRightPoint.y, self.lowerLeftPoint.y,
                                otherBox.upperRightPoint.y, otherBox.lowerLeftPoint.y)):
            return True
        return False

    def move(self, delta):
        self.lowerLeftPoint += delta
        self.upperRightPoint += delta

    def rangeOverlap(self, maxA, minA, maxB, minB):
        if maxA > minB:
            return False
        if minA < maxB:
            return False
        return True