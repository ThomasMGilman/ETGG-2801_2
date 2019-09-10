from sdl2 import *
from sdl2.keycode import *
from sdl2.sdlmixer import *
from Program import *
import os.path
import globs
import glCommands
import sys, traceback
import Shapes

objectsToDraw = []

soundTime = 0               #in milSec

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
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)
    Mix_Init(MIX_INIT_OGG | MIX_INIT_MP3)
    Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 1, 4096)

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
    globs.DESIRED_SEC_PER_FRAME = 1 / fps
    globs.DESIRED_MSEC_PER_FRAME = int(globs.DESIRED_SEC_PER_FRAME * 1000)
    globs.TICKS_PER_SECOND = SDL_GetPerformanceFrequency()
    globs.UPDATE_QUANTUM_MSEC = 5

def draw(elapsedMSec, glCmd, window):
    glCmd.clear()
    objectsToDraw[0].draw(glCmd)  # draw background
    numObjects = len(objectsToDraw)
    if numObjects >= 1:
        i = numObjects - 1
        while i > 0:
            obj = objectsToDraw[i]
            obj.update(elapsedMSec)
            if obj.alive():
                obj.draw(glCmd)
            else:
                objectsToDraw.remove(obj)
            i -= 1;
    SDL_GL_SwapWindow(window)

def update(elapsedMsec, glCmd, bulletV_array, bulletI_array, sound, soundTime):
    ev = SDL_Event()
    while 1:
        if not SDL_PollEvent(byref(ev)):
            break
        if ev.type == SDL_QUIT:
            SDL_Quit()
            sys.exit(0)
        elif ev.type == SDL_KEYDOWN:
            k = ev.key.keysym.sym
            globs.keyset.add(k)
            #print("key down:", k)
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)
            if SDLK_SPACE in globs.keyset:
                if globs.RED < 1:
                    globs.RED += .01
                glClearColor(globs.RED, globs.GREEN, globs.BLUE, globs.ALPHA)   #Set render color to new color
        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            #print("key up:", k)
            if SDLK_SPACE in globs.keyset:                                      #Fire BULLET and go back to black
                rv = Mix_FadeInChannelTimed(-1, sound, 0, 0, soundTime)         #sounds found in globs.py
                newBullet = Shapes.Bullet(0, 0, bulletV_array, bulletI_array)
                objectsToDraw.append(newBullet)
                globs.RED = 0.0
                glClearColor(globs.RED, globs.GREEN, globs.BLUE, globs.ALPHA)   #Set render color to black

            globs.keyset.discard(k)
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

    globs.pulseSound = Mix_LoadWAV(os.path.join("assets", globs.pulseSound).encode()) # load PulseSound file

    setupFrameRateGlobals(globs.DESIRED_FRAMES_PER_SEC)

    # create glCmd object for drawing
    glCmd = glCommands.glCommands()

    starV_array = array.array("f")
    bulletV_array = array.array("f")
    bulletI_array = array.array("I")

    #seed random, initialize array, populate with random stars by num wanted
    Shapes.seedRandom()
    starV_array = Shapes.createRandPoints(starV_array, globs.numStars)
    glCmd.setup(starV_array)

    global background
    objectsToDraw.append(Shapes.StarBackground(starV_array))

    # create bullet vertex array and index array
    Shapes.createCircle(bulletV_array, .25, 0, 0)
    Shapes.createCircleIndexArray(bulletI_array)
    # Setup vao and indexbuff
    glCmd.setup(bulletV_array, bulletI_array)

    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    lastTicks = SDL_GetPerformanceCounter()
    accumElapsedMsec = 0
    while 1:
        nowTicks = SDL_GetPerformanceCounter()                                      #Get ticks at start of loop
        elapsedTicks = nowTicks - lastTicks                                         #Ticks since lastTick
        lastTicks = nowTicks                                                        #lastTick is now
        elapsedMsec = int(1000 * elapsedTicks / globs.TICKS_PER_SECOND)           #convert lastTicks to Msec
        accumElapsedMsec += elapsedMsec
        while accumElapsedMsec >= globs.UPDATE_QUANTUM_MSEC:
            update(elapsedMsec, glCmd, bulletV_array, bulletI_array, globs.pulseSound, globs.pulseSoundTime)
            accumElapsedMsec -= globs.UPDATE_QUANTUM_MSEC

        draw(elapsedMsec, glCmd, win)

        endTicks = SDL_GetPerformanceCounter()                                      #Get finale tick
        frameTicks = endTicks - nowTicks                                            #Get num ticks for frame
        frameMsec = int(frameTicks / globs.TICKS_PER_SECOND * 1000)               #convert ticks for frame to Msec
        leftoverMsec = globs.DESIRED_MSEC_PER_FRAME - frameMsec                   #calculate numTicks for desired frameRate left
        if leftoverMsec > 0:
            SDL_Delay(leftoverMsec)                                                 #delay to meet frameRate if frame doesnt take to long

main()