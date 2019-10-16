from gl import *
from glconstants import *

#the non-mipmap sampler
class Sampler:
    def __init__(self):
        tmp = array.array("I",[0])
        glGenSamplers(1,tmp)
        self.samp = tmp[0]
        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
        glSamplerParameteri( self.samp, 
            GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glSamplerParameteri( self.samp, 
            GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    def bind(self,unit):
        glBindSampler(unit, self.samp )
