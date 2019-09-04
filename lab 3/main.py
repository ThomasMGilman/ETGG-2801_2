from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from gl import *
from glconstants import *
from Buffer import *
from Program import *
from globals import *
import Shapes

def setup(vertexBuff, indexBuff = None):
    glEnable(GL_MULTISAMPLE)
    glClearColor(0, 0, 0, 1.0)

    bindVao(vertexBuff)

    #Bind index buffer to point at vertexbuffers indicies if available
    if indexBuff != None and len(indexBuff) != 0:
        ibuff = Buffer(indexBuff)
        ibuff.bind(GL_ELEMENT_ARRAY_BUFFER)

    prog = Program("vs.txt", "fs.txt")
    prog.use()

def bindVao(vArray):
    vBuff = Buffer(vArray)  # array.array("f", [0, 0]))
    # GenerateVAO
    tmp = array.array("I", [0])
    glGenVertexArrays(1, tmp)
    vao = tmp[0]
    glBindVertexArray(vao)

    # Tell GL about buffer layout and use the buffer
    vBuff.bind(GL_ARRAY_BUFFER)
    # which pipe, items per vertex, type per item, auto-normalize, data size per item in bytes, start in buffer
    # numPoints = len(arrayOfPoints)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)
    # unbind
    glBindVertexArray(0)

def update():
    ev = SDL_Event()
    while 1:
        if not SDL_PollEvent(byref(ev)):
            break
        if ev.type == SDL_QUIT:
            SDL_Quit()
            sys.exit(0)
        elif ev.type == SDL_KEYDOWN:
            k = ev.key.keysym.sym
            print("key down:", k)
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)
        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            print("key up:", k)
        elif ev.type == SDL_MOUSEBUTTONDOWN:
            print("mouse down:", ev.button.button, ev.button.x, ev.button.y)
        elif ev.type == SDL_MOUSEBUTTONUP:
            print("mouse up:", ev.button.button, ev.button.x, ev.button.y)
        elif ev.type == SDL_MOUSEMOTION:
            print("mouse move:", ev.motion.x, ev.motion.y)


def draw(numToDraw, array):
    glClear(GL_COLOR_BUFFER_BIT)
    bindVao(array)
    glDrawArrays(GL_POINTS, 0, numToDraw)

def drawElement(mode, numToDraw, array):
    glClear(GL_COLOR_BUFFER_BIT)
    bindVao(array)
    glDrawElements(mode, numToDraw, GL_UNSIGNED_INT, 0)

def main():
    SDL_Init(SDL_INIT_VIDEO)

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_DEBUG_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 4)

    win = SDL_CreateWindow(b"ETGG", 20, 20, 512, 512, SDL_WINDOW_OPENGL)

    print("running");
    if not win:
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()

    #seed random, initialize array, populate with random stars by num wanted
    Shapes.seedRandom()
    starArray = array.array("f")
    starArray = Shapes.createRandPoints(starArray, numStars)
    setup(starArray)

    #Hexagon
    hexagonArray        = array.array("f")
    Shapes.createRandHexagon(hexagonArray, .25)
    hexagonIndexArray   = array.array("I")
    Shapes.createHexIndexArray(hexagonIndexArray)

    setup(hexagonArray, hexagonIndexArray)

    while 1:
        update()
        draw(numStars, starArray)
        drawElement(GL_TRIANGLES, len(hexagonArray), hexagonArray)
        SDL_GL_SwapWindow(win)

main()