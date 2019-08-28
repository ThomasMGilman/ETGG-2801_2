from gl import *
from glconstants import *
import array, os


class Program:
    def __init__(self, vsfname, fsfname):
        vs = self.compile(vsfname, GL_VERTEX_SHADER)
        fs = self.compile(fsfname, GL_FRAGMENT_SHADER)
        self.prog = glCreateProgram()
        glAttachShader(self.prog, vs)
        glAttachShader(self.prog, fs)
        glLinkProgram(self.prog)
        self.getLog("Linking " + vsfname + " and " + fsfname, glGetProgramInfoLog, self.prog)
        tmp = array.array("I", [0])
        glGetProgramiv(self.prog, GL_LINK_STATUS, tmp)
        if not tmp[0]:
            raise RuntimeError("Cannot link " + vsfname + " and " + fsfname)

    def use(self):
        glUseProgram(self.prog)

    def compile(self, fname, shaderType):
        s = glCreateShader(shaderType)
        shaderdata = open(os.path.join("shaders", fname)).read()
        glShaderSource(s, 1, [shaderdata], None)
        glCompileShader(s)
        self.getLog("Compiling " + fname, glGetShaderInfoLog, s)
        tmp = array.array("I", [0])
        glGetShaderiv(s, GL_COMPILE_STATUS, tmp)
        if not tmp[0]:
            raise RuntimeError("Cannot compile " + fname)
        return s

    def getLog(self, description, func, identifier):
        blob = bytearray(4096)
        tmp = array.array("I", [0])
        func(identifier, len(blob), tmp, blob)
        length = tmp[0]
        if length > 0:
            string = blob[:length].decode()
            print(description, ":")
            print(string)