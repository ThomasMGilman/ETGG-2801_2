from utilityLibs.Texture import *

class Texture2DArray(Texture):
    def __init__(self, w, h, slices):
        Texture.__init__(self, GL_TEXTURE_2D_ARRAY)
        self.width = w
        self.height = h
        self.slices = slices