from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from sdl2.sdlmixer import *
from gl import *
from glconstants import *
import math
import random
import traceback
import os.path
import globs        #global variables
from Program import *
from Buffer import *
from Sampler import *
from math3d import *
from Car import *

def debugCallback( source, msgType, msgId, severity, length,
    message, param ):
    print(msgId,":",message)
    if severity == GL_DEBUG_SEVERITY_HIGH:
        for x in traceback.format_stack():
            print(x,end="")

def setup():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_MULTISAMPLE)
    
    samp = Sampler()
    samp.bind(0)
    
    glClearColor(0.2,0.4,0.6,0)
    
    prog = Program("vs.txt","fs.txt")
    prog.use()
    
    globs.car = Car()
    
    
def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    globs.car.draw()
    
    
def update(elapsed):
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
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)
        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            globs.keyset.discard(k)
        elif ev.type == SDL_MOUSEBUTTONDOWN:
            print("mouse down:",ev.button.button,ev.button.x,ev.button.y)
        elif ev.type == SDL_MOUSEBUTTONUP:
            print("mouse up:",ev.button.button,ev.button.x,ev.button.y)
        elif ev.type == SDL_MOUSEMOTION:
            pass
            #print("mouse move:",ev.motion.x,ev.motion.y)
    
    
    globs.car.update( elapsed, globs.keyset )
    

def main():
    SDL_Init(SDL_INIT_VIDEO|SDL_INIT_AUDIO)
    Mix_Init(MIX_INIT_OGG | MIX_INIT_MP3)
    Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 1, 4096)

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION,4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION,3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS,SDL_GL_CONTEXT_DEBUG_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS,1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES,4)
    
    win = SDL_CreateWindow( b"ETGG",20,20, 768,768, SDL_WINDOW_OPENGL)
    if not win: 
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()
        
    glDebugMessageCallback( debugCallback, None )
    
    # Source, type, severity, count, ids, enabled
    glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE,
        0, None, True )
        
    glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
    glEnable(GL_DEBUG_OUTPUT)

    setup()
    
    DESIRED_FRAMES_PER_SEC = 60
    DESIRED_SEC_PER_FRAME = 1/DESIRED_FRAMES_PER_SEC
    DESIRED_MSEC_PER_FRAME = int(DESIRED_SEC_PER_FRAME * 1000)
    TICKS_PER_SECOND = SDL_GetPerformanceFrequency()
    UPDATE_QUANTUM_MSEC = 5
    
    lastTicks = SDL_GetPerformanceCounter()
    accumElapsedMsec = 0
    while 1:
        nowTicks = SDL_GetPerformanceCounter()
        elapsedTicks = nowTicks - lastTicks
        lastTicks = nowTicks
        elapsedMsec = int(1000 * elapsedTicks / TICKS_PER_SECOND)
        accumElapsedMsec += elapsedMsec
        while accumElapsedMsec >= UPDATE_QUANTUM_MSEC:
            update(UPDATE_QUANTUM_MSEC)
            accumElapsedMsec -= UPDATE_QUANTUM_MSEC
        draw()
        SDL_GL_SwapWindow(win)
        endTicks = SDL_GetPerformanceCounter()
        frameTicks = endTicks - nowTicks
        frameMsec = int(1000*frameTicks / TICKS_PER_SECOND)
        leftoverMsec = DESIRED_MSEC_PER_FRAME - frameMsec
        if leftoverMsec > 0:
            SDL_Delay(leftoverMsec)
        


main()
