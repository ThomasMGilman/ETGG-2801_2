from sdl2 import *
from sdl2.keycode import *
from Program import *
import globals
import glCommands
import sys, traceback
import Shapes

def debugCallback( source, msgType, msgId, severity, length, message, param ):
    print(msgId,":",message)
    if severity == GL_DEBUG_SEVERITY_HIGH:
        for x in traceback.format_stack():
            print(x, end="")


def enableDebugging(enabled = False):
    if enabled:
        glDebugMessageCallback(debugCallback, None)
        # Source, type, severity, count, ids, enabled
        glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE,
                              0, None, True)
        glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
        glEnable(GL_DEBUG_OUTPUT)

def setupWindow():
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

    return SDL_CreateWindow(b"ETGG", 20, 20, 512, 512, SDL_WINDOW_OPENGL)

"""Setup Desired FrameRate in Globals"""
def setupFrameRateGlobals(fps):
    globals.DESIRED_SEC_PER_FRAME = 1/fps
    globals.DESIRED_MSEC_PER_FRAME = int(globals.DESIRED_SEC_PER_FRAME * 1000)
    globals.TICKS_PER_SECOND = SDL_GetPerformanceFrequency()

def update(elapsedMsec):
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

    win = setupWindow()                 #Setup SDL_GL_Attributes and get SDL_Window
    print("running");
    if not win:
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()

    enableDebugging()                  #enables debugging messages, DISABLED BY DEFAULT for performance

    setupFrameRateGlobals(globals.DESIRED_FRAMES_PER_SEC)

    # create glCmd object for drawing
    glCmd = glCommands.glCommands()

    #seed random, initialize array, populate with random stars by num wanted
    Shapes.seedRandom()
    starArray = array.array("f")
    starArray = Shapes.createRandPoints(starArray, globals.numStars)
    glCmd.setup(starArray)

    #Hexagon
    hexagonArray        = array.array("f")
    Shapes.createHexagon(hexagonArray, .25, -.5, -.5)
    hexagonIndexArray   = array.array("I")
    Shapes.createHexIndexArray(hexagonIndexArray)
    glCmd.setup(hexagonArray, hexagonIndexArray)

    #Circle
    circleArray         = array.array("f")
    Shapes.createCircle(circleArray, .25, .5, .5)
    circleIndexArray    = array.array("I")
    Shapes.createCircleIndexArray(circleIndexArray)
    glCmd.setup(circleArray, circleIndexArray)

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    lastTicks = SDL_GetPerformanceCounter()
    while 1:
        nowTicks = SDL_GetPerformanceCounter()                                      #Get ticks at start of loop
        elapsedTicks = nowTicks - lastTicks                                         #Ticks since lastTick
        lastTicks = nowTicks                                                        #lastTick is now
        elapsedMsec = int(1000 * elapsedTicks / globals.TICKS_PER_SECOND)           #convert lastTicks to Msec
        update(elapsedMsec)

        glCmd.clear()
        glCmd.draw(GL_POINTS, globals.numStars, starArray)
        glCmd.drawElement(GL_TRIANGLES, len(hexagonIndexArray), hexagonArray, hexagonIndexArray, 0)
        glCmd.drawElement(GL_TRIANGLES, len(circleIndexArray), circleArray, circleIndexArray, 0)
        SDL_GL_SwapWindow(win)

        endTicks = SDL_GetPerformanceCounter()                                      #Get finale tick
        frameTicks = endTicks - nowTicks                                            #Get num ticks for frame
        frameMsec = int(frameTicks / globals.TICKS_PER_SECOND * 1000)               #convert ticks for frame to Msec
        leftoverMsec = globals.DESIRED_MSEC_PER_FRAME - frameMsec                   #calculate numTicks for desired frameRate left
        if leftoverMsec > 0:
            SDL_Delay(leftoverMsec)                                                 #delay to meet frameRate if frame doesnt take to long

main()