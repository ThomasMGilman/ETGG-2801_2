from gl import *
from glconstants import *
import os.path
import image
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
        self.membuf = io.BytesIO()
        self.width = None
        self.height = None
        self.slices = 0

        for fname in files:
            if fname.endswith(".png") or fname.endswith(".jpg"):
                tmp = open(os.path.join("assets", fname), "rb").read()
                pw, ph, fmt, pix = image.decode(tmp)
                pix = image.flipY(pw, ph, pix)
                if self.width == None:
                    self.width = pw;
                    self.height = ph;
                else:
                    if self.width != pw or self.height != ph:
                        raise RuntimeError("Size mismatch"+
                                           str((self.width, self.height)) + " " + str((pw, ph)))
                self.slices += 1
                self.membuf.write(pix)

            elif fname.endswith(".ora") or fname.endswith(".zip"):
                z = zipfile.ZipFile(os.path.join("assets"), fname)
                for n in sorted(z.namelist()):
                    if "thumbnail" in n:
                        continue
                    if n.endswith(".png") or n.endswith(".jpg"):
                        tmp = z.open(n).read()
                        pw, ph, fmt, pix = image.decode(tmp)
                        pix = image.flipY(pw, ph, pix)
                        if self.width == None:
                            self.width = pw;
                            self.height = ph
                        else:
                            if self.width != pw or self.height != ph:
                                raise RuntimeError("Size mismatch"+
                                                    str((self.width, self.height)) + " " + str((pw, ph)))
                        self.slices += 1
                        self.membuf.write(pix)
            else:
                raise RuntimeError("Cannot read file: " + fname)

        Texture2DArray.__init__(self, self.width, self.height, self.slices)
        tmp = array.array("I", [0])
        glGenTextures(1, tmp)
        self.tex = tmp[0]
        self.bind(0)            #set superclass tex as the active tex object

        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, self.width, self.height, self.slices,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, self.membuf.getbuffer())
        self.unbind(0)