from glLibs.gl import *
from glLibs.glconstants import *

class Sampler:
    def __init__(self):
        tmp = array.array("I",[0])
        glGenSamplers(1,tmp)
        self.samp = tmp[0]
        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glSamplerParameteri( self.samp,
            GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glSamplerParameteri( self.samp,
            GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def bind(self,unit):
        glBindSampler(unit, self.samp )