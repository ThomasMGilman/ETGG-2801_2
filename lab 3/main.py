from sdl2 import *
from sdl2.keycode import *
from Program import *
from globals import *
import glCommands
import Shapes

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

    glCmd = glCommands.glCommands()

    #seed random, initialize array, populate with random stars by num wanted
    Shapes.seedRandom()
    starArray = array.array("f")
    starArray = Shapes.createRandPoints(starArray, numStars)
    glCmd.setup(starArray)

    #Hexagon
    hexagonArray        = array.array("f")          #Vertices array
    Shapes.createHexagon(hexagonArray, .25)
    hexagonIndexArray   = array.array("I")          #point indicies array
    Shapes.createHexIndexArray(hexagonIndexArray)
    glCmd.setup(hexagonArray, hexagonIndexArray)
    print("ArrayBuff Size: {0}\n{1}".format(len(hexagonArray), hexagonArray))
    print("indexBuff Size: {0}\n{1}".format(len(hexagonIndexArray), hexagonIndexArray))

    while 1:
        update()
        glCmd.clear()
        glCmd.draw(GL_POINTS, numStars, starArray)
        glCmd.draw(GL_POINTS, len(hexagonArray), hexagonArray)
        glCmd.drawElement(GL_TRIANGLES, len(hexagonIndexArray), hexagonArray, hexagonIndexArray, 0)
        SDL_GL_SwapWindow(win)

main()