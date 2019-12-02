from utilityLibs.Texture2DArray import *
from toolLibs import image
import os.path, zipfile, io

class ImageTexture2DArray(Texture2DArray):
    def __init__(self, *files, path="assets"):
        membuf = io.BytesIO()
        width = None
        height = None
        slices = 0

        #print(str(files))
        for fname in files:
            if fname.endswith(".png") or fname.endswith(".jpg"):
                tmp = open(os.path.join(path, fname), "rb").read()
                pw, ph, fmt, pix = image.decode(tmp)
                pix = image.flipY(pw, ph, pix)
                #print(fname,pw,ph)
                #print(fname + " imageW: " + str(pw) + " imageH: " + str(ph))
                if width == None:
                    width = pw
                    height = ph
                else:
                    if width != pw or height != ph:
                        raise RuntimeError("Size mismatch"+
                                           str((width, height)) + " " + str((pw, ph)))
                slices += 1
                membuf.write(pix)

            elif fname.endswith(".ora") or fname.endswith(".zip"):
                z = zipfile.ZipFile(os.path.join(path, fname))
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

        #Push texture data to gpu
        Texture2DArray.__init__(self, width, height, slices)
        tmp = array.array("I", [0])
        glGenTextures(1, tmp)
        self.tex = tmp[0]
        self.bind(0)            #set superclass tex as the active tex object

        glTexImage3D(
            GL_TEXTURE_2D_ARRAY,    #Type of Texture
            0,                      #Mip Level
            GL_RGBA,                #Internal Format
            width, height, slices,  #Size
            0,                      #Border
            GL_RGBA,                #In Data Format
            GL_UNSIGNED_BYTE,       #In Data type
            membuf.getbuffer())     #In Data

        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)   #enable mipMapping

        self.unbind(0)