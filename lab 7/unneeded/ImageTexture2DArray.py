import io
from Texture2DArray import *
import zipfile
import image
import os.path

class ImageTexture2DArray(Texture2DArray):
    def __init__(self,*files):
        membuf = io.BytesIO()
        w=None
        h=None
        slices=0
        
        for fname in files:
            if fname.endswith(".png") or fname.endswith(".jpg"):
                tmp = open(os.path.join("assets",fname),"rb").read()
                pw,ph,fmt,pix = image.decode(tmp)
                pix = image.flipY(pw,ph,pix)
                if w == None:
                    w=pw
                    h=ph
                else:
                    if w!=pw or h!=ph:
                        raise RuntimeError("Size mismatch: "+str((w,h))+" "+str((pw,ph)))
                slices += 1
                membuf.write(pix)
                
            elif fname.endswith(".ora") or fname.endswith(".zip"):
                z = zipfile.ZipFile(os.path.join("assets",fname))
                for n in sorted(z.namelist()):
                    if "thumbnail" in n:
                        continue
                    if n.endswith(".png") or n.endswith(".jpg"):
                        ze = z.open(n)
                        tmp = ze.read()
                        pw,ph,fmt,pix = image.decode(tmp)
                        if w == None:
                            w=pw
                            h=ph
                        else:
                            if w != pw or h != ph:
                                raise RuntimeError("Size mismatch: "+str((w,h))+" "+str((pw,ph)))
                        slices+=1
                        membuf.write(pix)
            else:
                raise RuntimeError("Cannot read file "+fname)
           
        Texture2DArray.__init__(self,w,h,slices)
        tmp = array.array("I",[0])
        glGenTextures(1,tmp)
        self.tex = tmp[0]
        self.bind(0) 
        glTexImage3D( GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, 
            w,h,slices, 0, GL_RGBA, GL_UNSIGNED_BYTE, 
            membuf.getbuffer() )
        self.unbind(0)
