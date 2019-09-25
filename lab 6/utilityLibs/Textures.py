from glLibs.gl import *
from glLibs.glconstants import *
from toolLibs import image
import os.path
import zipfile
import io

class Texture:
    def __init__(self, typ):
        self.type = typ;
        self.tex = None
    def bind(self, unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type, self.tex)
    def unbind(self, unit):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(self.type, 0)


class Texture2DArray(Texture):
    def __init__(self, w, h, slices):
        Texture.__init__(self, GL_TEXTURE_2D_ARRAY)
        self.width = w
        self.height = h
        self.slices = slices


class ImageTexture2DArray(Texture2DArray):
    def __init__(self, *files):
        membuf = io.BytesIO()
        width = None
        height = None
        slices = 0

        for fname in files:
            if fname.endswith(".png") or fname.endswith(".jpg"):
                tmp = open(os.path.join("assets", fname), "rb").read()
                pw, ph, fmt, pix = image.decode(tmp)
                pix = image.flipY(pw, ph, pix)
                if width == None:
                    width = pw;
                    height = ph;
                else:
                    if width != pw or height != ph:
                        raise RuntimeError("Size mismatch"+
                                           str((width, height)) + " " + str((pw, ph)))
                slices += 1
                membuf.write(pix)

            elif fname.endswith(".ora") or fname.endswith(".zip"):
                z = zipfile.ZipFile(os.path.join("assets"), fname)
                for n in sorted(z.namelist()):
                    if "thumbnail" in n:
                        continue
                    if n.endswith(".png") or n.endswith(".jpg"):
                        tmp = z.open(n).read()
                        pw, ph, fmt, pix = image.decode(tmp)
                        pix = image.flipY(pw, ph, pix)
                        if width == None:
                            width = pw;
                            height = ph
                        else:
                            if width != pw or height != ph:
                                raise RuntimeError("Size mismatch"+
                                                    str((width, height)) + " " + str((pw, ph)))
                        slices += 1
                        membuf.write(pix)
            else:
                raise RuntimeError("Cannot read file: " + fname)

        Texture2DArray.__init__(self, width, height, slices)
        tmp = array.array("I", [0])
        glGenTextures(1, tmp)
        self.tex = tmp[0]
        self.bind(0)            #set superclass tex as the active tex object

        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, width, height, slices,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, membuf.getbuffer())
        self.unbind(0)