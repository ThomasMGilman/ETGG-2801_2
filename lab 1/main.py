from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from gl import *
from glconstants import *
import glconstants
import array

def setup():
    glEnable(GL_MULTISAMPLE)
    glClearColor(0.2,0.4,0.6,1.0)

def ps(x):
    return str(x.decode())
    
def printx(*args,**kwargs):
    print(*args,end=kwargs.get("end","\n"),file=fp)

def main():
    global fp
    fp=open("caps.txt","w")
    try:
        SDL_Init(SDL_INIT_VIDEO)

        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
        SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
        SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
        rc=None
        for major,minor in [ (4,8),(4,7),(4,6),(4,5),(4,4),(4,3),(4,2),(4,1),(4,0),(3,3) ]:
            if rc:
                break
            for withDebug in [True,False]:
                SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION,major)
                SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION,minor)
                if withDebug:
                    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS,SDL_GL_CONTEXT_DEBUG_FLAG)
                SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
                SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS,1)
                SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES,4)
            
                win = SDL_CreateWindow( b"ETGG",20,20, 512,512, SDL_WINDOW_OPENGL)
                if not win: 
                    continue

                printx("Trying to create GL",str(major)+"."+str(minor),"context with debug=",withDebug,"...",end="")
                rc = SDL_GL_CreateContext(win)
                if rc:
                    printx("Success")
                    break
                else:
                    printx("Failed")
                
                SDL_DestroyWindow(win)
           
        printx("Renderer:",ps(glGetString(GL_RENDERER)))
        printx("Vendor: ",ps(glGetString(GL_VENDOR)))
        printx("Version: ",ps(glGetString(GL_VERSION)))

        tmp = array.array("I",[0])

        for q in sorted(["MAX_3D_TEXTURE_SIZE","MAX_TEXTURE_SIZE","MAX_ARRAY_TEXTURE_LAYERS",
            "MAX_CUBE_MAP_TEXTURE_SIZE","MAX_VERTEX_ATTRIB_BINDINGS","MAX_TEXTURE_BUFFER_SIZE",
            "MAX_VERTEX_ATTRIBS","MAX_VERTEX_UNIFORM_COMPONENTS","MAX_VERTEX_OUTPUT_COMPONENTS",
            "MAX_VERTEX_TEXTURE_IMAGE_UNITS","MAX_VERTEX_SHADER_STORAGE_BLOCKS",
            "MAX_FRAGMENT_INPUT_COMPONENTS","MAX_FRAGMENT_ATOMIC_COUNTER_BUFFERS",
            "MAX_UNIFORM_BLOCK_SIZE","MAX_SHADER_STORAGE_BLOCK_SIZE","MAX_DRAW_BUFFERS",
            "MAX_COLOR_ATTACHMENTS"
            ]):
            glGetIntegerv(eval("glconstants.GL_"+q),tmp)
            printx(q,":",tmp[0])
            

        printx("GLSL: ",ps(glGetString(GL_SHADING_LANGUAGE_VERSION)))
        glGetIntegerv(GL_NUM_SHADING_LANGUAGE_VERSIONS,tmp)
        for i in range(tmp[0]):
            printx("GLSL",i,":",ps(glGetStringi(GL_SHADING_LANGUAGE_VERSION,i)))
        
            
        L=[]
        glGetIntegerv(GL_NUM_EXTENSIONS,tmp)
        for i in range(tmp[0]):
            L.append(ps(glGetStringi(GL_EXTENSIONS,i)))
        L.sort()
        for i in range(len(L)):
            printx("Extension",i,":",L[i])
        
        printx("End of report")
        
        SDL_Quit()
        
    except Exception as e:
        printx(str(e))
    finally:
        fp.close()
        print("Wrote report to caps.txt")
        
main()
sys.exit(0)
