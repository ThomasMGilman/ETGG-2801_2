from glLibs.gl import *
from glLibs.glconstants import *

class Sampler:
    def __init__(self, AnisotropicNumSamples = 1):
        tmp = array.array("I",[0])
        glGenSamplers(1,tmp)
        self.samp = tmp[0]
        self.sampleCount = AnisotropicNumSamples if (AnisotropicNumSamples >= 1 and AnisotropicNumSamples <= 16) else 1

        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_S, GL_REPEAT)

        glSamplerParameteri( self.samp,
            GL_TEXTURE_WRAP_T, GL_REPEAT)

        glSamplerParameteri( self.samp,
            GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glSamplerParameteri( self.samp,
            GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        glSamplerParameteri( self.samp,
            GL_TEXTURE_MAX_ANISOTROPY_EXT, self.sampleCount)

    def bind(self,unit):
        glBindSampler(unit, self.samp )