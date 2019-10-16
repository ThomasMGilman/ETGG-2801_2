from gl import *
from glconstants import *
import array, os
from Buffer import *

class Program:
    uniforms={}
    ubo=None
    current = None
    
    def __init__(self,vsfname, fsfname):
        vs = self.compile(vsfname, GL_VERTEX_SHADER)
        fs = self.compile(fsfname, GL_FRAGMENT_SHADER)
        self.prog = glCreateProgram()
        glAttachShader(self.prog, vs)
        glAttachShader(self.prog, fs)
        glLinkProgram(self.prog)
        self.getLog("Linking "+vsfname+" and "+fsfname,glGetProgramInfoLog, self.prog)
        tmp = array.array("I",[0])
        glGetProgramiv( self.prog, GL_LINK_STATUS, tmp )
        if not tmp[0]:
            raise RuntimeError("Cannot link "+vsfname+" and "+fsfname)
        if Program.ubo == None:
            Program.setupUniforms(self.prog)
            
    @staticmethod
    def setupUniforms(prog):
        tmp = array.array("I",[0])
        glGetProgramiv(prog,GL_ACTIVE_UNIFORMS,tmp);
        numuniforms = tmp[0]
        uniformsToQuery = array.array("I",range(numuniforms))
        offsets = array.array("I",[0]*numuniforms)
        sizes = array.array("I",[0]*numuniforms)
        types = array.array("I",[0]*numuniforms)
        glGetActiveUniformsiv(prog, numuniforms,
            uniformsToQuery, GL_UNIFORM_OFFSET, offsets);
        glGetActiveUniformsiv(prog, numuniforms,
            uniformsToQuery, GL_UNIFORM_SIZE, sizes);
        glGetActiveUniformsiv(prog, numuniforms,
            uniformsToQuery, GL_UNIFORM_TYPE, types);

        sizeForType = {
            GL_FLOAT_VEC4: 4*4,
            GL_FLOAT_VEC3: 3*4,
            GL_FLOAT_VEC2: 2*4,
            GL_FLOAT: 1*4,
            GL_INT: 1*4,
            GL_FLOAT_MAT4: 4*16,
            GL_FLOAT_MAT3: 3*16,
            GL_FLOAT_MAT2: 2*16
        }

        nameBytes = bytearray(256)
        Program.totalUniformBytes = 0
        for i in range(numuniforms):
            glGetActiveUniformName(prog, i,
            len(nameBytes), tmp, nameBytes);
            nameLen = tmp[0]
            name = nameBytes[:nameLen].decode()
            if offsets[i] != 0xffffffff:
                assert sizes[i] == 1
                numBytes = sizeForType[types[i]]
                Program.uniforms[name] = ( offsets[i], numBytes, types[i] )
                end = offsets[i] + numBytes
                if end > Program.totalUniformBytes:
                    Program.totalUniformBytes = end
        #create_string_buffer is inside the ctypes package
        Program.uboBackingMemory = create_string_buffer(Program.
            totalUniformBytes)
        #addressof is from ctypes too
        Program.uboBackingAddress = addressof(Program.uboBackingMemory)
        Program.ubo = Buffer(
            data=None,
            size=Program.totalUniformBytes,usage=GL_DYNAMIC_DRAW )

        Program.ubo.bindBase(GL_UNIFORM_BUFFER,0)
        
    @staticmethod
    def setUniform(name,value):
        if name not in Program.uniforms:
            msg = "No such uniform '"+name+"'"
            if name+"[0]" in Program.uniforms:
                msg += "(maybe you meant '"+name+"[0]' ?)"
            raise RuntimeError(msg)
            
        offset,numBytes,typ = Program.uniforms[name]
        if typ == GL_FLOAT:
            value = array.array("f",[value])
        elif typ == GL_INT:
            value = array.array("I",[value])
            
        b = value.tobytes()
        if len(b) != numBytes:
            raise RuntimeError("Type mismatch when setting uniform '"+
                name+"': Got "+str(type(value)))
        
        dst = c_void_p(Program.uboBackingAddress+offset)
        memmove( dst, b, numBytes )
        
        
    @staticmethod
    def updateUniforms():
        glBufferSubData(GL_UNIFORM_BUFFER, 0,
            Program.totalUniformBytes,
            Program.uboBackingMemory)

    def use(self):
        glUseProgram(self.prog)
        Program.current = self
    
    def compile(self,fname,shaderType):
        s = glCreateShader(shaderType)
        lines = open(os.path.join("shaders",fname)).readlines()

        #find the '#version' line, or insert one at line zero if
        #we don't find it
        vl=0
        while vl < len(lines):
            line = lines[vl].strip()
            if line.startswith("#version "):
                break
            vl+=1
        
        if vl == len(lines):
            vl = -1
        
        upath = os.path.join("shaders","uniforms.txt")
        if os.access( upath, os.F_OK ):
            uniformdata = (
                "layout( std140, row_major ) uniform Uniforms {\n"+
                "#line 1\n"+
                open(upath).read()+
                "\n};\n" +
                "#line "+str(vl+2)+"\n"
            )
            lines.insert( vl+1, uniformdata )

        if vl == -1:
            lines.insert(0,"#version 430\n")

        src = "".join(lines)
        glShaderSource(s, 1, [src], None )
        glCompileShader(s)
        self.getLog("Compiling "+fname, glGetShaderInfoLog, s)
        tmp = array.array("I",[0])
        glGetShaderiv( s, GL_COMPILE_STATUS, tmp )
        if not tmp[0]:
            raise RuntimeError("Cannot compile "+fname)
        return s
        
    def getLog( self, description, func, identifier ):
        blob = bytearray(4096)
        tmp = array.array("I",[0])
        func( identifier, len(blob), tmp, blob )
        length = tmp[0]
        if length > 0 :
            string = blob[:length].decode()
            print(description,":")
            print(string)
             
