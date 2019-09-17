from gl import *
from glconstants import *
from Buffer import *
import array, os

class Program:
    uniforms            = {}
    ubo                 = None

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

        if Program.ubo == None:
            Program.setupUniforms(self.prog)

    def use(self):
        glUseProgram(self.prog)

    def compile(self, fname, shaderType):
        s = glCreateShader(shaderType)

        shaderdata = open(os.path.join("shaders", fname)).read()
        uniformData = open(os.path.join("shaders", "uniforms.txt")).read()
        src = ["#version 430\n",
               "layout(std140, row_major) uniform Uniforms {\n",
               "#line 1\n",
               uniformData,
               "};\n",
               "#line 1\n",
               shaderdata]

        glShaderSource(s, len(src), src, None)
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

    @staticmethod
    def setupUniforms(prog):
        sizeForType = {
            GL_FLOAT_VEC4: 4 * 4,
            GL_FLOAT_VEC3: 3 * 4,
            GL_FLOAT_VEC2: 2 * 4,
            GL_FLOAT: 1 * 4,
            GL_INT: 1 * 4
        }
        tmp = array.array("I", [0])
        glGetProgramiv(prog, GL_ACTIVE_UNIFORMS, tmp);
        numuniforms = tmp[0]
        uniformsToQuery = array.array("I", range(numuniforms))
        offsets = array.array("I", [0] * numuniforms)
        sizes = array.array("I", [0] * numuniforms)
        types = array.array("I", [0] * numuniforms)
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_OFFSET, offsets);
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_SIZE, sizes);
        glGetActiveUniformsiv(prog, numuniforms, uniformsToQuery, GL_UNIFORM_TYPE, types);
        nameBytes = bytearray(256)
        Program.totalUniformBytes = 0
        for i in range(numuniforms):
            glGetActiveUniformName(prog, i, len(nameBytes), tmp, nameBytes);
            nameLen = tmp[0]
            name = nameBytes[:nameLen].decode()
            if offsets[i] != 0xffffffff:
                assert sizes[i] == 1
                numBytes = sizeForType[types[i]]
                Program.uniforms[name] = (offsets[i], numBytes, types[i])
                end = offsets[i] + numBytes
                if end > Program.totalUniformBytes:
                    Program.totalUniformBytes = end

        Program.uboBackingMemory = create_string_buffer(Program.totalUniformBytes)
        Program.uboBackingAddress = addressof(Program.uboBackingMemory)
        Program.ubo = Buffer(data=None,
                             size=Program.totalUniformBytes,
                             usage=GL_DYNAMIC_DRAW)
        Program.ubo.bindBase(GL_UNIFORM_BUFFER, 0)

    @staticmethod
    def setUniform(name, value):
        offset, numBytes, typ = Program.uniforms[name]

        if typ == GL_FLOAT:
            value = array.array("f", [value])
        elif typ == GL_INT:
            value = array.array("I", [value])

        print(str(value))
        b = value.tobytes()
        if len(b) != numBytes:
            raise RuntimeError("Type mismatch when setting uniform '"+name+"' : Got "+str(type(value)))

        dst = c_void_p(Program.uboBackingAddress + offset)
        memmove(dst, b, numBytes)

    @staticmethod
    def updateUniforms():
        glBufferSubData(GL_UNIFORM_BUFFER, 0, Program.totalUniformBytes, Program.uboBackingMemory)